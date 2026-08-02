# Ecossistema Brasil — mapa para Council

**Status:** `INPUT_INCOMPLETE` — mapa documental preparatório; não registra uma execução de painel.
**Data do mapa:** `2026-08-03` (`Europe/Lisbon`)
**Escopo:** somente repositórios explicitamente nomeados em [`AGENTS.md`](../AGENTS.md), [`SKILL.md`](../SKILL.md) e referências lidas neste repositório.
**Capacidade:** `lookup`/`prepare`, read-only. Não cria adapter, runtime, bridge, catálogo executável ou ação externa.

Este arquivo organiza papel, ganhos, lacunas, rejeições e próximos gates. `Council` aqui significa apoio à decisão sob incerteza: não é fonte, não cria evidência, não verifica URL, não confirma cobertura, licença, número ou capacidade e não autoriza commit, push, PR, merge, deploy ou submissão. A fonte de verdade continua sendo o contrato local e a fonte primária citada; `UNKNOWN` não significa “não existe”.

## Método e rótulos

- **FACT:** afirmação observada no contrato local ou reproduzida de uma referência citada.
- **INFERENCE:** leitura ou recomendação derivada dos `FACTs`; não é observação do repositório.
- **ASSUMPTION:** condição que precisa ser confirmada antes de promover uma decisão.
- **UNKNOWN:** informação ausente, bloqueada, contraditória ou não revalidada.
- **REVALIDAR:** a afirmação depende de upstream. A URL, a data abaixo e a limitação são ponte de rechecagem; não são prova atual. A data anterior a `2026-08-03` é a data registrada na referência local, não uma nova consulta.

Não há alegação de inventário completo do GitHub, do ecossistema brasileiro, dos feeds GTFS ou das capacidades dos projetos. URLs de órgãos, portais e padrões que não são repositórios ficam fora deste mapa.

## Inventário delimitado

