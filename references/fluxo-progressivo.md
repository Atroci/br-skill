# Fluxo progressivo: Spec Kit + Orca

## Contrato

Esta referência traduz o fluxo agentic do GitHub Spec Kit para prompts em
português brasileiro e gates supervisionados pelo Orca. Ela é uma orientação
portátil: não instala Spec Kit, não cria `.specify/`, não substitui CI, revisão
humana ou autoridade do repositório e não transforma uma resposta de agente em
aprovação.

Os nomes abaixo são fases e artefatos conceituais. Quando um projeto tiver
Spec Kit instalado, os caminhos usuais são `.specify/memory/constitution.md`,
`spec.md`, `plan.md` e `tasks.md`; confirme a estrutura e a versão local antes
de executar qualquer comando. Sem Spec Kit, os mesmos prompts podem ser
usados como instrução textual e os artefatos podem ser Markdown comum.

O fluxo completo é:

```text
constitution → specify → clarify → plan → tasks → analyze → implement → converge
```

`checklist` é um gate opcional do Spec Kit. Quando estiver disponível, use-o
entre `plan` e `tasks` ou depois de `clarify`; ele não elimina `analyze`, CI ou
revisão. Fases de alto risco podem voltar a uma fase anterior várias vezes.

## Pré-voo portátil

1. Registre objetivo, não-objetivos, repositório, branch/worktree, arquivos no
   escopo, jurisdição, dados pessoais, capacidade (`lookup`, `prepare` ou
   `submit`), risco, fonte e check esperado.
2. Carregue a pasta inteira da skill. O caminho de descoberta varia por
   runtime; consulte [`plataformas.md`](plataformas.md). Não dependa de
   `agents/openai.yaml` para comportamento.
3. Se o CLI `specify` existir, confirme a instalação sem assumir versão:

   ```bash
   specify --help
   specify version
   specify version --features
   ```

   Se não existir, registre `unsupported` para a capacidade e continue com os
   prompts portáteis; não instale dependência apenas para esta referência.
4. Se Orca estiver disponível, o coordenador cria Run, tarefas e worktrees
   com escopo, saída, limite e proibição de mutação explícitos. Se Orca não
   estiver disponível, o operador aplica os mesmos gates manualmente e registra
   a limitação.
5. Antes de cada mutação, confirme que o artefato anterior foi revisado. Uma
   fonte externa, resultado MCP, navegador, worker ou modelo é evidência a
   revisar, nunca autorização.

### Forma de invocação

O Spec Kit documenta `/speckit.*` como forma canônica, mas a forma real depende
do agente. Alguns agentes baseados em skills expõem `$speckit-*`; outros podem
expor slash command, comando de skill ou nenhum comando. Não escreva um
prompt que dependa de uma forma específica:

| Runtime | Descoberta da BR Skill | Invocação Spec Kit | Fallback sem capacidade |
|---|---|---|---|
| Codex | `.agents/skills/br-skill/` ou `~/.agents/skills/br-skill/` | use o alias que a sessão expuser, frequentemente `$speckit-*` | cole o prompt PT-BR como mensagem |
| OpenCode | `.opencode/skills/br-skill/`, `.agents/skills/br-skill/` ou diretório de usuário | use o command/skill instalado e confirme no help | cole o prompt PT-BR como mensagem |
| Gemini CLI | `.gemini/skills/br-skill/`, `.agents/skills/br-skill/` ou diretório de usuário | recarregue/lista de skills; use a forma exposta | cole o prompt PT-BR como mensagem |
| Google Antigravity | `.agents/skills/br-skill/` ou `~/.gemini/config/skills/br-skill/` | use a integração disponível; não presuma slash command | cole o prompt PT-BR como mensagem |

Em todos os runtimes, o conteúdo desta referência é a parte portátil. Não
presuma Orca, MCP, navegador, login, script, bloqueio automático ou integração
específica. Login, CAPTCHA, pagamento, assinatura, submissão e qualquer efeito
externo continuam exigindo handoff e aprovação explícitos.

## Gates Orca e autoridade

