# Spec Kit e Orca

## Princípio

Spec Kit é uma camada de especificação proporcional ao risco; não é autoridade de release e não substitui teste, lint, revisão ou aprovação humana. Use a versão instalada no ambiente e confirme seus comandos antes de automatizar. Esta skill ainda não contém `.specify/` nem impõe uma versão de CLI.

## Níveis de especificação

| Situação | Artefato mínimo | Gate |
|---|---|---|
| ajuste de texto ou link | issue/check curto | validação local |
| mudança pequena e delimitada | `spec`, `tasks` | teste/check |
| novo adapter read-only | `spec`, `plan`, `tasks`, fixture e matriz de fonte | revisão Orca + teste |
| jurídico, login, PII, tenancy, pagamento ou efeito externo | artefatos completos + threat model + plano de rollback | aprovação explícita antes de executar |
| CI, issue ou mudança documental pública | escopo, fonte, redaction, check e revisão PR | merge separado de push |

`spec`, `plan` e `tasks` são nomes conceituais; não crie arquivos ou comandos específicos sem confirmar o Spec Kit disponível no projeto.

## Conteúdo obrigatório para domínio grande

- objetivo e não-objetivos;
- usuários, jurisdição e contexto autorizado;
- fontes e licença;
- dados pessoais, segredo e ameaça;
- contrato de entrada/saída e falhas;
- capacidade (`lookup`, `prepare`, `submit`);
- critérios de aceitação e fixture;
- handoff, rollback e aprovação;
- o que fica explicitamente adiado.

## Orca: execução supervisionada

Fora de um terminal gerenciado pelo Orca, use `orca-ide`; dentro dele, o binário pode ser `orca`. Comandos abaixo seguem a CLI atual conhecida; confirme `--help` no runtime instalado:

```bash
orca-ide orchestration run-create --objective "Mapear fontes oficiais brasileiras" --json
orca-ide orchestration task-create --run <RUN_ID> --spec "Fontes jurídicas; somente leitura; devolver URLs e limites" --json
orca-ide orchestration task-create --run <RUN_ID> --spec "Fontes imobiliárias; somente leitura; separar cadastro de registro" --json
orca-ide orchestration worker-start --task <TASK_ID> --worktree current --agent codex --run <RUN_ID> --json
orca-ide orchestration task-list --run <RUN_ID> --json
orca-ide orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
```

Cada worker recebe repo, arquivos, escopo, formato de saída e proibição de mutação. Ao terminar, deve registrar resultado, evidências, limitações e IDs de tarefa. O coordenador sintetiza; não promove automaticamente.

`worker_done` encerra o trabalho delegado, mas não é autorização para cherry-pick, merge, push, deploy ou ação externa. O coordenador deve revisar diff, escopo, checks e fonte antes do próximo gate. Se o Run ou terminal Orca estiver indisponível, registrar a limitação e não transformar uma conclusão textual em aprovação.

## Ondas BR Skill

1. **Mapa:** arquitetura, fontes oficiais, jurisdições, riscos e lacunas.
2. **Center:** contrato de evidência, falhas e aprovação.
3. **Moat:** vocabulário, formatos, regras e fontes brasileiras de um domínio.
4. **Adapters:** um jurídico e um imobiliário read-only, cada um com fixture.
5. **Handoff:** browser/login ou ação externa apenas se existir aprovação, autenticação legítima e rollback.

Não paralelize duas escritas no mesmo arquivo ou repo sem worktrees separados. Revisão read-only pode ocorrer em paralelo; merge, push, deploy e ação externa são gates do operador.

## PR e publicação

O workflow de qualidade executa checks locais em `pull_request` e `push`, sem segredo nem rede de aplicação. Isso prova invariantes do pacote, não ativa branch protection. Required checks, revisão obrigatória e regras de merge precisam ser configurados separadamente nas definições do GitHub; não declarar essa configuração como ativa sem verificar.

## Segurança de orquestração

- Não passe segredo, cookie ou PII para worker.
- Não alimente ferramenta mutável diretamente com resultado não verificado de pesquisa externa.
- `[P1]` ou suspeita de acesso indevido interrompe promoção até conferência no artefato real.
- `worker_done` encerra apenas a tarefa delegada; não autoriza merge, publicação ou ação externa.
- Se fonte oficial estiver indisponível, reporte a lacuna; não faça fallback silencioso para site não autorizado.
