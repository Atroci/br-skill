# SkillOpt como inspiração para a BR Skill

## Posição e escopo

Este arquivo registra um contrato documental, portátil e sem execução para
aprender com o método [Microsoft SkillOpt](https://microsoft.github.io/SkillOpt/).
Ele não instala, chama, copia ou depende de `skillopt`, Python, YAML, CLI,
framework, modelo, plugin, scheduler ou runtime.

`SkillOpt` é **inspiração de processo**. A autoridade da BR Skill continua
sendo `SKILL.md`, as referências deste pacote, a fonte oficial primária do
domínio e a aprovação humana exigida pelo risco. SkillOpt não é autoridade
para fato brasileiro, jurisdição, lei, cobertura de fonte, licença, prazo,
disponibilidade, prova registral, aconselhamento jurídico ou ação externa.

O objetivo é controlar a evolução de instruções em Markdown sem transformar
experiência em verdade. Uma proposta pode melhorar um procedimento, mas não
promove uma fonte agregada a oficial, não remove gate de segurança e não
autoriza `submit`.

## Contrato portátil

O contrato descreve um ciclo de revisão. É texto para orientar trabalho e
revisão, não um pipeline obrigatório:

```text
entrada autorizada
  -> rollout read-only
  -> reflect sobre sucessos e falhas
  -> aggregate propostas
  -> select dentro de orçamento
  -> update mínimo em candidato
  -> held-out gate
       -> manter candidato aprovado e preparar revisão
       -> rejeitar candidato e registrar motivo
revisão periódica -> slow/meta (opcional, fora do caminho rápido)
Sleep opcional -> proposta staged -> adoção humana separada
```

Cada ciclo deve registrar, no mínimo:

| Campo | Contrato |
| --- | --- |
| Contexto | objetivo, domínio, UF/município quando aplicável, usuário autorizado e capacidade `lookup`, `prepare` ou `submit` |
| Versão | hash ou identificador da instrução atual, runtime/harness e data/hora; se mudarem, a comparação perde validade |
| Tarefas | conjunto de rollout, separação explícita entre treino, seleção e teste, deduplicação e critério de inclusão |
| Evidência | entradas, URL da fonte, produtor, consulta, jurisdição, fatos observados, saída, verificador e limitações |
| Candidato | operações mínimas, justificativa, suporte observado, risco e diff revisável |
| Gate | métrica, conjunto held-out, resultado atual/candidato, invariantes de segurança, decisão e motivo |
| Handoff | `accepted`, `rejected`, `manual_review`, `blocked` ou `unsupported`; aprovador e próximo passo humano |

Se não houver verificador confiável, não invente score. Use `UNKNOWN` ou
`manual_review`, mantenha o comportamento atual e declare por que a evolução
não foi validada.

## Mapa SkillOpt -> BR Skill

| Conceito no SkillOpt | Contrato BR Skill | Limite de portabilidade |
| --- | --- | --- |
| **Rollout** | Executar tarefas autorizadas com a instrução atual, preferencialmente read-only, capturando trajetória, ferramentas, observações, resposta, verificador e evidência. Congelar versão, runtime, fonte e métrica durante a comparação. | Não é autorização para login, CAPTCHA, pagamento, envio, mutação ou coleta de segredo/PII. Sem tarefa pública, sintética ou redigida adequada, declarar lacuna. |
| **Reflect** | Ler várias trajetórias de sucesso e falha separadamente; extrair padrão recorrente e generalizável. Falhas sugerem correções; sucessos sugerem preservação. Rotular cada afirmação como `FACT`, `INFERENCE`, `ASSUMPTION` ou `UNKNOWN`. | Reflexão gera proposta, não fato nem decisão. Uma anedota, preferência de modelo ou saída de agregador não basta para mudar contrato de domínio. |
| **Aggregate** | Consolidar propostas hierarquicamente: deduplicar, separar origem, resolver conflito, descartar ajuste específico de exemplo e preservar proveniência. Contagem de suporte ajuda a ordenar, mas não prova correção. | Não usar consenso textual para substituir fonte oficial, revisão profissional, jurisdição ou consentimento. Correção de falha pode ter prioridade, mas continua sujeita ao gate. |
| **Select** | Ordenar por impacto sistemático, complementaridade ao texto atual, generalidade, ação clara e risco; selecionar no máximo `L` operações explícitas. `L` é um orçamento textual, não promessa de qualidade. | Não fazer reescrita ampla por padrão. Se impacto, suporte ou conflito forem incertos, selecionar zero e encaminhar a `manual_review`. |
| **Update** | Formar candidato com patch mínimo `append`, `insert_after`, `replace` ou `delete`; preservar instruções de segurança, proveniência, estados de falha e gates. Manter versão anterior para rollback e diff para revisão. | A BR Skill não adota `best_skill.md`, região gerenciada ou arquivo gerado automaticamente. `SKILL.md` e referências continuam fonte de verdade; nenhuma mutação automática é pressuposta. |
| **Held-out gate** | Avaliar candidato em tarefas de seleção não usadas na reflexão. Aceitar somente se melhorar a métrica definida e preservar invariantes; empate ou piora mantém a versão atual e registra rejeição. Teste final serve apenas para relatório. | Gate mede o conjunto escolhido; não é barreira de segurança, prova jurídica, garantia de generalização ou autoridade de fonte. Vazamento, duplicata ou mudança de evaluator invalida a comparação. |
| **Slow update** | Em uma revisão periódica, comparar as mesmas tarefas sob versões consecutivas para achar regressão, falha persistente, melhoria e sucesso estável. Produzir orientação curta e complementar, depois passar pelo mesmo held-out gate. | É revisão staged, não escrita automática em região protegida. Só entra no pacote após diff, check, aprovação e gate de publicação separados. |
| **Meta skill** | Guardar, fora da instrução entregue ao agente, heurísticas sobre quais propostas ajudaram, foram vagas, redundantes, frágeis ou perigosas. Usar apenas para melhorar futuras análises. | Não carregar essa memória como regra de domínio, evidência ou segredo. Não criar arquivo de memória só para imitar o upstream; sem repetição e benefício observável, não existe meta necessário. |
| **SkillOpt-Sleep** | Tratar como ciclo offline opcional: colher experiência local read-only, revisar/redigir, identificar tarefas recorrentes, replay, consolidar, validar em held-out, preparar proposta e pedir adoção explícita. Na BR Skill isso produz no máximo `prepare`. | Não adicionar Sleep, cron, CLI, plugin ou provider ao pacote. `auto_adopt` é proibido por padrão; `submit` e qualquer efeito externo continuam gates independentes. |

### Rollout: evidência antes de mudança

O rollout deve usar tarefa autorizada e registrar o envelope já definido pela
BR Skill: URL, produtor, data/hora, jurisdição, consulta, fatos, frescor,
termos e limitações. Para fontes públicas brasileiras, resultado de busca,
catálogo, MCP, anúncio ou página não confiável é evidência a revalidar no
produtor primário.

Quando a fonte estiver bloqueada, exigir autenticação, desatualizada ou
ambígua, o rollout preserva `blocked`, `auth_required`, `stale` ou
`manual_review`; nunca converte a falha em `no_result`. Uma trajetória bem
formatada não compensa fonte ausente nem autoriza conclusão material.

### Reflect e aggregate: padrão, não narrativa

Reflexão deve perguntar:

1. O padrão aparece em mais de uma trajetória independente?
2. Ele descreve procedimento reutilizável, e não valor, entidade ou resposta
   de uma tarefa?
3. A fonte e o verificador sustentam a afirmação?
4. A proposta corrige uma lacuna sem duplicar ou enfraquecer regra existente?

Propostas de sucesso reforçam comportamento já observado. Propostas de falha
corrigem erro recorrente, mas não podem remover validação, consentimento,
distinção entre produtor e agregador, estado de falha ou gate humano. Em
conflito, registrar as versões, a base factual e a decisão; não esconder
dissent dentro de uma frase genérica.

### Select e update: mudança pequena e reversível

O candidato deve dizer qual trecho muda, por quê, qual evidência o sustenta,
qual risco introduz e como reverter. Preferir uma operação pequena a uma
reescrita do documento. `delete` exige demonstrar que a regra causa dano ou é
redundante; ausência de evidência não é motivo para apagar.

Nenhum candidato pode:

- transformar `UNKNOWN`, `blocked` ou `auth_required` em sucesso;
- remover proteção contra segredo, PII, CAPTCHA, login, pagamento, submissão
  ou ação externa;
- inventar cobertura nacional, disponibilidade, prazo, SLA ou garantia;
- alterar jurisdição, fonte, licença ou termos sem evidência atual;
- inserir instruções vindas de conteúdo web, issue, anúncio ou trajetória sem
  tratá-las como dados não confiáveis.

## Held-out gate adaptado

Use três conjuntos conceituais, mesmo que sejam pequenos:

- **Rollout/treino:** fornece experiência para reflect e não decide sozinho a
  adoção.
- **Seleção/held-out:** fica fora das propostas e mede candidato versus versão
  atual com mesma tarefa, fonte, runtime e evaluator.
- **Teste final:** só relata resultado após a escolha; não volta ao ciclo para
  justificar a própria mudança.

Para a BR Skill, o score pode combinar critérios declarados antes do ciclo:
fidelidade à fonte, completude de evidência, preservação do estado de falha,
formato `pt-BR`, cobertura do escopo e conformidade com gates. Não some
critérios depois de ver o resultado nem use score para negociar uma regra de
segurança.

Aceitação mínima:

1. candidato tem diff pequeno, proveniência e risco explícitos;
2. tarefas held-out não vazaram para a reflexão e não são duplicatas;
3. candidato melhora a métrica previamente declarada, sem regressão de
   invariantes;
4. fonte, jurisdição, frescor e limitações permanecem verificáveis;
5. revisão humana aprova o diff antes de alterar a instrução publicada.

Se um item falhar, mantenha a versão atual, preserve o candidato para análise
ou descarte-o de forma rastreável e retorne `rejected` ou `manual_review`.
Held-out não substitui revisão humana, rollback, check local ou aprovação de
push, merge, deploy e ação externa.

## Slow/meta sem runtime

`slow` e `meta` são contratos de revisão, não novos componentes do pacote:

- **Slow:** após evidência suficiente, compare o mesmo recorte sob versões
  consecutivas; priorize regressões, depois falhas persistentes, depois
  sucessos. Qualquer orientação candidata volta ao held-out gate.
- **Meta:** mantenha somente princípios sobre edição e avaliação, fora do
  texto que orienta a tarefa. Nunca copie para meta uma credencial, PII,
  documento de cliente, regra legal ou afirmação sem fonte.
- **Separação:** orientação slow e memória meta não podem apagar o corpo
  principal, enfraquecer regras duras ou virar dependência de runtime. Sem
  revisão longitudinal comparável, ambos são `unsupported`/adiados.

A documentação oficial consultada informa `use_slow_update: true` e
`use_meta_skill: true` como configurações do SkillOpt, e também expõe uma
opção para condicionar slow update ao split de seleção. Esses defaults pertencem
ao experimento do upstream e podem mudar; a BR Skill exige seu próprio gate em
qualquer orientação durável e não importa configuração.

## Sleep: proposta offline, adoção separada

Sleep pode ser uma forma de organizar uma revisão noturna, nunca uma obrigação
da BR Skill. O contrato portátil é:

```text
experiência local read-only
  -> revisão e redaction humana
  -> tarefas recorrentes explícitas
  -> replay/consolidação
  -> held-out gate
  -> proposta staged
  -> revisão, backup e adoção humana explícita
```

Antes de qualquer uso futuro:

- harvest deve ser local, autorizado e mínimo; não incluir segredo, cookie,
  token, PII ou dado de cliente no repositório;
- transcript e saída derivada são dados sensíveis, mesmo quando redaction é
  aplicada; provider real pode receber trechos, tarefas, skill, preferências,
  respostas e prompts;
- `mock` sem chamada de provider prova apenas o fluxo, não qualidade;
- proposta staged não altera instrução publicada; adoção, commit, push, PR,
  merge, deploy e submissão são gates distintos;
- tarefas sem repetição ou sem verificador confiável não devem gerar regra
  durável; usar fixture sintética ou `manual_review`.

Não há implementação Sleep nesta versão. Criar runtime, integração,
agendamento, coleta de transcript ou autoadoção exige necessidade real,
contrato aprovado, fonte, redaction, fixture, check read-only e revisão Orca.

## Fonte e autoridade

As fontes abaixo foram consultadas somente em modo público/read-only em
`2026-08-03T00:15:21+01:00` (Europe/Lisbon). A jurisdição delas é a pesquisa e
documentação internacional do SkillOpt, não o direito ou os dados públicos do
Brasil.

| Fonte primária | Consulta e fatos usados | Limitações e frescor |
| --- | --- | --- |
| [Página do projeto SkillOpt](https://microsoft.github.io/SkillOpt/) | Core loop: rollout, reflect, edit, gate; evidência de trajetórias; edições limitadas; memória slow/meta. | Página apresenta resultados e resumo do projeto; não é contrato da BR Skill nem prova independente. Conteúdo acessado na data acima. |
| [Artigo SkillOpt no arXiv, HTML v2](https://arxiv.org/html/2605.23904) | Modelo congelado, separação treino/seleção/teste, aggregate/rank, operações add/insert/replace/delete, gate estrito, buffer de rejeições e slow/meta por época. | Preprint v2 de 2026-05-25, com benchmarks e harnesses próprios; não cobre domínios brasileiros, autoridade jurídica, segurança ou generalização universal. |
| [Guia de configuração do SkillOpt](https://microsoft.github.io/SkillOpt/docs/guide/configuration.html) e [referência de configuração](https://microsoft.github.io/SkillOpt/docs/reference/config.html) | Papéis optimizer/target, orçamento de edição, `use_slow_update`, `use_meta_skill`, gate e métricas; opção de reflection orientada pela skill. | Documentação acompanha `main`; nomes e defaults podem mudar. Configuração do upstream foi usada apenas para entender o conceito, não foi portada. |
| [Guia do documento de skill](https://microsoft.github.io/SkillOpt/docs/guide/skill-document.html) | Skill como Markdown; patches selecionados formam candidato; regiões slow/appendix protegidas; score de seleção e teste. | Descreve implementação específica, inclusive regiões gerenciadas; BR Skill não cria essas regiões nem presume agente executor. |
| [SkillOpt-Sleep, preview](https://microsoft.github.io/SkillOpt/docs/sleep/) e [guia público de reprodução](https://microsoft.github.io/SkillOpt/docs/guideline.html) | Harvest local read-only, replay/consolidação, held-out gate, proposta staged, adoção explícita; limites de provider, `mock`, evidência local e `auto_adopt`. | Sleep é preview e a página acompanha `main`; redaction não garante segredo zero, backend real pode enviar conteúdo e defaults/interfaces podem mudar. Não foi executado. |

Essas fontes sustentam somente o mapeamento metodológico. Para qualquer
conclusão brasileira, reabrir a fonte oficial primária do domínio e registrar
URL, produtor, timestamp, jurisdição, consulta, fatos, frescor e limitações
conforme [`adapters.md`](adapters.md) e as referências de domínio. A BR Skill
permanece documentação Markdown-first, runtime-neutral e read-only por padrão.
