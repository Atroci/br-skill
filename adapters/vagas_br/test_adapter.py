"""Check executável e focado do adapter `vagas_br` — só parsers e heurísticas
locais. Nenhum teste aqui faz requisição de rede (as funções `fetch_*` /
`discover_*` exigem invocação manual e explícita; ver README.md)."""

from __future__ import annotations

import json
from pathlib import Path

from adapter import (
    DEFAULT_ATS_ALLOWLIST,
    GUPY_ALLOWED_SUFFIXES,
    PROGRAMATHOR_ALLOWED_SUFFIXES,
    Job,
    UntrustedHostError,
    apply_trust_validator,
    assert_allowed_url,
    build_trust_validator,
    classify_trust_level,
    list_programathor_job_urls,
    parse_empregare_response,
    parse_gupy_career_page,
    parse_jobposting_jsonld,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_gupy_parser() -> None:
    html = (FIXTURES / "gupy_career_page_sintetica.html").read_text(encoding="utf-8")
    jobs = parse_gupy_career_page(html)
    assert len(jobs) == 2, f"esperado 2 vagas válidas, obtido {len(jobs)}"

    titles = {job.title for job in jobs}
    assert "Analista de Exemplo Pleno" in titles
    assert "Analista de Exemplo Junior (Afirmativa PCD)" in titles
    assert "" not in titles, "vaga sem título não pode ser emitida"

    pleno = next(job for job in jobs if job.title == "Analista de Exemplo Pleno")
    assert pleno.url == "https://empresa-exemplo-br.gupy.io/job/900001"
    assert pleno.company == "Empresa Exemplo BR"
    assert pleno.location == "Sao Paulo, SP, Brasil"

    junior = next(job for job in jobs if "Junior" in job.title)
    assert junior.location.endswith("(hybrid)"), "workplaceType != on-site deve aparecer na location"

    # HTML sem __NEXT_DATA__ -> lista vazia, nunca erro.
    assert parse_gupy_career_page("<html><body>sem next data</body></html>") == []
    # __NEXT_DATA__ presente mas sem pageProps.jobs -> lista vazia.
    empty = '<script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{}}}</script>'
    assert parse_gupy_career_page(empty) == []


def test_jobposting_jsonld_parser() -> None:
    html = (FIXTURES / "jobposting_jsonld_sintetica.html").read_text(encoding="utf-8")
    job = parse_jobposting_jsonld(
        html, source_url="https://programathor.example.invalid/jobs/88221-dev-automacao"
    )
    assert job is not None, "deve tolerar caractere de controle bruto dentro do JSON-LD"
    assert job.title == "Desenvolvedor(a) de Automacao de Testes"
    assert job.company == "Empresa Exemplo Tech"
    assert job.location == "Curitiba, PR, BR"
    assert "Requisitos:" in job.description
    assert "<p>" not in job.description, "descrição deve vir sem marcação HTML"
    assert job.extra["employment_type"] == "FULL_TIME"
    assert job.extra["job_benefits"].startswith("Vale-refeicao")
    assert job.posted_at_ms is not None

    # Página só com BreadcrumbList (sem JobPosting) -> None, nunca erro nem vaga inventada.
    sem_jobposting = (FIXTURES / "sem_jobposting_sintetica.html").read_text(encoding="utf-8")
    assert parse_jobposting_jsonld(sem_jobposting, source_url="https://x.invalid/y") is None

    # JobPosting sem título e sem URL utilizável -> None (contrato exige os dois).
    sem_titulo = (
        '<script type="application/ld+json">'
        '{"@type": "JobPosting", "title": "", "hiringOrganization": {"name": "X"}}'
        "</script>"
    )
    assert parse_jobposting_jsonld(sem_titulo, source_url="") is None


def test_programathor_link_extraction() -> None:
    listing_html = (
        '<a href="/jobs/1-vaga-a">Vaga A</a>'
        '<a href="/jobs/2-vaga-b">Vaga B</a>'
        '<a href="/jobs/1-vaga-a">Vaga A (duplicada)</a>'
        '<a href="/empresas/x">não é vaga</a>'
    )
    urls = list_programathor_job_urls(listing_html)
    assert urls == [
        "https://programathor.com.br/jobs/1-vaga-a",
        "https://programathor.com.br/jobs/2-vaga-b",
    ], urls


def test_empregare_parser() -> None:
    payload = json.loads((FIXTURES / "empregare_resposta_sintetica.json").read_text(encoding="utf-8"))
    jobs = parse_empregare_response(payload)
    assert len(jobs) == 1, "registro sem título/URL utilizável deve ser descartado"
    job = jobs[0]
    assert job.url == "https://www.empregare.com/vaga-analista-de-exemplo_500001"
    assert job.location == "Brasilia, DF, BR (Hibrido)"
    assert job.posted_at_ms == 1785000000 * 1000
    assert "data_cadastro" in job.extra

    assert parse_empregare_response({}) == []
    assert parse_empregare_response({"model": {"dados": "não é lista"}}) == []


def test_ssrf_guard() -> None:
    try:
        assert_allowed_url("http://empresa.gupy.io/", allowed_suffixes=GUPY_ALLOWED_SUFFIXES)
        raise AssertionError("deveria recusar HTTP")
    except UntrustedHostError:
        pass

    try:
        assert_allowed_url("https://gupy.io.evil.example/", allowed_suffixes=GUPY_ALLOWED_SUFFIXES)
        raise AssertionError("deveria recusar host fora do allowlist")
    except UntrustedHostError:
        pass

    assert assert_allowed_url("https://empresa.gupy.io/job/1", allowed_suffixes=GUPY_ALLOWED_SUFFIXES)
    assert assert_allowed_url(
        "https://programathor.com.br/jobs/1-x", allowed_suffixes=PROGRAMATHOR_ALLOWED_SUFFIXES
    )
    try:
        assert_allowed_url("https://sub.programathor.com.br.evil.example/", allowed_suffixes=PROGRAMATHOR_ALLOWED_SUFFIXES)
        raise AssertionError("sufixo deve casar host inteiro, não substring solta")
    except UntrustedHostError:
        pass


def test_trust_validator() -> None:
    assert classify_trust_level(100) == "high"
    assert classify_trust_level(75) == "medium"
    assert classify_trust_level(10) == "low"

    validator = build_trust_validator()

    missing_url = validator(Job(title="Vaga", url="", company="Empresa Exemplo"))
    assert missing_url.flags == ("missing_apply_url",)
    assert missing_url.level == "medium"

    invalid_url = validator(Job(title="Vaga", url="não é url", company="Empresa Exemplo"))
    assert invalid_url.flags == ("invalid_url",)

    suspicious = validator(Job(title="Vaga", url="https://bit.ly/abcd", company="Empresa Exemplo"))
    assert "suspicious_domain" in suspicious.flags

    ats_hosted = validator(
        Job(title="Vaga", url="https://empresa.gupy.io/job/1", company="Qualquer Nome Ltda")
    )
    assert ats_hosted.flags == (), "host em DEFAULT_ATS_ALLOWLIST não deve levar mismatch"
    assert ats_hosted.score == 100

    mismatch = validator(
        Job(title="Vaga", url="https://outrodominio.example.invalid/vaga/1", company="Zeta Consultoria Ltda")
    )
    assert "company_domain_mismatch" in mismatch.flags

    assert "gupy.io" in DEFAULT_ATS_ALLOWLIST
    assert "programathor.com.br" in DEFAULT_ATS_ALLOWLIST


def test_apply_trust_validator_preserves_job_fields() -> None:
    html = (FIXTURES / "gupy_career_page_sintetica.html").read_text(encoding="utf-8")
    jobs = parse_gupy_career_page(html)
    marked = apply_trust_validator(jobs)
    assert len(marked) == len(jobs)
    for original, updated in zip(jobs, marked):
        assert updated.title == original.title
        assert updated.url == original.url
        assert updated.trust_level in ("high", "medium", "low")
        assert updated.trust_score is not None


def main() -> None:
    test_gupy_parser()
    test_jobposting_jsonld_parser()
    test_programathor_link_extraction()
    test_empregare_parser()
    test_ssrf_guard()
    test_trust_validator()
    test_apply_trust_validator_preserves_job_fields()
    print("ok - parsers, validador de confiança e guarda de host (SSRF) testados com fixtures sintéticas")


if __name__ == "__main__":
    main()
