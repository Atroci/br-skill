"""Adapter de descoberta de vagas no Brasil (lookup, read-only).

Contrato traduzido/adaptado de `santifer/career-ops` (MIT — ver
`references/carreira-scanner-br.md` para atribuição e escopo completos). Este
módulo não é uma cópia do JavaScript upstream: é uma reimplementação em Python
do mesmo padrão (provider = função pura de parse + função opcional de fetch
com allowlist de host), restrita às fontes brasileiras verificadas nesta
rodada e ao contrato de falhas já usado em `adapters/gtfs_static/`.

Escopo desta versão
--------------------
- Capacidade: somente `lookup`. Nenhuma função aqui envia candidatura,
  autentica, paga, assina ou grava em serviço externo.
- `parse_*`: funções puras, sem rede, testadas com fixtures sintéticas em
  `fixtures/`. Seguras para rodar em qualquer ambiente, inclusive CI.
- `fetch_*` / `discover_*`: fazem requisição HTTP real (somente
  `urllib.request` da biblioteca padrão) contra a fonte pública já
  verificada. Não são chamadas pelos testes automatizados; exigem invocação
  explícita (linha de comando ou chamada direta) porque dependem de rede e da
  política vigente de robots.txt/ToS da fonte no momento do uso — reabra
  `references/carreira-scanner-br.md` antes de automatizar uma chamada
  recorrente.
- Fontes com robots.txt que bloqueiam crawler de IA nomeado (ex.: ClaudeBot,
  GPTBot, anthropic-ai) ou que restringem o caminho consultado (ex.: rota
  `/api/` fora de `/api/docs` e `/api/mcp`) não recebem função `fetch_*` aqui,
  mesmo quando o formato de dado já foi confirmado. Ver a tabela de catálogo
  na referência para o estado de cada fonte.

Falhas tipadas
--------------
Mesmo vocabulário do restante do pacote: `ok`, `no_result`, `stale`,
`blocked`, `auth_required`, `manual_review`, `unsupported`.
"""

from __future__ import annotations

import datetime
import html as _html_module
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlparse

STATUSES = (
    "ok",
    "no_result",
    "stale",
    "blocked",
    "auth_required",
    "manual_review",
    "unsupported",
)

DEFAULT_USER_AGENT = "br-skill-vagas-br/0.1 (+leitura publica, read-only, sem login)"
DEFAULT_TIMEOUT_S = 10


# ---------------------------------------------------------------------------
# Forma normalizada do Job (Center) — traduzida de providers/_types.js
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Job:
    """Vaga normalizada — unidade comum entre todas as fontes.

    Espelha o `Job` de career-ops (`providers/_types.js`): `title` e `url`
    são obrigatórios; o resto pode ficar vazio quando a fonte não expõe o
    dado no nível de listagem. `extra` carrega campos específicos da fonte
    (ex.: `jobBenefits`, `employmentType`) sem forçá-los no contrato comum.
    """

    title: str
    url: str
    company: str = ""
    location: str = ""
    description: str = ""
    posted_at_ms: int | None = None
    source_id: str = ""
    trust_score: int | None = None
    trust_flags: tuple[str, ...] = ()
    trust_level: str | None = None
    extra: dict[str, object] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "url": self.url,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "posted_at_ms": self.posted_at_ms,
            "source_id": self.source_id,
            "trust_score": self.trust_score,
            "trust_flags": list(self.trust_flags),
            "trust_level": self.trust_level,
            "extra": self.extra,
        }


@dataclass(frozen=True)
class SourceResult:
    """Envelope mínimo de um fetch/parse — não substitui o envelope completo
    de `references/envelope-evidencia.md`; é a unidade que uma skill/relatório
    deve embrulhar nesse envelope antes de apresentar ao usuário."""

    status: str
    source_id: str
    source_url: str
    jobs: tuple[Job, ...] = ()
    limitations: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "source_id": self.source_id,
            "source_url": self.source_url,
            "jobs": [job.as_dict() for job in self.jobs],
            "limitations": list(self.limitations),
        }


# ---------------------------------------------------------------------------
# Guarda de host (SSRF) — traduzida de assertGreenhouseUrl/assertLeverUrl
# ---------------------------------------------------------------------------


class UntrustedHostError(ValueError):
    """URL fora do allowlist de host ou fora de HTTPS."""


