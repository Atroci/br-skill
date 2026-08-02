# Plataformas compatíveis

## Contrato portátil

O pacote mínimo é uma pasta com `SKILL.md` na raiz e `references/` ao lado. Copie ou instale a pasta inteira. `SKILL.md` começa imediatamente com frontmatter YAML contendo `name` e `description`; não dependa de campos exclusivos de um fornecedor.

`agents/openai.yaml` serve somente para metadados de interface do Codex. OpenCode, Gemini CLI e Google Antigravity podem ignorá-lo sem perder comportamento.

## Matriz de descoberta

| Runtime | Projeto | Usuário | Recarga/verificação |
|---|---|---|---|
| OpenCode | `.opencode/skills/br-skill/` ou `.agents/skills/br-skill/` | `~/.config/opencode/skills/br-skill/` ou `~/.agents/skills/br-skill/` | reiniciar ou confirmar lista no tool `skill` |
| Codex | `.agents/skills/br-skill/` | `~/.agents/skills/br-skill/` | reiniciar sessão; validar com `quick_validate.py` |
| Gemini CLI | `.gemini/skills/br-skill/` ou `.agents/skills/br-skill/` | `~/.gemini/skills/br-skill/` ou `~/.agents/skills/br-skill/` | `/skills reload` e `/skills list` |
| Google Antigravity | `.agents/skills/br-skill/` | `~/.gemini/config/skills/br-skill/` | reiniciar conversa ou recarregar skills |

O diretório precisa conter o `SKILL.md` diretamente; não coloque uma camada extra como `br-skill/br-skill/SKILL.md`. Nomes devem ser minúsculos, com hífens, e coincidir com `name: br-skill`.

## Instalação

Depois que `Atroci/br-skill` existir:

```bash
# Gemini CLI
gemini skills install https://github.com/Atroci/br-skill

# Desenvolvimento local Gemini CLI
gemini skills link /caminho/para/br-skill --scope workspace
```

Para OpenCode, Codex e Antigravity, instale a mesma pasta inteira em um dos diretórios da matriz. O alias compartilhado `.agents/skills/br-skill/` é a opção de projeto mais portátil entre os quatro.

## Capacidades opcionais

O conteúdo funciona como instrução e pesquisa read-only sem ferramenta adicional. Orca, MCP, navegador, login e scripts não são pressupostos. Se o runtime não oferecer uma capacidade, mantenha a entrega em `lookup` ou `prepare`, registre a limitação e peça handoff humano antes de `submit`.

Não use `agents/openai.yaml` para configurar ferramentas, permissões ou segredos. Cada runtime mantém esses controles fora da skill.

## Check de publicação

Antes de publicar ou instalar:

1. Rode `python3 /home/hugocarvalho/.codex/skills/.system/skill-creator/scripts/quick_validate.py .` na raiz.
2. Confirme que `SKILL.md`, `references/` e links relativos existem.
3. Abra uma sessão nova ou recarregue skills no runtime.
4. Verifique que `br-skill` aparece na lista e que uma tarefa jurídica/imobiliária aciona a descrição correta.
5. Confirme que nenhuma credencial, PII ou fixture real entrou no pacote.