O Orca organiza trabalho; não altera a autoridade técnica do repositório.
Cada tarefa delegada deve declarar:

- objetivo e fase;
- worktree/branch e arquivos permitidos;
- entradas e artefato de saída;
- risco, dados proibidos e limite de execução;
- checks esperados e formato do relatório;
- condição de bloqueio e destinatário da escalada.

Use esta sequência de estados, mesmo quando a ferramenta não estiver
disponível:

```text
proposto → em execução → artefato pronto → revisão Orca → aprovado para próxima fase
                         ↘ blocked/manual_review
```

### Gates obrigatórios

| Gate | Evidência mínima | Decisão e limite |
|---|---|---|
| Entrada | objetivo, escopo, risco, capacidade, branch/worktree e check | coordenador aceita ou pede esclarecimento; não há mutação implícita |
| Constituição/especificação | artefato, lacunas e princípios aplicáveis | aprovação explícita para propagar regras a templates ou fases seguintes |
| Planejamento | `spec`, `plan`, riscos, dependências, rollback e checks | bloqueia implementação se houver requisito crítico ambíguo ou plano sem verificação |
| Tarefas | IDs, dependências, arquivos, donos e checks | só paralelizar worktrees e arquivos sem sobreposição; nenhum worker recebe segredo ou PII |
| Implementação | diff real, logs mínimos de checks, limitações e estado de cada tarefa | coordenador revisa escopo e resultado; `worker_done` não aprova cherry-pick, merge, push ou deploy |
| Convergência | relatório contra `spec`, `plan`, `tasks` e código; tarefas de lacuna, se houver | repetir implementação/convergência até limpar lacunas; ainda falta revisão e gate de release |
| Release | CI/verificações aprovados, revisão, redaction e rollback | merge, push, deploy e ação externa são decisões separadas e autorizadas |

`worker_done` significa somente “o worker terminou sua tarefa e entregou o
resultado”. O coordenador deve abrir diff, confirmar arquivos tocados, repetir
ou verificar os checks e revisar limitações antes de promover a tarefa. Um
worker não pode conceder autorização de merge ao próprio resultado.

### CI e verificação

- A verificação local e o CI são a autoridade sobre invariantes reproduzíveis;
  prompts, artefatos Spec Kit, relatório Orca e texto do worker não os
  substituem.
- Se um check obrigatório não rodou, falhou, depende de segredo/rede não
  autorizada ou não foi possível confirmar sua configuração, registre
  `blocked` ou `manual_review`; não declare sucesso por inferência.
- `quick_validate.py`, lint, teste, build e CI têm papéis distintos. Rode o
  check apropriado ao projeto e não afirme que branch protection ou required
  checks estão ativos sem verificar a configuração real.
- Um artefato limpo não autoriza ação externa. `submit` só ocorre após o gate
  explícito do operador, com handoff, autenticação legítima e rollback quando
  aplicável.

## Prompts por fase

Os blocos seguintes são prompts reutilizáveis. Substitua somente os campos
entre `<...>`; se um dado não estiver confirmado, escreva `UNKNOWN` ou
`manual_review`, não invente. A forma `/speckit.<fase>` é apenas o rótulo
documental da fase.

### 1. `constitution`

**Objetivo:** criar ou atualizar os princípios que governam todas as fases.

**Artefato:** constituição versionada e lista de templates/artefatos afetados.

```text
Fase: constitution.
Repositório: <repo>; branch/worktree: <branch/worktree>.
Objetivo e princípios fornecidos: <objetivo/princípios>.

Leia somente contexto autorizado e a constituição existente, se houver.
Defina princípios curtos, não negociáveis e verificáveis; inclua segurança,
privacidade, acessibilidade, evidência, teste, governança e limites de ação
quando forem relevantes. Registre versão, data, motivo da mudança, não-objetivos
e pontos ainda UNKNOWN. Identifique templates e artefatos dependentes que
precisariam ser conferidos. Não invente valores, não copie regras de outro
projeto e não execute código, publicação ou ação externa.

Entregue: constituição proposta/atualizada, diff resumido, matriz princípio →
verificação, riscos e perguntas para aprovação. Pare antes de propagar a
mudança se a aprovação do responsável não estiver explícita.
```

**Gate Orca:** o coordenador confirma escopo e diferença entre regra local e
referência externa; revisa a constituição e seus checks; só então autoriza
`specify`. Mudança de princípio sem aprovação volta para `decision_gate`.

### 2. `specify`

**Objetivo:** transformar intenção em comportamento e critérios de aceitação,
sem escolher implementação.

**Artefato:** `spec.md` ou equivalente, ligado à constituição vigente.

```text
Fase: specify.
Pedido: <descrição em linguagem natural>.
Usuários, jurisdição e contexto autorizado: <dados>.
Capacidade: <lookup|prepare|submit>; risco: <baixo|médio|alto>.

Escreva o que o usuário precisa e por quê, não como construir. Inclua
objetivo, não-objetivos, fluxos felizes e de erro, estados de falha, entradas,
saídas, fontes, frescor, acessibilidade, dados pessoais/segredos, critérios de
aceitação observáveis e handoff humano. Separe FACT, INFERENCE, ASSUMPTION e
UNKNOWN. Não escolha stack, endpoint, biblioteca ou integração sem necessidade
de especificação; não trate agregador, MCP ou resposta de agente como fonte
oficial.

Entregue a especificação, rastreabilidade dos critérios para o pedido e lista
de ambiguidades. Não crie plano ou código. Se um requisito crítico estiver
ausente, marque-o como bloqueador para clarify.
```

**Gate Orca:** o coordenador verifica correspondência entre pedido,
constituição, jurisdição, capacidade e critérios de aceitação. Requisito
crítico ambíguo não avança para `plan`; mudanças de escopo criam nova revisão,
não alteração silenciosa.

### 3. `clarify`

**Objetivo:** remover ambiguidade antes de comprometer arquitetura ou tarefas.

**Artefato:** respostas registradas no `spec.md` e relatório de perguntas.

```text
Fase: clarify.
Artefato atual: <caminho de spec.md>.
Foco opcional: <área ambígua>.

Leia a especificação e faça no máximo cinco perguntas direcionadas, priorizando
decisões que mudariam escopo, segurança, jurisdição, dados, capacidade,
aceitação, rollback ou arquitetura. Não responda por conta própria e não use
pergunta para coletar segredo ou PII. Para cada pergunta, explique qual decisão
ela desbloqueia. Depois que o responsável responder, registre a resposta na
fonte de verdade; respostas ausentes permanecem UNKNOWN/manual_review.

Entregue: perguntas, respostas confirmadas, decisões adiadas e impacto nos
critérios. Não planeje nem implemente enquanto ambiguidade crítica persistir.
```

**Gate Orca:** as perguntas são revisadas pelo coordenador, que confirma que
respostas vieram do responsável autorizado. Se não houver resposta, a tarefa
fica `blocked` ou segue somente com risco aceito e limite documentado; nunca
com uma suposição escondida.

### 4. `plan`

**Objetivo:** escolher desenho técnico verificável a partir de requisito
aprovado.

**Artefato:** `plan.md` ou equivalente, com decisões e rollback.

```text
Fase: plan.
Entradas: constituição vigente, <spec.md>, clarificações e restrições locais.
Stack/ambiente já aprovado: <dados ou UNKNOWN>.

Projete a solução necessária para atender a especificação. Mapeie cada
critério para componentes, interfaces, dados, dependências, permissões,
observabilidade, migração, rollback e checks. Reutilize padrões e dependências
existentes; não adicione infraestrutura, runtime, segredo ou integração
especulativa. Diferencie decisão, alternativa rejeitada, suposição e risco.
Defina como testar falhas, limites de fonte, acessibilidade, consentimento e
efeitos externos. Se uma capacidade do runtime não existir, desenhe um
fallback read-only ou marque manual_review.

Entregue: plano, matriz requisito → decisão → verificação, ordem de entrega,
risco residual e perguntas de aprovação. Não implemente.
```

**Gate Orca:** revisão read-only confirma que o plano não contradiz a spec,
não cria escopo e possui check/rollback. O coordenador bloqueia implementação
quando a dependência, permissão ou verificação é desconhecida; aprovação do
plano não é aprovação de merge.

### 5. `tasks`

**Objetivo:** decompor o plano em trabalho executável e rastreável.

**Artefato:** `tasks.md` com IDs estáveis, dependências e checks.

```text
Fase: tasks.
Entradas: <spec.md>, <plan.md>, constituição e decisões de clarify.

Gere tarefas pequenas, observáveis e ordenadas por dependência. Use fases de
Setup, Foundational, histórias/entregas em prioridade e Polish somente quando
forem necessárias. Para cada tarefa, informe ID estável, objetivo, arquivos
permitidos, pré-condições, resultado, check e critério de conclusão. Inclua
testes na mesma entrega quando o requisito exigir; marque paralelismo apenas
quando worktrees e arquivos não se sobrepõem. Separe tarefas read-only de
mutação e tarefas externas; não coloque segredo, PII, login ou deploy no
escopo implícito.

Entregue: tasks.md, DAG/dependências, agrupamento para workers e riscos de
coordenação. Não escreva código nem remova tarefas para esconder lacunas.
```

**Gate Orca:** o coordenador valida a cobertura de requisitos, a DAG e o
paralelismo. Cada worker recebe somente sua tarefa, worktree, arquivos,
limite, saída e checks; duas escritas no mesmo arquivo exigem sequência ou
worktrees separados. A criação da tarefa Orca não autoriza ação externa.

### 6. `analyze`

**Objetivo:** encontrar inconsistências antes da implementação.

**Artefato:** relatório read-only entre `spec.md`, `plan.md` e `tasks.md`.

```text
Fase: analyze.
Entradas: <spec.md>, <plan.md>, <tasks.md> e constituição.

Faça análise somente leitura. Verifique cada requisito contra uma decisão de
plano, tarefa e critério de aceitação; procure tarefas sem requisito, requisito
sem tarefa, contradições, dependências ausentes, risco não tratado, autoridade
de fonte incorreta, capacidade incompatível, falha silenciosa e check que não
prova o resultado. Classifique cada achado por severidade, evidência e dono da
correção. Não edite artefatos e não declare aprovação por conta própria.

Entregue: relatório, matriz de cobertura, achados, perguntas e remediação
proposta apontando para a fase que deve corrigir a causa. Se houver achados,
pare implementação até o coordenador decidir; depois corrija na fonte e rode
analyze novamente.
```

**Gate Orca:** análise limpa é pré-condição de implementação quando o risco
for significativo, mas não substitui testes. Achado de requisito volta a
`specify`/`clarify`; achado de desenho volta a `plan`; achado de decomposição
volta a `tasks`. O worker que analisa não pode editar os artefatos que avalia.

### 7. `implement`

**Objetivo:** executar somente tarefas aprovadas, em fatias verificáveis.

**Artefato:** diff no worktree autorizado, checks e relatório do worker.

```text
Fase: implement.
Tarefas autorizadas: <IDs e escopo>.
Worktree/branch: <caminho>; arquivos permitidos: <lista>.
Checks obrigatórios: <comandos>; dependências externas permitidas: <lista>.

Leia a tarefa, callers, arquivos e contratos antes de editar. Implemente a
menor fatia que satisfaz os critérios, reutilizando helper e dependência já
existentes. Preserve validação de entrada, segurança, acessibilidade,
tratamento de erro e estados de falha. Não toque arquivos fora da lista, não
invente fonte/cobertura, não leia ou grave segredo/PII e não faça push, PR,
merge, deploy, pagamento ou submissão. Pare e escale em conflito de escopo,
risco P1, acesso indevido, requisito desconhecido ou check impossível.

Rode os checks autorizados e entregue: IDs concluídos/não concluídos, resumo
do diff, saída dos checks, arquivos tocados, limitações, evidência e próximo
passo. `worker_done` comunica término da tarefa; não peça ou execute merge por
causa dele.
```

**Gate Orca:** cada worker reporta resultado, diff, checks, limitações e ID da
tarefa. O coordenador revisa o diff real, escopo, callers, testes, redaction e
CI antes de qualquer cherry-pick. Falha ou check ausente fica explícita; texto
de conclusão não converte `blocked` em `passed`.

