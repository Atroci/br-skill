# Contribuindo

Leia `SKILL.md`, `AGENTS.md` e as referências de domínio antes de propor mudança. Escreva em português brasileiro, com exemplos brasileiros reais apenas quando forem públicos, redigidos e necessários.

## Nova skill de workflow

1. Defina nome, usuário, domínio, jurisdição, capacidade (`lookup`,
   `prepare` ou `submit`) e o que fica fora.
2. Leia o envelope e o router; não crie rota duplicada nem carregue toda a
   biblioteca em cada workflow.
3. Rode `init_skill.py <id> --path skills` e substitua o template por
   instruções PT-BR concisas, fonte primária, estados, frescor, limitações e
   handoff.
4. Mantenha somente `skills/<id>/SKILL.md` e
   `skills/<id>/agents/openai.yaml` quando não houver script ou referência
   material necessária. Não crie README, adapter ou stub de runtime sem caso
   concreto.
5. Rode `quick_validate.py skills/<id>`, `.github/scripts/check_skill.py` e
   `git diff --check`. Para mudança compartilhada no router/envelope, adicione
   fixture ou check que cubra a rota.
6. Use Orca para revisão paralela quando o escopo justificar; `worker_done`
   prova somente a task delegada, não autoriza merge, push ou ação externa.

## Novo adapter

1. Declare domínio, UF/município, fonte oficial, licença e classe de acesso.
2. Defina se a capacidade é `lookup`, `prepare` ou `submit`.
3. Especifique entradas, saída, frescor, limites e falhas esperadas.
4. Comece com fixture read-only e teste de contrato.
5. Documente o que não é possível fazer e qualquer handoff humano.
6. Rode `quick_validate.py`, checks do adapter e revisão read-only via Orca.
7. Só depois solicite aprovação para ação externa, publicação ou integração autenticada.

## Padrão de mudança

- Não copie skill, prompt, referência ou credencial do upstream.
- Não invente endpoint, cobertura, prazo, decisão jurídica ou disponibilidade de imóvel.
- Não adicione dependência para resolver tarefa que a biblioteca padrão ou o runtime já resolve.
- Não edite `SKILL.md` para esconder uma limitação; atualize a referência e o teste.
- Mudança de alto risco deve ter `spec`, `plan` e `tasks` proporcionais ao risco, conforme `references/spec-kit-orca.md`.
- Mantenha commits pequenos e não publique sem autorização explícita.

## Como pedir ajuda

Abra uma issue com objetivo, domínio, jurisdição, fonte pretendida, evidência observada, resultado esperado e o que está bloqueado. Remova tokens, cookies, PII, dados de cliente e documentos restritos. Para vulnerabilidade, use canal privado do mantenedor em vez de issue pública.