| ID | Repositório nomeado | Classe no contrato | Decisão de escopo atual |
|---|---|---|---|
| R-001 | [`Atroci/br-skill`](https://github.com/Atroci/br-skill) | pacote pretendido | manter Markdown-first; existência do remoto ainda precisa de confirmação (`REVALIDAR`) |
| R-002 | [`NomaDamas/k-skill`](https://github.com/NomaDamas/k-skill) | referência upstream (`REVALIDAR`) | estudar somente por comparação; não copiar |
| R-003 | [`Mcp-Brasil/mcp-brasil`](https://github.com/Mcp-Brasil/mcp-brasil) | agregador/MCP independente (`REVALIDAR`) | usar como pista de descoberta, nunca como autoridade |
| R-004 | [`MobilityData/mobility-database-catalogs`](https://github.com/MobilityData/mobility-database-catalogs) | catálogo de dados GTFS (`REVALIDAR`) | usar como diretório; reabrir produtor e arquivo |
| R-005 | [`roldaobatista/roldao-method`](https://github.com/roldaobatista/roldao-method/tree/main) | referência de engenharia (`REVALIDAR`) | extrair contrato mínimo; não portar framework |
| R-006 | [`rodrigowindows/GTFS`](https://github.com/rodrigowindows/GTFS) | cópia comunitária de dado GTFS (`REVALIDAR`) | manter apenas como referência histórica a revalidar |
| R-007 | [`benaytms/urbs-gtfs`](https://github.com/benaytms/urbs-gtfs) | cópia comunitária de dado GTFS (`REVALIDAR`) | não tratar como produtor oficial |

O conjunto acima é o conjunto deste mapa, não uma afirmação de completude. Repositórios citados como fontes de dados não são automaticamente repositórios de software candidatos a integração.

## Fichas dos repositórios

### R-001 — `Atroci/br-skill`

- **Papel:** [F-001] **FACT:** o contrato local identifica `Atroci/br-skill` como repositório público pretendido e define `SKILL.md` e `references/` como fonte de verdade do pacote.
- **Ganho:** [I-001] **INFERENCE:** uma pasta portátil, referências relativas e validação local formam a menor unidade útil para os quatro runtimes documentados.
- **Lacuna:** [U-001] **UNKNOWN:** existência, visibilidade, branch protection, CI efetivo e estado do remoto não foram verificados nesta tarefa.
- **Rejeição:** [I-002] **INFERENCE:** não declarar publicação, cobertura, suporte de runtime ou release; não fazer push, PR, merge ou deploy como parte deste mapa.
- **Revalidação:** [R-001] URL `https://github.com/Atroci/br-skill`; acesso `2026-08-03` ao contrato local; limitação: a URL veio da documentação e o remoto não foi consultado.

### R-002 — `NomaDamas/k-skill`

- **Papel:** [F-002] **FACT — REVALIDAR:** [`AGENTS.md`](../AGENTS.md) o nomeia como upstream de pesquisa, não como fonte para copiar ou modificar.
- **Ganho:** [I-003] **INFERENCE — REVALIDAR:** pode servir somente para comparar padrões e limites já registrados na arquitetura brasileira.
- **Lacuna:** [U-002] **UNKNOWN — REVALIDAR:** existência/URL canônica, conteúdo atual, licença, dependências, compatibilidade e capacidade não foram estabelecidos pelas referências inspecionadas.
- **Rejeição:** [I-004] **INFERENCE — REVALIDAR:** rejeitar cópia de árvore, instruções, pipeline, runtime, hooks, claims de cobertura ou dependências antes de uma necessidade e um contrato aprovados.
- **Revalidação:** [R-002] URL proposta para checagem `https://github.com/NomaDamas/k-skill`; acesso `2026-08-03` ao identificador em `AGENTS.md`, sem consulta live; limitação: URL canônica e qualquer claim upstream permanecem `UNKNOWN`.

### R-003 — `Mcp-Brasil/mcp-brasil`

- **Papel:** [F-003] **FACT — REVALIDAR:** [`mcp-brasil.md`](mcp-brasil.md) o descreve como servidor independente que agrega APIs e datasets públicos brasileiros; o MCP não é órgão público nem autoridade do dado.
- **Ganho:** [I-005] **INFERENCE — REVALIDAR:** a organização de discovery, autenticação visível, masking, frescor e falhas pode orientar fichas de fonte, sem importar runtime.
- **Lacuna:** [U-003] **UNKNOWN — REVALIDAR:** cada fonte pode ter termos, licença, acesso, schema, frescor e risco próprios; a capacidade atual do upstream não foi rechecada nesta tarefa.
- **Rejeição:** [I-006] **INFERENCE — REVALIDAR:** não portar FastMCP, Python, Pydantic, DuckDB, Azure, datasets, crawler, registry, code mode, BM25/LLM recommender ou superfície de tools só por existir no upstream citado.
- **Revalidação:** [R-003] URL `https://github.com/Mcp-Brasil/mcp-brasil`; acesso registrado `2026-08-02` em `mcp-brasil.md`; limitação: leitura local não confirma README, endpoints, números, licença uniforme, cobertura ou disponibilidade atual.

### R-004 — `MobilityData/mobility-database-catalogs`

- **Papel:** [F-004] **FACT — REVALIDAR:** [`brasil-gtfs.md`](brasil-gtfs.md) usa o projeto como catálogo/diretório de registros GTFS localizados.
- **Ganho:** [I-007] **INFERENCE — REVALIDAR:** pode acelerar descoberta inicial de operador, feed e URL candidata antes da reabertura da fonte do produtor.
- **Lacuna:** [U-004] **UNKNOWN — REVALIDAR:** status, URL, validade, licença e escopo podem mudar; o snapshot local não é inventário nacional e a ausência de GTFS-RT no catálogo não prova ausência no Brasil.
- **Rejeição:** [I-008] **INFERENCE — REVALIDAR:** não tratar registro, `urls.latest` ou status do catálogo como arquivo atual, autoridade, licença, cobertura nacional ou GTFS-RT confirmado.
- **Revalidação:** [R-004] URL `https://github.com/MobilityData/mobility-database-catalogs`; acesso registrado `2026-08-02` em `brasil-gtfs.md`; limitação: catálogo é diretório, e produtor oficial, bytes, hash, frescor e termos precisam de checagem separada.

### R-005 — `roldaobatista/roldao-method`

- **Papel:** [F-005] **FACT — REVALIDAR:** [`roldao-method.md`](roldao-method.md) o usa como referência de engenharia para contrato observável, fixtures, checks e promoção gradual; não como base para copiar framework.
- **Ganho:** [I-009] **INFERENCE — REVALIDAR:** regra de três, non-goals, fixture sintética, check offline e rastreabilidade podem informar um caminho proporcional de promoção.
- **Lacuna:** [U-005] **UNKNOWN — REVALIDAR:** contagens, compatibilidade, dependências, licença e comportamento atual do upstream não foram revalidados; nenhum padrão implica cobertura jurídica, fiscal ou regulatória.
- **Rejeição:** [I-010] **INFERENCE — REVALIDAR:** não portar CLI, árvore de agents/workflows, hooks Claude-only, addon framework, scraping, mutação externa, dependências ou claims legais/fiscais prontos.
- **Revalidação:** [R-005] URL `https://github.com/roldaobatista/roldao-method/tree/main`; acesso registrado `2026-08-02` em `roldao-method.md`; limitação: a referência local não valida estado atual, licença, números ou capacidade do upstream.

### R-006 — `rodrigowindows/GTFS`

- **Papel:** [F-006] **FACT — REVALIDAR:** `brasil-gtfs.md` cita uma URL raw deste repositório para um arquivo histórico associado a Bagé/RS.
- **Ganho:** [I-011] **INFERENCE — REVALIDAR:** pode servir, no máximo, como pista histórica ou fixture a redigir e validar; não como feed operacional.
- **Lacuna:** [U-006] **UNKNOWN — REVALIDAR:** autoridade do produtor, licença, frescor, integridade do arquivo e continuidade do serviço não foram confirmados.
- **Rejeição:** [I-012] **INFERENCE — REVALIDAR:** não usar a cópia comunitária para afirmar serviço atual, cobertura, licença ou autoridade de Prefeitura/operador.
- **Revalidação:** [R-006] URL `https://github.com/rodrigowindows/GTFS/raw/master/GTFS_Bage.zip`; acesso registrado `2026-08-02` no mapa GTFS; limitação: URL de arquivo não prova produtor, validade, licença ou atualização.

### R-007 — `benaytms/urbs-gtfs`

- **Papel:** [F-007] **FACT — REVALIDAR:** `brasil-gtfs.md` cita uma cópia GitHub para URBS/Curitiba e a classifica como fonte catalogada não oficial.
- **Ganho:** [I-013] **INFERENCE — REVALIDAR:** pode ajudar a localizar uma pista para comparação read-only, desde que o portal URBS seja reaberto e a cópia não seja promovida.
- **Lacuna:** [U-007] **UNKNOWN — REVALIDAR:** licença, frescor, autoridade, integridade e correspondência entre cópia e portal oficial não foram confirmados.
- **Rejeição:** [I-014] **INFERENCE — REVALIDAR:** não tratar o repositório como produtor, nem publicar sua cópia como feed atual, licenciado ou completo.
- **Revalidação:** [R-007] URL `https://github.com/benaytms/urbs-gtfs/releases/download/latest/gtfs_curitiba.zip`; acesso registrado `2026-08-02` no mapa GTFS; limitação: cópia comunitária e URL de release não provam termos, bytes atuais, escopo ou autoridade.

## Council: pergunta, posições e dissent

**Pergunta:** quais repositórios podem informar o próximo corte da BR Skill, quais ficam apenas como contexto e o que deve ser rejeitado até haver evidência?

**Status:** `INPUT_INCOMPLETE`. Este arquivo não executou Council/subagentes nem inventa consenso. As posições abaixo são um mapa de argumentos derivados dos contratos locais; a pessoa responsável decide o próximo gate.

**Fonte de verdade:** `AGENTS.md`, `SKILL.md`, referências locais e fontes primárias reabertas no futuro. Council apenas organiza esses materiais.

### Painel proposto — posições independentes

- **Skeptic:** [I-015] **INFERENCE — REVALIDAR [R-003, R-004, R-006, R-007]:** manter a skill Markdown-first e sem adapters/runtime; catálogos, MCP e cópias comunitárias são apenas pistas até produtor, termos, frescor e escopo estarem revalidados. Não aceitar números, cobertura ou capacidade vindos de README/catalogação.
- **Pragmatist:** [I-016] **INFERENCE — REVALIDAR [R-003, R-004]:** preservar MCP e MobilityData como referências de discovery pode reduzir repetição sem criar dependência; o próximo passo reversível é um registro de evidência read-only, com `UNKNOWN` explícito e sem bridge.
- **Critic:** [I-017] **INFERENCE — REVALIDAR [R-003, R-004, R-006, R-007]:** priorizar risco de proveniência e licença: cópia comunitária, URL raw, catálogo e agregador podem conflitar com produtor. Qualquer adapter deve parar em `manual_review` quando a fonte primária não puder confirmar o campo material.

### Dissent preservado

- [I-018] **INFERENCE:** Pragmatist aceita catálogo/agregador como ponto de partida documental; Skeptic rejeita qualquer promoção até revalidação do produtor. As duas posições permanecem; nenhuma vira `FACT`.
- [I-019] **INFERENCE:** Pragmatist admite uma fixture histórica redigida para testar estados; Critic exige prova de licença, integridade e finalidade antes de reutilizar bytes comunitários. Decisão fica adiada.
- [U-008] **UNKNOWN:** não há votação, consenso, cite-check live ou painel executado neste artefato.

### Limite da recomendação

[I-020] **INFERENCE:** manter os sete repositórios como referências classificadas é o menor corte reversível. Nenhum deve gerar adapter, servidor MCP, bridge, crawler, runtime compartilhado ou promessa de cobertura sem os gates do roadmap. Isso não é autorização de implementação ou publicação.

## Roadmap por gates

### P0 — revalidar o inventário, read-only

1. Reabrir cada URL `R-001`–`R-007` sem login, CAPTCHA, pagamento ou bypass; registrar URL canônica, acesso, jurisdição/escopo observado e estado (`ok`, `blocked`, `stale`, `auth_required` ou `UNKNOWN`).
2. Para `R-002`–`R-007`, confirmar se papel, termos, licença, frescor, produtor e capacidade alegados ainda são sustentados; se não, reduzir a `UNKNOWN` ou `manual_review`.
3. Para GTFS, separar catálogo → produtor oficial → arquivo atual; não baixar bytes sem autorização, limite e necessidade aprovada.
4. Confirmar a existência do remoto `Atroci/br-skill` antes de qualquer publicação. Esta confirmação não autoriza push.

### P1 — contrato mínimo, se houver caso real

1. Escolher um único domínio e fonte autorizada somente após P0; declarar jurisdição, capacidade, entradas, saída, falhas e non-goals.
2. Criar fixture pública, mínima e redigida, com um check read-only que preserve `UNKNOWN` e distinga `blocked` de `no_result`.
3. Pedir revisão Orca do contrato; nenhum resultado de Council substitui teste, cite-check ou fonte primária.

### P2 — promoção condicionada

1. Promover um adapter apenas quando fonte, fixture, teste, proveniência, frescor e handoff estiverem aprovados.
2. Só considerar lógica comum no `Center` após dois adapters independentes exigirem o mesmo comportamento sem exceções locais e casos comparáveis confirmarem o contrato.
3. Só considerar bridge `stdio`/HTTP se dois runtimes ou adapters precisarem da mesma fronteira; manter `discover`/`call` read-only e `submit` human-gated.

### P3 — publicação separada

Rodar `quick_validate.py`, check nativo disponível, `git diff --check` e revisão de escopo. Commit, push, PR, merge, deploy e ação externa continuam gates separados; esta tarefa só cobre o artefato documental local.

## Rejeições e critérios de parada

- Rejeitar “todos os repositórios”, “todas as APIs”, “cobertura nacional”, números, licença, SLA ou capacidade sem fonte, data e limite verificáveis.
- Rejeitar catálogo, MCP, README, URL raw ou cópia comunitária como autoridade do produtor, arquivo atual, registro, feed realtime ou direito jurídico.
- Parar quando uma fonte estiver bloqueada, autenticada, ambígua, stale ou com termos/licença materialmente desconhecidos; não converter falha em lista vazia.
- Parar se uma fixture contiver segredo, cookie, token, PII ou dado de cliente.
- Parar qualquer ação externa se surgir login, CAPTCHA, assinatura, pagamento, envio, contato, candidatura, publicação, push, PR, merge ou deploy.
- Rebaixar confiança e preservar dissent quando cite-check, produtor, jurisdição, frescor ou escopo entrarem em conflito.

## Referências locais lidas

- [`AGENTS.md`](../AGENTS.md) — escopo, upstream e gates de publicação.
- [`SKILL.md`](../SKILL.md) — roteamento, rótulos, fontes e limites.
- [`arquitetura.md`](arquitetura.md) — Center, Moat, fontes auxiliares e limites de escala.
- [`mcp-brasil.md`](mcp-brasil.md) — MCP como agregador e contrato de proveniência.
- [`brasil-gtfs.md`](brasil-gtfs.md) — catálogo GTFS, produtores e cópias comunitárias.
- [`roldao-method.md`](roldao-method.md) — contrato mínimo, checks e promoção sem copiar framework.
- [`adapters.md`](adapters.md) — fonte, jurisdição, falhas, fixture e aprovação.
- [`council-adapter.md`](council-adapter.md) — dissent, `UNKNOWN`, fonte de verdade e gate humano.
- [`plataformas.md`](plataformas.md) e [`governanca-seguranca.md`](governanca-seguranca.md) — distribuição e gates separados.
