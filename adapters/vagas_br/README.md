# Adapter Vagas BR

Validator e normalizador `lookup`, read-only, para descoberta de vagas em
fontes brasileiras públicas e sem login. Traduzido/adaptado da arquitetura de
providers de [`santifer/career-ops`](https://github.com/santifer/career-ops)
(MIT) para Python — não é uma cópia do código JavaScript upstream. Ver
[`references/carreira-scanner-br.md`](../../references/carreira-scanner-br.md)
para atribuição completa, metodologia de verificação e o catálogo de fontes.

## Fonte e jurisdição

Este adapter cobre três fontes brasileiras verificadas nesta rodada, cada
uma com seu próprio estado de acesso — não existe uma única "fonte" única
como em `adapters/gtfs_static/`:

| Fonte | `source.role` | `access` | Função de rede nesta rodada |
|---|---|---|---|
| Gupy (`<empresa>.gupy.io`) | `official_producer` (a empresa contratante publica sua própria vaga; a Gupy hospeda) | `public` | `fetch_gupy_career_page` / `discover_gupy_company` — implementada |
| Programathor (`programathor.com.br`) | `aggregator` | `public` | `fetch_programathor_url` / `discover_programathor_jobs` — implementada |
| Empregare (`empregare.com`) | `aggregator` | `public`, mas `robots.txt` restringe automação em `/api/` a `/api/mcp` e `/api/docs` | somente `parse_empregare_response`; **sem** função `fetch_*` nesta rodada |

`accessed_at` de cada verificação, o texto de `robots.txt` observado e as
limitações completas ficam na referência, não neste README, para não haver
duas cópias divergentes da mesma evidência.

## Contrato

Entrada: HTML/JSON já obtido (para `parse_*`) ou um identificador simples —
subdomínio da empresa no caso do Gupy (para `fetch_*`/`discover_*`). Saída:
lista de `Job` (`title`, `url`, `company`, `location`, `description`,
`posted_at_ms`, `source_id`, `trust_score`/`trust_flags`/`trust_level`,
`extra`) envelopada em `SourceResult` (`status`, `source_id`, `source_url`,
`jobs`, `limitations`).

- `parse_gupy_career_page`, `parse_jobposting_jsonld` e
  `parse_empregare_response` são funções puras — sem rede, sem I/O, testadas
  com fixtures sintéticas em `fixtures/`.
- `fetch_gupy_career_page`, `fetch_programathor_url`, `discover_gupy_company`
  e `discover_programathor_jobs` fazem requisição HTTP real (só
  `urllib.request` da biblioteca padrão, sem dependência nova). Validam host
  e HTTPS antes de qualquer chamada (`assert_allowed_url`, mesma disciplina
  de `assertGreenhouseUrl`/`assertLeverUrl` do upstream) e recusam
  redirecionamento automático.
- `build_trust_validator`/`apply_trust_validator` — heurística de confiança
  traduzida de `providers/_trust-validator.mjs`: nunca descarta uma vaga, só
  sinaliza (`trust_score` 0–100, `trust_flags`, `trust_level`). Não é prova
  de legitimidade; ver "Legitimidade da publicação" em
  [`references/carreira-br.md`](../../references/carreira-br.md).

## O que este adapter não faz

Não envia candidatura, não autentica, não paga, não assina, não cria conta,
não grava em serviço externo e não roda em segundo plano. Não é um scanner
agendado: cada chamada é uma decisão explícita do operador ou do agente
supervisionado, nunca automática. Não tenta as fontes com robots.txt
bloqueando crawler de IA nomeado (ver o catálogo) nem as que exigem
JavaScript para revelar a vaga (ex.: Sólides Vagas/ex-Kenoby nesta rodada) —
essas ficam documentadas como `manual_review`, não implementadas.

## Estados

Mesmo vocabulário do restante do pacote:

- `ok`: rede OK (quando aplicável) e ao menos uma vaga válida extraída.
- `no_result`: fonte acessível, sem vaga aproveitável na resposta.
- `blocked`: HTTP de erro, rede indisponível, ou host fora do allowlist
  (`UntrustedHostError`).
- `auth_required`: resposta HTTP 401/403.
- `stale`, `manual_review`, `unsupported`: não emitidos pelo código — são
  estados que a skill/relatório que envolve este adapter deve aplicar ao
  cruzar o resultado com frescor, robots.txt e o catálogo de fontes.

## Limites

Cobre só as três fontes acima, cada uma com o alcance descrito na
referência (Gupy: uma empresa por chamada, sem paginação — a página traz a
lista inteira; Programathor: até `max_jobs` vagas por chamada, padrão 5, bom
vizinho de rede; Empregare: parser sem fetch). Não cobre Vagas.com.br, Catho,
InfoJobs, Indeed, LinkedIn, Trampos.co, Revelo, GeekHunter nem Sólides
Vagas/ex-Kenoby como funções de rede — essas ficam catalogadas com estado
observado (`manual_review`, `blocked` por robots de IA nomeado, ou
"estrutura não confirmada") na referência, não implementadas aqui. Não há
paginação genérica, não há cache, não há deduplicação entre fontes, não há
persistência local e não há verificação de vaga expirada (liveness) — quem
consumir a saída deve tratar `posted_at_ms`/`extra.data_expiracao` como
pistas, não como confirmação de vaga ainda aberta.

## Execução

Testes (sem rede, só fixtures sintéticas):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 adapters/vagas_br/test_adapter.py
```

Uso manual/interativo (rede real — revise a fonte, o robots.txt vigente e o
horário antes de rodar; nunca automatizar sem supervisão):

```bash
python3 adapters/vagas_br/adapter.py gupy <subdominio-da-empresa>
python3 adapters/vagas_br/adapter.py programathor 5
```

Uso programático:

```python
from adapter import discover_gupy_company, discover_programathor_jobs

resultado = discover_gupy_company("nome-da-empresa")
resultado2 = discover_programathor_jobs(max_jobs=5)
```
