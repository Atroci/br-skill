## Escopo

- O que muda:
- O que não muda:
- Arquivos ou áreas afetados:

## Evidência

- Fonte, URL, commit ou fixture:
- Data/hora da verificação:
- Resultado observado:
- Limitações ou pontos ainda não verificados:

## Jurisdição e contexto

- Domínio:
- UF/município ou outra jurisdição:
- Runtime e versão, quando relevante:

## PII e segredos

- [ ] Não incluí segredo, token, cookie, credencial, PII ou dado de cliente.
- [ ] Redigi ou substituí qualquer dado sensível usado para reproduzir o caso.
- [ ] Não incluí conteúdo de fonte restrita ou acesso não autorizado.

## Risco e gates

- Risco: `baixo` / `médio` / `alto`
- Capacidade afetada: `lookup` / `prepare` / `submit` / `não se aplica`
- Rollback ou reversão:
- Aprovação externa necessária? Qual gate:

## Checks

- [ ] `python3 .github/scripts/check_skill.py`
- [ ] `quick_validate.py .` no ambiente local da skill creator
- [ ] `git diff --check`
- Outros checks:

## Aprovação

- [ ] Escopo, evidência, jurisdição, risco e limitações foram revisados.
- [ ] A aprovação para merge é separada de push, deploy ou ação externa.
- Revisores:
