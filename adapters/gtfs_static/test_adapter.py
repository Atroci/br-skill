"""Check executável focado do adapter GTFS sintético."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from adapter import validate_feed


FIXTURE = Path(__file__).parent / "fixtures" / "synthetic_feed"


def main() -> None:
    valid = validate_feed(FIXTURE)
    assert valid.status == "ok", valid.as_dict()
    assert not valid.errors
    assert "referências entre tabelas sem órfãos" in valid.checks
    assert "stop_times com sequência e horários coerentes" in valid.checks

    missing = validate_feed(FIXTURE / "não-existe")
    assert missing.status == "no_result", missing.as_dict()

    with tempfile.TemporaryDirectory() as temporary:
        broken = Path(temporary) / "broken"
        shutil.copytree(FIXTURE, broken)
        stop_times = broken / "stop_times.txt"
        stop_times.write_text(
            stop_times.read_text(encoding="utf-8").replace(
                "stop-sintetica-b", "stop-ausente", 1
            ),
            encoding="utf-8",
        )
        invalid = validate_feed(broken)
        assert invalid.status == "unsupported", invalid.as_dict()
        assert any("stop_id sem referência" in error for error in invalid.errors)

    print("ok - fixture GTFS sintética e falha de FK validadas")


if __name__ == "__main__":
    main()
