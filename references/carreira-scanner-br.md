# Carreira BR — scanner de fontes (adaptado de career-ops)

## Escopo e origem

Este arquivo é o companheiro de [`carreira-br.md`](carreira-br.md) para a
parte que a versão anterior deixou fora de escopo: descoberta em lote a
partir de fontes brasileiras específicas, com um catálogo verificado e um
adapter mínimo (`adapters/vagas_br/`). Continua `lookup`, read-only, sem
candidatura, sem CV, sem dashboard e sem armazenamento de dado pessoal.

Fonte de arquitetura: [`santifer/career-ops`](https://github.com/santifer/career-ops)
(licença MIT, copyright Santiago Fernández de Valderrama), consultado nesta
rodada em `2026-08-08`. `references/ecossistema-brasil.md` já registrava esse
repositório como referência de método/produto a preservar ("pipeline de
oportunidades, revisão humana e adaptação a sites brasileiros") e a rejeitar
("candidatura automática, scraping sem termos ou exposição de PII"); este
arquivo é a operacionalização dessa entrada, autorizada nesta rodada como o
caso concreto que faltava para sair de `INPUT_INCOMPLETE`.

Não é cópia do código JavaScript upstream nem do texto de `AGENTS.md`,
`MANIFESTO.md` ou `docs/SUPPORTED_JOB_BOARDS.md` de career-ops. É uma
tradução de arquitetura e conceito para o contrato já existente em br-skill
(Center/Moat, envelope de evidência, estados tipados), mais um catálogo de
fontes brasileiras verificado por leitura direta nesta rodada — career-ops
não mapeia nenhuma fonte brasileira nativa (seu catálogo cobre ATS
internacionais como Greenhouse/Lever/Ashby/Workday e agregadores
US/EU/APAC/LatAm-hispânico; nenhuma linha de
[`docs/SUPPORTED_JOB_BOARDS.md`](https://github.com/santifer/career-ops/blob/main/docs/SUPPORTED_JOB_BOARDS.md)
cobre Brasil). Onde o código é reimplementado (validador de confiança, guarda
de host), o cabeçalho do módulo Python cita a origem; a licença MIT permite a
adaptação com atribuição, que este arquivo e `adapters/vagas_br/README.md`
cumprem.

## Relação com `carreira-br.md`

`carreira-br.md` continua a fonte de verdade para o **relatório** de uma
oportunidade (blocos FACT/INFERENCE/ASSUMPTION/UNKNOWN, fit, legitimidade da
publicação, contradições). Este arquivo cobre a **descoberta**: onde
procurar, com que método, e com que confiança de acesso. Uma vaga encontrada
via `adapters/vagas_br/` ainda precisa passar pelo fluxo de
`carreira-br.md` antes de virar recomendação para a pessoa usuária — a saída
do adapter é entrada para esse relatório, não um substituto dele.

O veredito de escopo anterior ("scanner, providers, dashboard, SQLite, batch,
índice derivado e submit ficam fora do escopo até haver fonte autorizada,
caso concreto e teste aprovado") não foi apagado nem contradito: ele
permanece verdadeiro para dashboard, SQLite, batch, índice derivado e submit,
que continuam fora. Para "scanner" e "providers" especificamente, o caso
concreto, a fonte autorizada e o teste aprovado (fixture + `test_adapter.py`
local) agora existem e ficam registrados aqui, com data.

## O que foi absorvido (Center comum, traduzido)

| Conceito em career-ops | Arquivo upstream | Tradução em br-skill |
|---|---|---|
| Contrato de provider (`id`, `detect()`, `fetch()` → `Job[]`) | `providers/_types.js`, `providers/README.md` | `parse_<fonte>(bruto) -> list[Job]` (puro) + `fetch_<fonte>(...)`/`discover_<fonte>(...)` (rede) em `adapters/vagas_br/adapter.py` |
| Forma normalizada `Job` | `providers/_types.js` | `dataclass Job` (`title`, `url`, `company`, `location`, `description`, `posted_at_ms`, `source_id`, `trust_*`, `extra`) |
| Guarda de host contra SSRF (`assertGreenhouseUrl`, `assertLeverUrl`) | `providers/greenhouse.mjs`, `providers/lever.mjs` | `assert_allowed_url()` — HTTPS obrigatório, allowlist de sufixo de host, sem redirecionamento automático |
| Validador de confiança (`_trust-validator.mjs`) | `providers/_trust-validator.mjs` | `build_trust_validator()`/`apply_trust_validator()` — mesmas 4 heurísticas (URL inválida, URL ausente, domínio de encurtador, empresa×host) |
| 4 níveis de descoberta (`modes/scan.md`) | `modes/scan.md` | 4 níveis adaptados abaixo, sem Playwright/MCP tool específico embutido no contrato |
| Política de indexação de fontes | `CONTRIBUTING.md` §Source Indexing Policy | §"Política de inclusão de fonte" abaixo |
| Log de evidência por fonte | `docs/SOURCE_INDEXING_LOG.md` | Notas por fonte abaixo, mesmo espírito (o que foi checado e como) |
| Conteúdo web é dado não confiável, nunca instrução | `AGENTS.md` §Untrusted External Content | já era regra de `SKILL.md`/`carreira-br.md`; sem mudança, só confirmação de alinhamento |
| Nunca enviar candidatura sem revisão humana | `AGENTS.md` §Ethical Use, `MANIFESTO.md` | já era regra do envelope comum (`submit` exige aprovação pontual); sem mudança |

### 4 níveis de descoberta (adaptado)

O upstream descreve 4 níveis (`modes/scan.md`): parser local, Playwright
direto, API/feed, WebSearch. br-skill precisa continuar neutro de runtime
(OpenCode, Codex, Gemini CLI, Google Antigravity nem sempre têm navegador ou
MCP equivalente), então a tradução troca "Playwright" por "capacidade
opcional do runtime":

1. **Nível 0 — parser local (mais barato):** função `parse_*` deste adapter
   sobre um HTML/JSON já obtido. Zero rede no momento do parse.
2. **Nível 1 — leitura assistida quando o runtime tiver navegador/computer-use:**
   único nível que depende de capacidade opcional (`references/plataformas.md`
   §Capacidades opcionais); usado para fontes SPA sem dado embutido (ex.:
   Sólides Vagas/ex-Kenoby nesta rodada). Se o runtime não tiver essa
   capacidade, o resultado é `manual_review`, não uma tentativa forçada.
3. **Nível 2 — API/feed público sem login (alvo preferencial):** o que
   `fetch_gupy_career_page`/`discover_gupy_company` e
   `fetch_programathor_url`/`discover_programathor_jobs` fazem. Zero-token no
   sentido de career-ops (sem custo de LLM), mais barato e mais confiável que
   Nível 1 quando existe.
4. **Nível 3 — busca ampla (`site:` no WebSearch disponível):** descoberta de
   empresas/fontes novas ainda não catalogadas aqui; resultado sempre tratado
   como desatualizado até confirmação direta na página (mesma cautela que
   `carreira-br.md` já aplica a "resultado de busca e catálogo são pistas").

Diferença deliberada do upstream: career-ops executa os 4 níveis dentro de
uma única sessão de scan orientada a `portals.yml`. Aqui não existe scan
agendado nem arquivo de configuração pessoal — cada nível é uma decisão
tomada por vez, dentro do fluxo de `carreira-br.md` ou de
[`skills/br-vagas-scanner/SKILL.md`](../skills/br-vagas-scanner/SKILL.md).

### O que não foi absorvido (non-goals explícitos)

Igual ao filtro que `roldao-method.md` e `ecossistema-brasil.md` já aplicam a
outros upstreams: não portar CLI (`cops`), os 115 scripts `.mjs` no diretório
raiz do upstream (106 sem contar `*.test.mjs`; contagem direta em
`2026-08-08`, não o número aproximado do próprio `ARCHITECTURE.md` deles),
`portals.yml`/perfil pessoal, geração de CV/PDF/LaTeX/carta de apresentação,
scripts de negociação salarial, banco de histórias de entrevista,
`interview-prep`, dashboard Go, SQLite, tracker de pipeline pessoal
(`data/applications.md` e equivalentes), sistema de plugins, updater,
integração Gmail/e-mail, preenchimento de formulário de candidatura
(`apply.md`) ou qualquer submissão. Esses cobrem um produto de gestão de
busca de emprego pessoal; br-skill cobre descoberta e avaliação read-only
compartilhável entre runtimes, sem estado pessoal persistido no pacote
público. Se um caso concreto pedir um desses itens no futuro, ele reabre este
arquivo e passa pelo mesmo gate (fonte autorizada, fixture, teste, revisão).

## Center vs Moat aplicado aqui

- **Center** (já genérico, reaproveitável por qualquer domínio de br-skill):
  `Job`, `SourceResult`, `assert_allowed_url`, o validador de confiança
  genérico, os 7 estados tipados.
- **Moat** (específico do Brasil/carreira, fica neste arquivo e em
  `adapters/vagas_br/`, não sobe para um "core" compartilhado ainda): o
  catálogo abaixo, o parser do JSON embutido do Gupy, a extração de link do
  Programathor, o schema de resposta do Empregare. Só migra para um núcleo
  comum se um segundo adapter (fora do domínio carreira) precisar do mesmo
  comportamento sem exceção local — regra já registrada em
  [`arquitetura.md`](arquitetura.md) e [`adapters.md`](adapters.md).

## Metodologia de verificação usada nesta rodada (P0)

Para cada fonte candidata: reabrir `robots.txt` na íntegra (não só os
primeiros bytes), checar diretivas nomeadas para bots de IA além da regra
geral `User-agent: *`, checar `sitemap.xml` quando presente, buscar dado
estruturado (JSON embutido tipo `__NEXT_DATA__`, ou `schema.org/JobPosting`
em JSON-LD) numa página pública de exemplo, sem login, sem CAPTCHA, sem
cookie de sessão. Sem chamada autenticada, sem download em massa, sem
raspagem de múltiplas páginas além do necessário para confirmar o formato.

**Por que checar diretiva de IA nomeada além da regra geral.** Em 2026,
vários sites publicam um bloco `Content-Signal` (proposta
[contentsignals.org](https://contentsignals.org)) e/ou `Disallow` nomeado
para `ClaudeBot`, `GPTBot`, `anthropic-ai`, `CCBot`, `PerplexityBot` etc.,
separado da regra geral `User-agent: *`. Um agente de IA que só lê a regra
geral pode concluir "permitido" quando o operador do site expressou o
oposto para esse tipo de cliente especificamente. Como esta skill roda sobre
modelos de linguagem (incluindo, nesta rodada, um modelo Claude via Prime
Agent), o critério aplicado foi: **a regra nomeada mais específica vale**,
mesmo quando o `User-Agent` HTTP efetivamente enviado é genérico. Isso não é
um requisito do padrão `robots.txt` (que resolve por especificidade de
`User-agent` declarado na requisição, não por "quem realmente opera o
cliente"), é uma decisão de conduta desta skill, mais conservadora que o
mínimo tecnicamente exigido — consistente com "prefira fonte oficial
primária, acesso público e coleta read-only" e com a Política de Indexação
de Fontes traduzida abaixo.

Isto **não** é uma auditoria jurídica de Termos de Uso. `terms_url` e
`license` continuam `UNKNOWN` por fonte até revisão humana dedicada, como já
exige [`adapters.md`](adapters.md) e [`mcp-brasil.md`](mcp-brasil.md).
Timestamp desta rodada de verificação: `2026-08-08` (consultas feitas entre
~15:30 e ~16:10 UTC).

## Catálogo de fontes brasileiras

Evidência observada em `2026-08-08`. Nenhuma linha desta tabela é cobertura,
disponibilidade ou recomendação de uso automático — é o estado observado
numa leitura pontual, sujeito a mudar. Antes de reusar uma fonte marcada
`ok`/implementada, reabra o `robots.txt` atual: os operadores mudam essas
regras sem aviso, como o próprio achado abaixo demonstra.

| Fonte | Papel | Tipo técnico | `robots.txt` geral | `robots.txt` — bots de IA nomeados | Estado nesta rodada |
|---|---|---|---|---|---|
| [Gupy](https://www.gupy.io/) — página por empresa (`<empresa>.gupy.io`) | `official_producer` (por empresa contratante) | JSON embutido em `__NEXT_DATA__` (SSR, sem paginação) | subdomínio de empresa não publica `robots.txt` próprio (cai no shell do app); `portal.gupy.io` permite tudo; `www.gupy.io` permite geral | `www.gupy.io` permite `ClaudeBot`/`GPTBot`/`PerplexityBot`/`Bytespider`/`Applebot-Extended` explicitamente | **Implementado** — `parse_gupy_career_page`/`discover_gupy_company` |
| [Programathor](https://programathor.com.br/) | `aggregator` | `schema.org/JobPosting` (JSON-LD) na página de cada vaga + links HTML simples em `/jobs` (sem exigir JS) | permissivo — só `/admin/`, `/user/`, `/users/`, `/company/` vedados; `sitemap.xml` publicado | nenhum bloqueio nomeado encontrado | **Implementado** — `parse_jobposting_jsonld`/`discover_programathor_jobs` |
| [Empregare](https://empregare.com/) (marca do produto observada nesta rodada; relação histórica com "99jobs" **não verificada** nesta sessão, tratar como `UNKNOWN`) | `aggregator` | API pública documentada: `GET /api/{culture}/vagas/buscar-novo`, OpenAPI em `/openapi/v1.json`, servidor MCP em `/api/mcp` | `Disallow: /api/` geral, com exceção explícita só para `/api/mcp` e `/api/docs` — a busca em si **não** está no Allow nomeado | `Content-Signal: ai-input=yes, ai-train=no` para `*`; nenhum bloqueio nomeado adicional | **Parser apenas** (`parse_empregare_response`); sem `fetch_*` — use o MCP oficial, não uma chamada direta recorrente |
| [Vagas.com.br](https://www.vagas.com.br/) | `aggregator` | `schema.org/JobPosting` confirmado em página individual (`/vagas/vNNNNNNN/...`), links simples na listagem | `Disallow: /api/`, `/vagas/pesquisas`, `/v1/`, entre outros | **Bloqueio nomeado total** (`Disallow: /`) para `ClaudeBot`, `Claude-Web`, `anthropic-ai`, `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`, `Google-Extended`, `CCBot`, `PerplexityBot`, `Bytespider`, `Amazonbot`, entre outros | **Não implementado** — formato de dado documentado só como referência; ver §Metodologia acima |
| [Catho](https://www.catho.com.br/) | `aggregator` | não confirmado (página individual amostrada não trouxe JSON-LD); descoberta em massa possível via `sitemap-index.xml` → `sitemap_vagas_N.xml` | `Disallow: /buscar/vagas/` (busca/listagem); páginas `/vagas-emprego/...` majoritariamente permitidas; `Disallow: /` só para `LinkedInBot` | permite explicitamente `GPTBot`/`ChatGPT-User`/`Claude-Web`/`anthropic-ai`/`PerplexityBot`/`CCBot`/`Googlebot`/`bingbot` | `manual_review` — descoberta via sitemap é permitida pelo robots.txt; parser de página de detalhe não construído nesta rodada |
| [InfoJobs Brasil](https://www.infojobs.com.br/) | `aggregator` | não verificado nesta rodada | `Disallow: /detailvacancy.aspx` (rota de detalhe da vaga) entre outras | nenhum bloqueio nomeado adicional (herda a regra geral) | `manual_review`/`blocked` para página de detalhe — o próprio robots.txt veda o caminho que interessa |
| [Indeed Brasil](https://br.indeed.com/) | `aggregator` | não verificado nesta rodada | geral relativamente permissivo (`Allow: /` com exceções de rastreamento); bots de IA nomeados recebem as mesmas regras da busca comum, não um bloqueio total | sem bloqueio nomeado total | `manual_review` — Termos de Uso **não foram relidos nesta sessão** (só `robots.txt`); career-ops também não lista provider para Indeed |
| [LinkedIn Vagas](https://www.linkedin.com/) | `aggregator` | N/A | proíbe **qualquer** automação sem permissão expressa do LinkedIn, por texto explícito no próprio arquivo | bloqueio nomeado total (`ClaudeBot`, `GPTBot`, `anthropic-ai`, `PerplexityBot`, `CCBot`, ...) | **Excluído — nunca implementar.** Mesma regra que career-ops aplica (`CONTRIBUTING.md`: "PRs that scrape platforms prohibiting automated access (LinkedIn, etc.). We actively reject these") |
| [Sólides Vagas](https://vagas.solides.com.br/) (sucessor observado de Kenoby — `kenoby.com` não resolve mais nesta rodada) | `aggregator`/ATS | Next.js renderizado no cliente; nenhum JSON de vagas embutido no HTML inicial encontrado nesta rodada | permissivo — `Allow: /empresa/*/vaga` explícito, `sitemap.xml` publicado | nenhum bloqueio nomeado encontrado | `manual_review` — exige Nível 1 (leitura assistida) ou engenharia reversa adicional do bundle JS, não feita nesta rodada |
| [Trampos.co](https://trampos.co/) | `aggregator` (startups/tech) | não confirmado — nenhum link de vaga em HTML puro na listagem amostrada (suspeita de SPA) | permissivo (`Disallow:` vazio + `/admin/`); `sitemap.xml` publicado | nenhum bloqueio nomeado encontrado | `manual_review` — estrutura de dado não confirmada |
| [Revelo](https://www.revelo.com.br/) | `aggregator` (tech) | não confirmado — caminho de listagem testado (`/vagas`) devolveu 404 | permissivo (`Disallow:` vazio); `sitemap.xml` publicado | nenhum bloqueio nomeado encontrado | `manual_review` — URL de listagem correta não confirmada |
| [GeekHunter](https://www.geekhunter.com.br/) (redireciona para `geekhunter.com`) | `aggregator` (tech) | não confirmado | domínio `.com.br` veda `/jobs`, `/pt/jobs`, `/vagas-*`; o domínio efetivo após redirecionamento é outro TLD, não reverificado | grupo geral com `Content-Signal: ai-input=yes` para `*`, mas o caminho de vaga já está vedado pela regra geral | `manual_review` — caminho de vaga vedado no domínio `.com.br`; `.com` não reverificado nesta rodada |
| SINE / Emprega Brasil (Ministério do Trabalho e Emprego) | `official_producer` (serviço público de intermediação de emprego) | histórico: portal dedicado do governo | `empregabrasil.mte.gov.br` falhou o handshake TLS nesta rodada (estado técnico observado, não confirmação de descontinuação); `www.gov.br/trabalho-e-emprego/pt-br` está no ar, mas a navegação lida nesta rodada não expôs um link direto de intermediação de emprego para quem busca vaga (só Seguro-Desemprego e Qualificação Profissional na seção "Trabalhador") | não avaliado | `UNKNOWN`/`stale` — **prioridade máxima para revalidação humana**; é a fonte mais alinhada com "prefira fonte oficial primária" do pacote, mas não pôde ser confirmada como operacional nesta sessão |
| Empregos.com.br, Trabalha Brasil | `catalog` | não reavaliado nesta rodada | não reavaliado nesta rodada | não reavaliado | mantém o estado "a verificar" já registrado em [`carreira-br.md`](carreira-br.md#portais-brasileiros-a-verificar) |
| CIEE, Nube | `catalog` | fora de escopo aqui (estágio/aprendizagem) | — | — | ver [`estagio-cursos-br.md`](estagio-cursos-br.md#fontes-para-estágio-e-aprendizagem) — não duplicado aqui |

## Notas por fonte

### Gupy

Página `https://<empresa>.gupy.io/` é renderizada no servidor (Next.js) com
a lista completa de vagas embutida em
`<script id="__NEXT_DATA__">…props.pageProps.jobs`. Campos observados por
vaga: `id`, `title`, `type`, `department`, `workplace.address` (`country`,
`stateShortName`, `state`, `city`, `district`), `workplace.workplaceType`
(`on-site`/`hybrid`/outros), `quickApply`. Não há campo de data de publicação
no payload de listagem — `posted_at_ms` fica `None` por vaga, o que é
esperado, não um bug. URL de detalhe observada como válida (HTTP 200):
`https://<empresa>.gupy.io/job/<id>`. Amostra usada para verificação: uma
empresa pública grande com página Gupy ativa, lida em `2026-08-08` (nome
omitido deste documento por não ser necessário à regra; qualquer subdomínio
`*.gupy.io` real serve para reproduzir o achado). `portal.gupy.io` (busca
agregada entre empresas na Gupy) existe e tem `robots.txt` permissivo, mas
não expôs endpoint de busca óbvio sem execução de JavaScript nesta rodada —
não implementado.

### Programathor

Listagem em `https://programathor.com.br/jobs` traz links `<a href="/jobs/ID-slug">`
em HTML puro. Cada página de vaga carrega `schema.org/JobPosting` em
JSON-LD com `title`, `description` (HTML), `identifier`, `datePosted`,
`validThrough`, `employmentType`, `hiringOrganization.name`,
`jobLocation.address`. Achado relevante para quem for portar este parser:
pelo menos uma página amostrada trazia um caractere de controle bruto (quebra
de linha literal) dentro de uma string JSON — `json.loads(..., strict=False)`
é necessário; `strict=True` (padrão) falha nessa página. O parser genérico
`parse_jobposting_jsonld` já usa `strict=False`.

### Empregare

`https://empregare.com/api/docs` serve documentação Scalar/OpenAPI
("Empregare - API de Vagas"); o spec em `/openapi/v1.json` descreve
`GET /api/{culture}/vagas/buscar-novo` como "Busca vagas ativas no jobboard
publico da Empregare. Nao requer autenticacao." — chamada de teste real
(parâmetros `Query`/`ItensPagina`) devolveu HTTP 200 com o formato descrito
em `parse_empregare_response`. Apesar disso, `robots.txt` restringe
automação em `/api/` à documentação e ao MCP (`/api/mcp`, referenciado no
próprio HTML de `/api/docs`), não ao endpoint de busca em si. Por isso este
adapter só normaliza uma resposta já obtida — não faz a chamada
automaticamente. Campo `timestamp`/`data` do payload parece refletir a
data de exibição (bateu com `data: "sex., 17/julho"` num teste real), que
pode ser republicação, não a publicação original (`dataCadastro` é campo
separado); o parser preserva ambos em `extra` com um aviso, em vez de
apresentar uma data só como certa.

### Vagas.com.br (documentado, não implementado)

Registrado aqui porque a descoberta do formato de dado (JSON-LD válido,
campos ricos incluindo `jobBenefits`, que mapeia direto para o campo
"Benefícios" de `carreira-br.md`) tem valor para quem revisar este catálogo
no futuro — mas o bloqueio nomeado a `ClaudeBot`/`GPTBot`/`anthropic-ai`/
`PerplexityBot`/`CCBot`/`Google-Extended` (ver tabela) significa que esta
skill, rodando sobre um modelo de IA, não deve buscar este site
automaticamente, independentemente do `User-Agent` HTTP enviado. Se uma
pessoa quiser usar este site manualmente (abrir a página no próprio
navegador, copiar o HTML), `parse_jobposting_jsonld` já normaliza o
resultado — é o mesmo parser do Programathor, porque o formato é o mesmo
padrão `schema.org`.

### SINE / Emprega Brasil

É a fonte que melhor cumpriria "prefira fonte oficial primária" deste
pacote — serviço público federal de intermediação de emprego. Não foi
possível confirmar endpoint ativo nesta rodada: `empregabrasil.mte.gov.br`
(URL historicamente citada para o serviço) devolveu falha de handshake TLS a
partir do ambiente usado para esta verificação; isso é um estado técnico
observado num único momento e ambiente, não uma conclusão sobre o serviço
estar fora do ar para o público em geral. O portal institucional do
Ministério (`www.gov.br/trabalho-e-emprego/pt-br`) está acessível, mas a
navegação lida nesta rodada não trouxe um link direto de busca de vaga na
seção voltada ao trabalhador. Fica como item de maior prioridade para uma
revalidação humana dedicada — não como fonte implementada.

## Política de inclusão de fonte (adaptada)

Tradução da Source Indexing Policy de career-ops (`CONTRIBUTING.md`),
restrita ao que já é regra em br-skill:

1. **O que entra no catálogo:** só fonte cujo anúncio seja atribuível a um
   empregador identificável e gratuita para quem busca vaga ler e se
   candidatar. Fonte que cobra da pessoa candidata para ver ou se candidatar
   a uma vaga não entra.
2. **URL canônica:** cada entrada aponta para o caminho mais curto até o
   empregador que a fonte expõe (URL do ATS/página de carreira, quando
   disponível).
3. **robots.txt e ToS decidem, não conveniência técnica.** Uma fonte
   tecnicamente alcançável sem login não está automaticamente autorizada —
   ver §Metodologia acima e a coluna "bots de IA nomeados" da tabela.
4. **Catalogar não é endosso, e não promete cobertura.** Nenhuma linha da
   tabela é uma afirmação de que a fonte é completa, atual ou representativa
   do mercado brasileiro.
5. **A camada de agregação fica no pacote, não na fonte.** Cada `parse_*`
   lê só a sua própria fonte; comparação entre fontes, ranking e
   deduplicação entre fontes ficam fora deste adapter (não existem nesta
   rodada).

## Contrato de saída (Job → envelope)

Uma vaga normalizada (`Job`, ver `adapters/vagas_br/adapter.py`) preenche o
envelope comum de [`envelope-evidencia.md`](envelope-evidencia.md) assim:

```yaml
capability: lookup
status: ok | no_result | stale | blocked | auth_required | manual_review | unsupported
request:
  intent: "descoberta de vagas"
  jurisdiction: "BR"
  inputs: { fonte: gupy | programathor | empregare | outro, parametro: "subdominio ou URL" }
source:
  provider: "gupy | programathor | empregare | ..."
  source_url: "URL exata consultada"
  source_role: official_producer | aggregator
  retrieved_at: "ISO 8601 com fuso"
  access_mode: public
  terms_url: unknown
result:
  facts:
    - title: "..."
      url: "..."
      company: "..."
      location: "..."
      trust_score: 0-100
      trust_flags: []
      extra: {}
  confidence: medium
limitations:
  - "trust_score é heurística, não prova de legitimidade"
  - "posted_at_ms pode estar ausente; nunca inferido"
handoff:
  required: false
```

Este envelope alimenta o relatório de `carreira-br.md`, não o substitui —
cada vaga listada aqui ainda precisa da avaliação de Fit e de Legitimidade da
publicação daquele contrato antes de virar recomendação.

## Falhas tipadas — nota sobre bloqueio por robô de IA

`blocked` já cobre "a fonte ou caminho foi impedido" (`envelope-evidencia.md`).
Quando o motivo específico é um `robots.txt` que nomeia bots de IA, registre
a limitação por extenso (ex.: `"robots.txt bloqueia ClaudeBot/GPTBot por
nome; Content-Signal permite apenas indexação de busca padrão"`) em vez de
só `blocked` genérico — mantém rastreável por que a fonte não foi tentada,
igual ao padrão já usado para `auth_required`/`manual_review` no resto do
pacote.

## Roadmap por gates (mesmo modelo de `ecossistema-brasil.md`)

- **P0 (concluído nesta rodada, para as fontes listadas):** reabertura de
  `robots.txt` geral e nomeado, checagem de formato de dado, sem
  autenticação nem download em massa.
- **P1 (concluído nesta rodada, para Gupy e Programathor):** contrato
  mínimo, fixture sintética redigida, `test_adapter.py` local passando sem
  rede.
- **P2 (pendente):** revisão Orca read-only do contrato antes de qualquer
  recomendação de uso recorrente/agendado. Promoção de lógica ao Center só
  se um segundo domínio (fora de carreira) precisar do mesmo comportamento.
- **P3 (pendente, gate separado):** publicação, commit, push, PR, merge —
  não cobertos por este arquivo.

## Referências

- Upstream: [`santifer/career-ops`](https://github.com/santifer/career-ops)
  — `AGENTS.md`, `ARCHITECTURE.md`, `MANIFESTO.md`, `CONTRIBUTING.md`,
  `providers/README.md`, `providers/_types.js`, `providers/_trust-validator.mjs`,
  `providers/greenhouse.mjs`, `providers/lever.mjs`,
  `docs/SUPPORTED_JOB_BOARDS.md`, `docs/SOURCE_INDEXING_LOG.md`,
  `modes/scan.md`, `modes/discover.md` (consultados nesta rodada,
  `2026-08-08`; licença MIT).
- [`carreira-br.md`](carreira-br.md) — contrato de relatório e envelope que
  esta descoberta alimenta.
- [`adapters.md`](adapters.md), [`arquitetura.md`](arquitetura.md),
  [`roldao-method.md`](roldao-method.md) — contrato de adapter, Center/Moat,
  fases de promoção aplicadas aqui.
- [`ecossistema-brasil.md`](ecossistema-brasil.md) — registro anterior de
  career-ops como referência de método/produto.
- [`envelope-evidencia.md`](envelope-evidencia.md) — contrato comum de saída.
- [`mcp-brasil.md`](mcp-brasil.md) — por que o MCP do Empregare é tratado
  como canal de descoberta, não como autoridade.
- [`adapters/vagas_br/README.md`](../adapters/vagas_br/README.md) — escopo
  executável, estados e limites do código.