def assert_allowed_url(url: str, *, allowed_suffixes: tuple[str, ...]) -> str:
    """Confere HTTPS e hostname antes de qualquer fetch.

    `allowed_suffixes` aceita host exato (`"programathor.com.br"`) ou
    subdomínio (`"gupy.io"` cobre `ambev.gupy.io`). Mesma disciplina de
    `greenhouse.mjs`/`lever.mjs`: HTTPS obrigatório, host validado antes da
    chamada, e o chamador deve desligar redirecionamento automático.
    """

    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise UntrustedHostError(f"URL precisa usar HTTPS: {url!r}")
    host = (parsed.hostname or "").lower()
    if not host:
        raise UntrustedHostError(f"URL sem hostname: {url!r}")
    for suffix in allowed_suffixes:
        suffix = suffix.lower()
        if host == suffix or host.endswith("." + suffix):
            return url
    raise UntrustedHostError(
        f"host não autorizado {host!r}; permitido: {', '.join(allowed_suffixes)}"
    )


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Recusa redirecionamento automático (equivalente a `redirect: 'error'`)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise urllib.error.HTTPError(newurl, code, "redirecionamento recusado (SSRF guard)", headers, fp)


def _http_get(url: str, *, timeout: int = DEFAULT_TIMEOUT_S) -> str:
    """GET read-only mínimo, sem seguir redirecionamento, sem autenticação."""

    opener = urllib.request.build_opener(_NoRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html,application/json"})
    with opener.open(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


# ---------------------------------------------------------------------------
# Validador de confiança — traduzido de providers/_trust-validator.mjs
# ---------------------------------------------------------------------------

DEFAULT_SUSPICIOUS_DOMAINS: tuple[str, ...] = (
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "forms.gle",
    "goo.gl",
    "shorturl.at",
    "rebrand.ly",
    "cutt.ly",
    "is.gd",
)

# Allowlist-base traduzida de career-ops (ATS internacionais) + fontes
# brasileiras confirmadas nesta rodada (ver o catálogo na referência).
DEFAULT_ATS_ALLOWLIST: tuple[str, ...] = (
    "greenhouse.io",
    "ashbyhq.com",
    "lever.co",
    "workday.com",
    "myworkdayjobs.com",
    "smartrecruiters.com",
    "jobvite.com",
    "recruitee.com",
    "workable.com",
    "icims.com",
    "taleo.net",
    "applytojob.com",
    "breezy.hr",
    "jazz.co",
    "bamboohr.com",
    "teamtailor.com",
    # fontes brasileiras confirmadas em references/carreira-scanner-br.md
    "gupy.io",
    "solides.com.br",
    "empregare.com",
    "programathor.com.br",
    "catho.com.br",
    "vagas.com.br",
    "infojobs.com.br",
)

_TRUST_PENALTIES = {
    "invalid_url": 50,
    "missing_apply_url": 40,
    "suspicious_domain": 25,
    "company_domain_mismatch": 15,
}


@dataclass(frozen=True)
class TrustResult:
    score: int
    flags: tuple[str, ...]
    level: str


def classify_trust_level(score: int) -> str:
    if score >= 90:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def _validate_url_shape(url: str) -> tuple[bool, str | None]:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False, "invalid_url"
    return True, None


def _matches_domain_list(hostname: str, domains: tuple[str, ...]) -> bool:
    hostname = hostname.lower()
    for domain in domains:
        domain = domain.lower()
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def _company_matches_hostname(company: str, hostname: str) -> bool:
    if not company or not hostname:
        return True
    normalized = re.sub(r"[^a-z0-9 ]", "", company.lower()).strip()
    if not normalized:
        return True
    slug = normalized.replace(" ", "")
    if slug and slug in hostname:
        return True
    for word in normalized.split():
        if len(word) >= 3 and word in hostname:
            return True
    return False


def build_trust_validator(
    *,
    suspicious_domains: tuple[str, ...] = DEFAULT_SUSPICIOUS_DOMAINS,
    ats_allowlist: tuple[str, ...] = DEFAULT_ATS_ALLOWLIST,
):
    """Fábrica de validador — mesma forma de `buildTrustValidator` upstream.

    Retorna uma função `job -> TrustResult`. Nunca descarta uma vaga: só
    sinaliza. Score 0-100; heurística, não prova de legitimidade (ver
    "Legitimidade da publicação" em `references/carreira-br.md`)."""

    def validate(job: Job) -> TrustResult:
        flags: list[str] = []
        score = 100

        url = (job.url or "").strip()
        if not url:
            flags.append("missing_apply_url")
            score -= _TRUST_PENALTIES["missing_apply_url"]
            clamped = max(0, score)
            return TrustResult(clamped, tuple(flags), classify_trust_level(clamped))

        ok, flag = _validate_url_shape(url)
        if not ok:
            flags.append(flag or "invalid_url")
            score -= _TRUST_PENALTIES["invalid_url"]
            clamped = max(0, score)
            return TrustResult(clamped, tuple(flags), classify_trust_level(clamped))

        hostname = (urlparse(url).hostname or "").lower()

        if _matches_domain_list(hostname, suspicious_domains):
            flags.append("suspicious_domain")
            score -= _TRUST_PENALTIES["suspicious_domain"]

        company = (job.company or "").strip()
        if company and not _matches_domain_list(hostname, ats_allowlist):
            if not _company_matches_hostname(company, hostname):
                flags.append("company_domain_mismatch")
                score -= _TRUST_PENALTIES["company_domain_mismatch"]

        score = max(0, min(100, score))
        return TrustResult(score, tuple(flags), classify_trust_level(score))

    return validate


def apply_trust_validator(jobs: list[Job], validator=None) -> list[Job]:
    """Aplica o validador a cada vaga e retorna novas instâncias marcadas."""

    validate = validator or build_trust_validator()
    marked: list[Job] = []
    for job in jobs:
        result = validate(job)
        marked.append(
            Job(
                title=job.title,
                url=job.url,
                company=job.company,
                location=job.location,
                description=job.description,
                posted_at_ms=job.posted_at_ms,
                source_id=job.source_id,
                trust_score=result.score,
                trust_flags=result.flags,
                trust_level=result.level,
                extra=job.extra,
            )
        )
    return marked


# ---------------------------------------------------------------------------
# Helpers de texto
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    """Remoção mínima de marcação HTML — suficiente para leitura, não é um
    parser HTML completo. Preserva quebras de parágrafo como espaço simples."""

    if not text:
        return ""
    unescaped = _html_module.unescape(text)
    return re.sub(r"\s+", " ", _TAG_RE.sub(" ", unescaped)).strip()


def _parse_iso_to_epoch_ms(value: object) -> int | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        parsed = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return int(parsed.timestamp() * 1000)


# ---------------------------------------------------------------------------
# Gupy — página de carreira por empresa (<empresa>.gupy.io)
#
# Confirmado nesta rodada: a página SSR (Next.js) embute a lista completa de
# vagas em <script id="__NEXT_DATA__">, sem exigir JS, login ou paginação
# separada. Evidência e limitações completas em
# references/carreira-scanner-br.md#gupy.
# ---------------------------------------------------------------------------

GUPY_ALLOWED_SUFFIXES = ("gupy.io",)


def parse_gupy_career_page(html_text: str) -> list[Job]:
    """Extrai vagas do JSON embutido de uma página `<empresa>.gupy.io`.

    Função pura: recebe o HTML já obtido (por `fetch_gupy_career_page` ou por
    qualquer outro meio autorizado) e devolve `Job`s. Não faz rede.
    """

    match = re.search(
        r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.S
    )
    if not match:
        return []
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    page_props = (data.get("props") or {}).get("pageProps") or {}
    career_page = page_props.get("careerPage") or {}
    subdomain = page_props.get("subdomain") or career_page.get("subdomain") or ""
    company = career_page.get("publicationName") or career_page.get("name") or ""
    raw_jobs = page_props.get("jobs")
    if not isinstance(raw_jobs, list):
        return []

    jobs: list[Job] = []
    for raw in raw_jobs:
        if not isinstance(raw, dict):
            continue
        title = str(raw.get("title") or "").strip()
        job_id = raw.get("id")
        if not title or job_id is None or not subdomain:
            continue
        url = f"https://{subdomain}.gupy.io/job/{job_id}"

        workplace = raw.get("workplace") or {}
        address = workplace.get("address") or {}
        location_parts = [
            address.get("city"),
            address.get("stateShortName") or address.get("state"),
            address.get("country"),
        ]
        location = ", ".join(part for part in location_parts if part)
        workplace_type = workplace.get("workplaceType")
        if workplace_type and workplace_type != "on-site":
            location = f"{location} ({workplace_type})" if location else str(workplace_type)

        jobs.append(
            Job(
                title=title,
                url=url,
                company=str(company),
                location=location,
                description="",
                posted_at_ms=None,
                source_id="gupy",
                extra={
                    "department": raw.get("department") or "",
                    "vacancy_type": raw.get("type") or "",
                    "district": address.get("district") or "",
                },
            )
        )
    return jobs


def fetch_gupy_career_page(subdomain: str, *, timeout: int = DEFAULT_TIMEOUT_S) -> str:
    """Busca real (rede) da página pública `<subdomain>.gupy.io/`.

    Não chamada pelos testes. `subdomain` deve ser só o rótulo da empresa
    (ex.: `"ambev"`), nunca uma URL completa fornecida por terceiro sem
    revalidação."""

    slug = re.sub(r"[^a-z0-9-]", "", subdomain.strip().lower())
    if not slug:
        raise ValueError("subdomain vazio ou inválido")
    url = assert_allowed_url(f"https://{slug}.gupy.io/", allowed_suffixes=GUPY_ALLOWED_SUFFIXES)
    return _http_get(url, timeout=timeout)


def discover_gupy_company(subdomain: str, *, timeout: int = DEFAULT_TIMEOUT_S) -> SourceResult:
    """Pipeline completo (rede + parse) para uma empresa no Gupy."""

    slug = subdomain.strip().lower()
    source_url = f"https://{slug}.gupy.io/"
    try:
        html_text = fetch_gupy_career_page(slug, timeout=timeout)
    except UntrustedHostError as exc:
        return SourceResult("blocked", "gupy", source_url, limitations=(str(exc),))
    except urllib.error.HTTPError as exc:
        status = "auth_required" if exc.code in (401, 403) else "blocked"
        return SourceResult(status, "gupy", source_url, limitations=(f"HTTP {exc.code}",))
    except (urllib.error.URLError, TimeoutError) as exc:
        return SourceResult("blocked", "gupy", source_url, limitations=(str(exc),))

    jobs = parse_gupy_career_page(html_text)
    if not jobs:
        return SourceResult(
            "no_result",
            "gupy",
            source_url,
            limitations=("página acessível, mas sem vagas no JSON embutido; confirme o subdomínio",),
        )
    jobs = apply_trust_validator(jobs)
    return SourceResult("ok", "gupy", source_url, jobs=tuple(jobs))


# ---------------------------------------------------------------------------
# JobPosting (schema.org) — parser genérico
#
# Confirmado em programathor.com.br e vagas.com.br (páginas individuais).
# Uso por fonte é condicionado ao estado de robots.txt/ToS de cada uma — ver
# a tabela de catálogo. Este parser não decide se é permitido buscar uma URL;
# quem decide isso é `assert_allowed_url` + o catálogo de robôs por fonte.
# ---------------------------------------------------------------------------

_LDJSON_RE = re.compile(
    r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I
)


def _iter_ldjson_blocks(html_text: str):
    for block in _LDJSON_RE.findall(html_text):
        try:
            parsed = json.loads(block, strict=False)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    yield item
        elif isinstance(parsed, dict):
            yield parsed


def parse_jobposting_jsonld(html_text: str, *, source_url: str = "", source_id: str = "jsonld_jobposting") -> Job | None:
    """Extrai um `Job` do primeiro bloco `schema.org/JobPosting` encontrado.

    Padrão amplo no Brasil (usado para o recurso "Google for Jobs"), não
    específico de uma fonte. `source_url` deve ser a URL canônica da página
    lida; o schema JobPosting nem sempre repete a própria URL."""

    job_posting = None
    for item in _iter_ldjson_blocks(html_text):
        if item.get("@type") == "JobPosting":
            job_posting = item
            break
    if job_posting is None:
        return None

    title = str(job_posting.get("title") or "").strip()
    url = str(job_posting.get("url") or source_url or "").strip()
    if not title or not url:
        return None

    hiring_org = job_posting.get("hiringOrganization")
    company = ""
    if isinstance(hiring_org, dict):
        company = str(hiring_org.get("name") or "").strip()
    if not company:
        identifier = job_posting.get("identifier")
        if isinstance(identifier, dict):
            company = str(identifier.get("name") or "").strip()

    location = ""
    job_location = job_posting.get("jobLocation")
    locations = job_location if isinstance(job_location, list) else [job_location]
    location_parts: list[str] = []
    for loc in locations:
        if not isinstance(loc, dict):
            continue
        addr = loc.get("address")
        if not isinstance(addr, dict):
            continue
        parts = [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")]
        joined = ", ".join(str(p) for p in parts if p and str(p).strip() and str(p).strip() != "-")
        if joined:
            location_parts.append(joined)
    location = " | ".join(dict.fromkeys(location_parts))  # dedup preservando ordem

    description = _strip_html(str(job_posting.get("description") or ""))
    posted_at_ms = _parse_iso_to_epoch_ms(job_posting.get("datePosted"))

    extra: dict[str, object] = {}
    if job_posting.get("employmentType"):
        extra["employment_type"] = job_posting.get("employmentType")
    if job_posting.get("validThrough"):
        extra["valid_through"] = job_posting.get("validThrough")
    if job_posting.get("jobBenefits"):
        extra["job_benefits"] = job_posting.get("jobBenefits")

    return Job(
        title=title,
        url=url,
        company=company,
        location=location,
        description=description,
        posted_at_ms=posted_at_ms,
        source_id=source_id,
        extra=extra,
    )


# ---------------------------------------------------------------------------
# Programathor — quadro de vagas com links simples em HTML + JobPosting
#
# Confirmado nesta rodada: robots.txt geral permissivo (só /admin/, /user/,
# /users/, /company/ vedados), sem bloqueio nomeado a crawler de IA, listagem
# em HTML puro (sem exigir JS) e schema JobPosting em cada vaga individual.
# ---------------------------------------------------------------------------

PROGRAMATHOR_ALLOWED_SUFFIXES = ("programathor.com.br",)
PROGRAMATHOR_LISTING_URL = "https://programathor.com.br/jobs"
_PROGRAMATHOR_LINK_RE = re.compile(r'href="(/jobs/[a-zA-Z0-9\-]+)"')


def list_programathor_job_urls(listing_html: str) -> list[str]:
    """Extrai URLs absolutas de vaga a partir do HTML da listagem `/jobs`."""

    seen: dict[str, None] = {}
    for path in _PROGRAMATHOR_LINK_RE.findall(listing_html):
        seen.setdefault(f"https://programathor.com.br{path}", None)
    return list(seen.keys())


def fetch_programathor_url(url: str, *, timeout: int = DEFAULT_TIMEOUT_S) -> str:
    checked = assert_allowed_url(url, allowed_suffixes=PROGRAMATHOR_ALLOWED_SUFFIXES)
    return _http_get(checked, timeout=timeout)


def discover_programathor_jobs(
    *, max_jobs: int = 5, timeout: int = DEFAULT_TIMEOUT_S
) -> SourceResult:
    """Pipeline completo (rede + parse) para o quadro do Programathor.

    `max_jobs` limita quantas páginas de vaga são lidas por execução — bom
    vizinho de rede pública, não um limite de cobertura real do quadro."""

    try:
        listing_html = fetch_programathor_url(PROGRAMATHOR_LISTING_URL, timeout=timeout)
    except UntrustedHostError as exc:
        return SourceResult("blocked", "programathor", PROGRAMATHOR_LISTING_URL, limitations=(str(exc),))
    except urllib.error.HTTPError as exc:
        status = "auth_required" if exc.code in (401, 403) else "blocked"
        return SourceResult(status, "programathor", PROGRAMATHOR_LISTING_URL, limitations=(f"HTTP {exc.code}",))
    except (urllib.error.URLError, TimeoutError) as exc:
        return SourceResult("blocked", "programathor", PROGRAMATHOR_LISTING_URL, limitations=(str(exc),))

    urls = list_programathor_job_urls(listing_html)[:max_jobs]
    if not urls:
        return SourceResult(
            "no_result", "programathor", PROGRAMATHOR_LISTING_URL,
            limitations=("listagem acessível, sem link de vaga reconhecido no HTML atual",),
        )

    jobs: list[Job] = []
    limitations: list[str] = []
    for job_url in urls:
        try:
            job_html = fetch_programathor_url(job_url, timeout=timeout)
        except (UntrustedHostError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            limitations.append(f"{job_url}: {exc}")
            continue
        job = parse_jobposting_jsonld(job_html, source_url=job_url, source_id="programathor")
        if job is not None:
            jobs.append(job)
        else:
            limitations.append(f"{job_url}: sem bloco JobPosting reconhecível")

    if not jobs:
        return SourceResult(
            "no_result", "programathor", PROGRAMATHOR_LISTING_URL, limitations=tuple(limitations) or ("nenhuma vaga extraída",)
        )
    jobs = apply_trust_validator(jobs)
    return SourceResult("ok", "programathor", PROGRAMATHOR_LISTING_URL, jobs=tuple(jobs), limitations=tuple(limitations))


# ---------------------------------------------------------------------------
# Empregare — API pública documentada (parse-only nesta rodada)
#
# `GET https://empregare.com/api/{culture}/vagas/buscar-novo` é uma API
# pública sem login (confirmado nesta rodada via
# https://empregare.com/openapi/v1.json). Não há função `fetch_*` aqui: o
# robots.txt do site restringe automação em `/api/` a `/api/mcp` e
# `/api/docs`, então o caminho recomendado é o servidor MCP oficial
# (`https://www.empregare.com/api/mcp`), não uma chamada direta recorrente a
# este endpoint. O parser abaixo serve para normalizar uma resposta já obtida
# por um canal autorizado (ex.: MCP, ou revisão humana pontual).
# ---------------------------------------------------------------------------


def parse_empregare_response(payload: dict) -> list[Job]:
    """Normaliza o corpo JSON documentado de `buscar-novo` em `Job`s."""

    model = payload.get("model") if isinstance(payload, dict) else None
    dados = (model or {}).get("dados") if isinstance(model, dict) else None
    if not isinstance(dados, list):
        return []

    jobs: list[Job] = []
    for raw in dados:
        if not isinstance(raw, dict):
            continue
        title = str(raw.get("titulo") or "").strip()
        rel_url = raw.get("url")
        job_id = raw.get("id")
        if not title:
            continue
        if rel_url:
            path = str(rel_url).lstrip("/")
        elif job_id is not None:
            path = f"v{job_id}"
        else:
            continue
        url = f"https://www.empregare.com/{path}"

        cidades = raw.get("cidades")
        location = ", ".join(str(c) for c in cidades) if isinstance(cidades, list) else ""
        remoto_texto = raw.get("trabalhoRemotoTexto")
        if remoto_texto:
            location = f"{location} ({remoto_texto})" if location else str(remoto_texto)

        timestamp = raw.get("timestamp")
        posted_at_ms = None
        if isinstance(timestamp, (int, float)) and timestamp > 0:
            posted_at_ms = int(timestamp) * 1000

        extra = {
            "nivel": raw.get("nivel") or "",
            "salario": raw.get("salario") or "",
            "status": raw.get("status") or "",
            "data_cadastro": raw.get("dataCadastro") or "",
            "data_expiracao": raw.get("dataExpiracao") or "",
            "aviso_timestamp": (
                "timestamp/data podem refletir republicação, não a publicação "
                "original; ver data_cadastro"
            ),
        }

        jobs.append(
            Job(
                title=title,
                url=url,
                company=str(raw.get("empresa") or ""),
                location=location,
                description=_strip_html(str(raw.get("chamada") or "")),
                posted_at_ms=posted_at_ms,
                source_id="empregare",
                extra=extra,
            )
        )
    return jobs


# ---------------------------------------------------------------------------
# CLI manual — não é chamado pelos testes; uso interativo/operador.
# ---------------------------------------------------------------------------


def _cli(argv: list[str]) -> int:
    if len(argv) < 2:
        print("uso: python3 adapter.py gupy <subdominio> | python3 adapter.py programathor [max_jobs]")
        return 2
    command = argv[1]
    if command == "gupy":
        if len(argv) < 3:
            print("uso: python3 adapter.py gupy <subdominio>")
            return 2
        result = discover_gupy_company(argv[2])
    elif command == "programathor":
        max_jobs = int(argv[2]) if len(argv) > 2 else 5
        result = discover_programathor_jobs(max_jobs=max_jobs)
    else:
        print(f"comando desconhecido: {command!r}")
        return 2
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
    return 0 if result.status == "ok" else 1


if __name__ == "__main__":
    import sys

    raise SystemExit(_cli(sys.argv))
