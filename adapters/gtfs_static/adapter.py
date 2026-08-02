"""Validador mínimo, local e read-only de GTFS Schedule."""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


STATUSES = (
    "ok",
    "no_result",
    "stale",
    "blocked",
    "auth_required",
    "manual_review",
    "unsupported",
)

REQUIRED_TABLES = {
    "agency.txt": ("agency_id", "agency_name", "agency_url", "agency_timezone"),
    "routes.txt": ("route_id", "agency_id", "route_type"),
    "stops.txt": ("stop_id", "stop_name", "stop_lat", "stop_lon"),
    "trips.txt": ("route_id", "service_id", "trip_id"),
    "stop_times.txt": (
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
    ),
    "calendar.txt": (
        "service_id",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "start_date",
        "end_date",
    ),
}

WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)

CHECKS = (
    "arquivos obrigatórios presentes",
    "CSV UTF-8 com cabeçalhos e linhas válidas",
    "chaves obrigatórias únicas",
    "referências entre tabelas sem órfãos",
    "coordenadas dentro dos limites numéricos",
    "fuso horário reconhecido pela base local",
    "calendário com datas e dias válidos",
    "stop_times com sequência e horários coerentes",
)

_TIME_PATTERN = re.compile(r"\d{1,2}:\d{2}:\d{2}\Z")


@dataclass(frozen=True)
class ValidationResult:
    """Saída estável do validator; não contém dados de linhas do feed."""

    status: str
    errors: tuple[str, ...] = ()
    checks: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "errors": list(self.errors),
            "checks": list(self.checks),
        }


class _FeedIssue(Exception):
    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


def _clean(row: dict[str, str], field: str) -> str:
    value = row.get(field)
    return value.strip() if isinstance(value, str) else ""


def _required(
    row: dict[str, str], field: str, filename: str, line: int, errors: list[str]
) -> str:
    value = _clean(row, field)
    if not value:
        errors.append(f"{filename}: campo obrigatório ausente na linha {line}: {field}")
    return value


def _read_table(root: Path, filename: str, columns: tuple[str, ...]) -> list[dict[str, str]]:
    path = root / filename
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            fieldnames = reader.fieldnames
            if not fieldnames or any(not name or not name.strip() for name in fieldnames):
                raise _FeedIssue("unsupported", f"{filename}: cabeçalho ausente ou vazio")
            if len(set(fieldnames)) != len(fieldnames):
                raise _FeedIssue("unsupported", f"{filename}: cabeçalho duplicado")
            missing = [column for column in columns if column not in fieldnames]
            if missing:
                joined = ", ".join(missing)
                raise _FeedIssue("unsupported", f"{filename}: colunas ausentes: {joined}")

            rows: list[dict[str, str]] = []
            for line, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    raise _FeedIssue(
                        "unsupported",
                        f"{filename}: quantidade de colunas inválida na linha {line}",
                    )
                rows.append(row)
            if not rows:
                raise _FeedIssue("unsupported", f"{filename}: tabela vazia")
            return rows
    except FileNotFoundError as exc:
        raise _FeedIssue("unsupported", f"arquivo obrigatório ausente: {filename}") from exc
    except PermissionError as exc:
        raise _FeedIssue("blocked", f"leitura bloqueada: {filename}") from exc
    except UnicodeDecodeError as exc:
        raise _FeedIssue("unsupported", f"{filename}: arquivo não está em UTF-8") from exc
    except csv.Error as exc:
        raise _FeedIssue("unsupported", f"{filename}: CSV inválido") from exc
    except OSError as exc:
        raise _FeedIssue("blocked", f"não foi possível ler {filename}") from exc


def _unique_ids(
    filename: str,
    rows: list[dict[str, str]],
    field: str,
    errors: list[str],
) -> set[str]:
    seen: set[str] = set()
    for line, row in enumerate(rows, start=2):
        value = _required(row, field, filename, line, errors)
        if value and value in seen:
            errors.append(f"{filename}: chave duplicada na linha {line}: {field}")
        elif value:
            seen.add(value)
    return seen


def _parse_int(
    value: str, filename: str, field: str, line: int, errors: list[str]
) -> int | None:
    try:
        return int(value)
    except ValueError:
        errors.append(f"{filename}: inteiro inválido na linha {line}: {field}")
        return None


