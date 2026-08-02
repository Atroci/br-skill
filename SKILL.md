---
name: br-skill
description: "Skill portátil em português brasileiro para OpenCode, Codex, Gemini CLI e Google Antigravity: mapear, projetar e revisar fluxos de sites, dados públicos, jurídico e mercado imobiliário no Brasil. Use quando a tarefa envolver fontes oficiais brasileiras, legislação, jurisprudência, imóveis, cadastros, localização, adaptação cultural de site ou criação de adapters com aprovação e evidência."
---

# BR Skill

## Objetivo

Orientar trabalho localizado para o Brasil sem transformar pesquisa em aconselhamento jurídico, prova registral ou ação externa automática. A skill separa fonte, contexto, adapter, evidência e aprovação.

## Roteamento

Leia somente a referência necessária antes de agir:

- `references/plataformas.md`: instalação, descoberta e limites por runtime.
- `references/arquitetura.md`: camadas, contexto, Center, Moat e limites do upstream.
- `references/brasil-juridico.md`: fontes, jurisdição e limites para fluxos jurídicos.
- `references/brasil-imobiliario.md`: imóveis, cadastro, mercado e localização no Brasil.
- `references/adapters.md`: contrato e checklist para adicionar adapter.
- `references/spec-kit-orca.md`: Spec Kit, níveis de risco e orquestração Orca.

## Fluxo padrão

1. Identifique o runtime e carregue a pasta inteira da skill; não dependa de `agents/openai.yaml` fora do Codex.
2. Classifique domínio, UF/município, usuário, dados pessoais e se o pedido é `lookup`, `prepare` ou `submit`.
3. Leia a referência de domínio e escolha fonte oficial primária.
4. Verifique acesso: público, API, login, CAPTCHA, pagamento, assinatura ou outro limite.
5. Produza envelope de evidência com URL, data/hora, jurisdição, consulta, fatos e limitações.
6. Pare antes de envio, pagamento, cancelamento, assinatura, autenticação ou alteração externa sem aprovação explícita.
7. Valide resultado, frescor da fonte, idioma `pt-BR`, formato brasileiro e próximos passos.

## Regras duras

- Não invente fatos, cobertura territorial, disponibilidade, prazo ou garantia jurídica.
- Não trate resultado de busca, anúncio, CIB, cadastro ou avaliação como prova de propriedade, matrícula, certidão ou direito.
- Não contorne CAPTCHA, login, identidade, assinatura, controle de acesso ou limite do site.
- Não leia, imprima, grave ou peça segredo em texto; use o cofre aprovado e valide apenas presença.
- Não faça submissão, pagamento, lance, contratação, protocolo ou cancelamento sem aprovação explícita no ponto de ação.
- Se fonte estiver bloqueada, desatualizada ou ambígua, declare `indisponível`, `desconhecida` ou `precisa de validação`; não faça fallback silencioso.
- Trabalho jurídico é pesquisa e preparação de evidência, não parecer ou aconselhamento profissional.
- Orca, MCP, navegador e scripts são capacidades opcionais do runtime; se não existirem, declare a limitação e mantenha o fluxo read-only.

## Sites brasileiros

Ao localizar site, preserve intenção e adapte exemplos, moeda, datas, CEP, UF, município, bairro, acentuação, acessibilidade, consentimento e linguagem. Confirme regras de negócio e fonte com o responsável; não traduza texto regulatório como se fosse orientação legal.

## Critério de conclusão

Uma entrega só está pronta quando registra fonte primária, momento da coleta, jurisdição, entradas, saída, limitações, gates de ação e verificação executada. Para código, inclua teste ou check mínimo executável e rode lint/build/teste apropriado.

Esta skill começa como documentação e contrato. Adapters executáveis entram somente após fonte, escopo, risco e teste read-only estarem aprovados.