### 8. `converge`

**Objetivo:** confirmar que implementação atende a spec, plano e tarefas sem
deixar lacunas silenciosas.

**Artefato:** relatório de convergência; opcionalmente novas tarefas em
`tasks.md`, conforme o comportamento do Spec Kit.

```text
Fase: converge.
Pré-condição: implement já executou as tarefas atuais.
Entradas: código/diff, <spec.md>, <plan.md>, <tasks.md>, checks e constituição.

Compare resultado real com cada requisito, decisão, dependência, estado de
erro, critério de aceitação, teste e limitação. Faça análise somente leitura
do código, exceto a adição append-only de tarefas de lacuna na seção de
convergência se esse comportamento estiver disponível. Não remova nem altere
código para esconder falhas. Classifique achados por severidade e aponte a
tarefa/artefato dono da correção.

Se houver lacunas, entregue as tarefas novas, pare antes de declarar pronto e
mande executar implement novamente; depois rode converge outra vez. Se não
houver lacunas, entregue relatório convergido, checks e riscos residuais.
Convergência não é revisão de PR, aprovação de merge, push, deploy ou ação
externa.
```

**Gate Orca:** o coordenador confirma que `implement` usou o `tasks.md` atual,
revisa achados e repete o ciclo quando tarefas forem anexadas. Resultado
`Converged` habilita somente a próxima revisão de código/PR; CI, revisão e
aprovação de merge continuam gates separados.

## Fluxo de falha e handoff

Use estados explícitos: `ok`, `no_result`, `stale`, `blocked`,
`auth_required`, `manual_review` e `unsupported`. Uma lista vazia não pode
representar fonte bloqueada. Para cada bloqueio, registre causa, evidência
obtida, impacto, limitação, responsável pelo próximo passo e condição para
retomar.

- **Capacidade ausente:** use prompt textual e entrega `prepare`/`lookup`;
  declare `unsupported` para a automação não disponível.
- **Ambiguidade crítica:** volte a `clarify`; não preencha com palpite.
- **Inconsistência:** corrija na fase dona e rode `analyze` novamente.
- **Check falho ou indisponível:** preserve log mínimo, marque `blocked` ou
  `manual_review` e não promova por texto.
- **Login, CAPTCHA, PII ou ação externa:** pare; faça handoff humano com
  escopo, fonte, jurisdição, risco e rollback, sem transportar segredo.
- **Orca indisponível:** mantenha a DAG e os gates em Markdown/issue local;
  não finja que a supervisão automática ocorreu.

## Fonte, frescor e limites

- [GitHub Spec Kit — Agentic SDD](https://github.github.com/spec-kit/reference/agentic-sdd.html) — acessado em `2026-08-03`; fonte primária para a sequência, objetivos, artefatos e comportamento de `constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement` e `converge`.
- [GitHub Spec Kit — Reference overview](https://github.com/github/spec-kit/blob/main/docs/reference/overview.md) — acessado em `2026-08-03`; fonte primária para separar CLI, integrações e comandos agentic, além da natureza opcional de gates.
- [GitHub Spec Kit — Core commands](https://github.github.com/spec-kit/reference/core.html) — acessado em `2026-08-03`; fonte primária para `specify --help`, `version`, `version --features` e confirmação de capacidade local.
- [`spec-kit-orca.md`](spec-kit-orca.md) — contrato local para risco proporcional, execução supervisionada, revisão e separação entre `worker_done`, merge, push e deploy.
- [`plataformas.md`](plataformas.md) — contrato local de descoberta, instalação, recarga e capacidades opcionais nos quatro runtimes.

Os docs upstream podem mudar; URLs, sintaxe e integrações devem ser
revalidadas no runtime instalado. Esta referência não fixa versão, não declara
que um comando existe em Codex, OpenCode, Gemini CLI ou Google Antigravity e
não cria enforcement técnico: a autoridade final continua sendo código,
verificação local/CI, revisão autorizada e gate operacional explícito.