def _parse_float(
    value: str, filename: str, field: str, line: int, errors: list[str]
) -> float | None:
    try:
        number = float(value)
    except ValueError:
        errors.append(f"{filename}: número inválido na linha {line}: {field}")
        return None
    if not math.isfinite(number):
        errors.append(f"{filename}: número não finito na linha {line}: {field}")
        return None
    return number


def _parse_date(
    value: str, filename: str, field: str, line: int, errors: list[str]
) -> date | None:
    if not re.fullmatch(r"\d{8}", value):
        errors.append(f"{filename}: data inválida na linha {line}: {field}")
        return None
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError:
        errors.append(f"{filename}: data inválida na linha {line}: {field}")
        return None


def _parse_time(
    value: str, filename: str, field: str, line: int, errors: list[str]
) -> int | None:
    if not _TIME_PATTERN.fullmatch(value):
        errors.append(f"{filename}: horário inválido na linha {line}: {field}")
        return None
    hours, minutes, seconds = (int(part) for part in value.split(":"))
    if minutes > 59 or seconds > 59 or hours > 99:
        errors.append(f"{filename}: horário inválido na linha {line}: {field}")
        return None
    return hours * 3600 + minutes * 60 + seconds


def _validate_tables(tables: dict[str, list[dict[str, str]]]) -> list[str]:
    errors: list[str] = []

    agency_rows = tables["agency.txt"]
    route_rows = tables["routes.txt"]
    stop_rows = tables["stops.txt"]
    trip_rows = tables["trips.txt"]
    stop_time_rows = tables["stop_times.txt"]
    calendar_rows = tables["calendar.txt"]

    agency_ids = _unique_ids("agency.txt", agency_rows, "agency_id", errors)
    for line, row in enumerate(agency_rows, start=2):
        _required(row, "agency_name", "agency.txt", line, errors)
        url = _required(row, "agency_url", "agency.txt", line, errors)
        timezone = _required(row, "agency_timezone", "agency.txt", line, errors)
        if url:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"agency.txt: URL inválida na linha {line}: agency_url")
        if timezone:
            try:
                ZoneInfo(timezone)
            except (ZoneInfoNotFoundError, ValueError):
                errors.append(f"agency.txt: fuso horário desconhecido na linha {line}")

    route_ids = _unique_ids("routes.txt", route_rows, "route_id", errors)
    for line, row in enumerate(route_rows, start=2):
        agency_id = _required(row, "agency_id", "routes.txt", line, errors)
        route_type_text = _required(row, "route_type", "routes.txt", line, errors)
        if agency_id and agency_id not in agency_ids:
            errors.append(f"routes.txt: agency_id sem referência na linha {line}")
        if route_type_text:
            route_type = _parse_int(route_type_text, "routes.txt", "route_type", line, errors)
            # ponytail: cobre apenas enum base 0-12; modos estendidos ficam fora do MVP.
            if route_type is not None and not 0 <= route_type <= 12:
                errors.append(f"routes.txt: route_type fora do enum base na linha {line}")
        if not _clean(row, "route_short_name") and not _clean(row, "route_long_name"):
            errors.append(f"routes.txt: nome curto ou longo obrigatório na linha {line}")

    stop_ids = _unique_ids("stops.txt", stop_rows, "stop_id", errors)
    for line, row in enumerate(stop_rows, start=2):
        _required(row, "stop_name", "stops.txt", line, errors)
        latitude_text = _required(row, "stop_lat", "stops.txt", line, errors)
        longitude_text = _required(row, "stop_lon", "stops.txt", line, errors)
        latitude = (
            _parse_float(latitude_text, "stops.txt", "stop_lat", line, errors)
            if latitude_text
            else None
        )
        longitude = (
            _parse_float(longitude_text, "stops.txt", "stop_lon", line, errors)
            if longitude_text
            else None
        )
        if latitude is not None and not -90 <= latitude <= 90:
            errors.append(f"stops.txt: latitude fora do limite na linha {line}")
        if longitude is not None and not -180 <= longitude <= 180:
            errors.append(f"stops.txt: longitude fora do limite na linha {line}")

    trip_ids = _unique_ids("trips.txt", trip_rows, "trip_id", errors)
    service_ids = _unique_ids("calendar.txt", calendar_rows, "service_id", errors)
    for line, row in enumerate(trip_rows, start=2):
        route_id = _required(row, "route_id", "trips.txt", line, errors)
        service_id = _required(row, "service_id", "trips.txt", line, errors)
        if route_id and route_id not in route_ids:
            errors.append(f"trips.txt: route_id sem referência na linha {line}")
        if service_id and service_id not in service_ids:
            errors.append(f"trips.txt: service_id sem referência na linha {line}")

    for line, row in enumerate(calendar_rows, start=2):
        for weekday in WEEKDAYS:
            value = _required(row, weekday, "calendar.txt", line, errors)
            if value:
                parsed = _parse_int(value, "calendar.txt", weekday, line, errors)
                if parsed is not None and parsed not in {0, 1}:
                    errors.append(f"calendar.txt: valor de dia inválido na linha {line}")
        start_text = _required(row, "start_date", "calendar.txt", line, errors)
        end_text = _required(row, "end_date", "calendar.txt", line, errors)
        start = (
            _parse_date(start_text, "calendar.txt", "start_date", line, errors)
            if start_text
            else None
        )
        end = (
            _parse_date(end_text, "calendar.txt", "end_date", line, errors)
            if end_text
            else None
        )
        if start is not None and end is not None and end < start:
            errors.append(f"calendar.txt: end_date anterior a start_date na linha {line}")

    stop_times_by_trip: dict[str, list[int]] = {}
    seen_stop_sequences: set[tuple[str, int]] = set()
    for line, row in enumerate(stop_time_rows, start=2):
        trip_id = _required(row, "trip_id", "stop_times.txt", line, errors)
        arrival_text = _required(row, "arrival_time", "stop_times.txt", line, errors)
        departure_text = _required(row, "departure_time", "stop_times.txt", line, errors)
        stop_id = _required(row, "stop_id", "stop_times.txt", line, errors)
        sequence_text = _required(row, "stop_sequence", "stop_times.txt", line, errors)

        if trip_id and trip_id not in trip_ids:
            errors.append(f"stop_times.txt: trip_id sem referência na linha {line}")
        if stop_id and stop_id not in stop_ids:
            errors.append(f"stop_times.txt: stop_id sem referência na linha {line}")

        arrival = (
            _parse_time(arrival_text, "stop_times.txt", "arrival_time", line, errors)
            if arrival_text
            else None
        )
        departure = (
            _parse_time(departure_text, "stop_times.txt", "departure_time", line, errors)
            if departure_text
            else None
        )
        sequence = (
            _parse_int(sequence_text, "stop_times.txt", "stop_sequence", line, errors)
            if sequence_text
            else None
        )
        if sequence is not None:
            if sequence < 1:
                errors.append(f"stop_times.txt: stop_sequence deve ser positiva na linha {line}")
            elif trip_id:
                pair = (trip_id, sequence)
                if pair in seen_stop_sequences:
                    errors.append(f"stop_times.txt: stop_sequence duplicada na linha {line}")
                seen_stop_sequences.add(pair)
                stop_times_by_trip.setdefault(trip_id, []).append(sequence)
        if arrival is not None and departure is not None and arrival > departure:
            errors.append(f"stop_times.txt: chegada posterior à partida na linha {line}")

    for trip_id in trip_ids:
        sequences = stop_times_by_trip.get(trip_id, [])
        if not sequences:
            errors.append("trips.txt: viagem sem stop_times")
        elif sequences != sorted(sequences):
            errors.append("stop_times.txt: stop_sequence fora de ordem")

    if not service_ids:
        errors.append("calendar.txt: nenhum service_id válido")

    return errors


def validate_feed(feed_dir: str | Path) -> ValidationResult:
    """Valida diretório GTFS local sem rede, escrita ou inferência operacional."""

    root = Path(feed_dir)
    try:
        if not root.exists():
            return ValidationResult("no_result", ("diretório do feed não encontrado",))
        if not root.is_dir():
            return ValidationResult("unsupported", ("entrada não é um diretório GTFS",))
    except PermissionError:
        return ValidationResult("blocked", ("acesso ao diretório bloqueado",))
    except OSError:
        return ValidationResult("blocked", ("não foi possível acessar o diretório",))

    tables: dict[str, list[dict[str, str]]] = {}
    try:
        for filename, columns in REQUIRED_TABLES.items():
            tables[filename] = _read_table(root, filename, columns)
    except _FeedIssue as issue:
        return ValidationResult(issue.status, (str(issue),))

    errors = _validate_tables(tables)
    if errors:
        return ValidationResult("unsupported", tuple(errors))
    return ValidationResult("ok", checks=CHECKS)
