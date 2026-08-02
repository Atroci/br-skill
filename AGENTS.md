# AGENTS.md — BR Skill

Canary: toda resposta de agente começa com `VIZUH`.

## Escopo

Este é um repositório independente de skill para o Brasil. O upstream `NomaDamas/k-skill` é referência de pesquisa, não fonte para copiar ou modificar. O repositório público pretendido é `Atroci/br-skill`; a existência do remoto precisa ser verificada antes de publicar.

## Fonte de verdade

- `SKILL.md`: comportamento carregado pelo agente.
- `references/*.md`: contexto, contratos, fontes e decisões técnicas.
- `agents/openai.yaml`: metadados de interface.
- `README.md`, `CONTRIBUTING.md` e `CODE_OF_CONDUCT.md`: uso e colaboração.

## Portabilidade

- O contrato portátil é a pasta inteira: `SKILL.md` + `references/` + recursos necessários.
- `agents/openai.yaml` é opcional e específico da interface Codex; não coloque instruções essenciais nele.
- Não crie cópias ou symlinks de `SKILL.md` para simular suporte. Documente o diretório de descoberta do runtime em `references/plataformas.md`.
- OpenCode, Codex, Gemini CLI e Google Antigravity devem funcionar com o mesmo conteúdo, salvo capacidades opcionais declaradas pelo runtime.

Não há stub gerado, pacote runtime ou sincronização automática nesta primeira versão. Não crie esses mecanismos até existir uma necessidade real e um contrato aprovado.

## Engenharia

- Escreva documentação em português brasileiro; preserve nomes de comandos, APIs, URLs, identificadores e termos técnicos quando necessário.
- Prefira fonte oficial primária, acesso público e coleta read-only.
- Registre URL, timestamp, jurisdição, consulta, fatos, limitações e frescor.
- Nunca armazene segredo, token, cookie, PII real ou dado de cliente.
- Nunca contorne login, CAPTCHA, assinatura, pagamento ou controle de acesso.
- Toda lógica não trivial precisa de um check ou teste executável.
- Use Spec Kit de forma proporcional ao risco; CI e verificação local continuam sendo autoridade de release.
- Use Orca para tarefas grandes ou paralelas; workers devem ter escopo, saída e limite explícitos.
- Não faça push, PR, merge, deploy ou ação externa sem autorização separada.

## Novo adapter

Leia `references/adapters.md`. Um adapter começa read-only, tem fonte e jurisdição explícitas, contrato de saída, falhas tipadas, fixture e revisão Orca. A pasta `adapters/` só deve ser criada quando o primeiro adapter for aprovado.

## Antes de editar

Inspecione o arquivo e seus links/callers, confirme que a mudança pertence a este repo, aplique o menor diff e rode a validação da skill creator:

```bash
python3 /home/hugocarvalho/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Se houver mudança de código, rode também o check nativo do projeto afetado. Não edite upstream, caches, generated output ou arquivos fora do escopo.
