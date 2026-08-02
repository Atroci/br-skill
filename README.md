# BR Skill

Skill independente para trabalho localizado no Brasil: sites, fontes públicas, pesquisa jurídica, dados imobiliários e adapters revisáveis.

O repositório é inspirado no mapa técnico de [`NomaDamas/k-skill`](https://github.com/NomaDamas/k-skill), mas não é fork nem cópia do conteúdo coreano. O upstream serve apenas como referência arquitetural. Esta versão começa com um contrato pequeno, documentação em PT-BR e fontes brasileiras.

## Estado

- caminho local: `www/projects/br-skill/`
- branch inicial: `main`
- remoto: [Atroci/br-skill](https://github.com/Atroci/br-skill), público, `main` em `5ea2e9d`
- adapters executáveis: ainda não implementados
- prioridade: fontes oficiais, leitura read-only, evidência e aprovação humana

## Uso local

Durante desenvolvimento, carregue a pasta inteira pelo caminho local conforme o runtime utilizado. Não copie apenas `SKILL.md`: as referências são parte do contrato. Para instalação pública:

```bash
npx --yes skills add https://github.com/Atroci/br-skill --skill br-skill -g
```

O remoto e o commit inicial já foram publicados; confirme a versão instalada antes de usar em produção.

## Compatibilidade

O pacote usa o formato aberto `SKILL.md` com `name` e `description`, sem frontmatter específico de fornecedor. Assim, a mesma pasta pode ser instalada nos quatro runtimes:

| Runtime | Descoberta local | Escopo global |
|---|---|---|
| OpenCode | `.opencode/skills/br-skill/` ou `.agents/skills/br-skill/` | `~/.config/opencode/skills/br-skill/` ou `~/.agents/skills/br-skill/` |
| Codex | `.agents/skills/br-skill/` | `~/.agents/skills/br-skill/` |
| Gemini CLI | `.gemini/skills/br-skill/` ou `.agents/skills/br-skill/` | `~/.gemini/skills/br-skill/` ou `~/.agents/skills/br-skill/` |
| Google Antigravity | `.agents/skills/br-skill/` | `~/.gemini/config/skills/br-skill/` |

Leia [`references/plataformas.md`](references/plataformas.md) para comandos de instalação, recarga e limites. `agents/openai.yaml` é apenas metadado de interface do Codex; os outros runtimes ignoram-no.

## Mapa rápido

- [`SKILL.md`](SKILL.md): instrução carregada pelo agente.
- [`references/arquitetura.md`](references/arquitetura.md): camadas, contexto, Center, Moat e relação com o upstream.
- [`references/plataformas.md`](references/plataformas.md): instalação e descoberta em OpenCode, Codex, Gemini CLI e Antigravity.
- [`references/brasil-juridico.md`](references/brasil-juridico.md): pesquisa jurídica e fontes oficiais.
- [`references/brasil-imobiliario.md`](references/brasil-imobiliario.md): imóveis, cadastro, localização e mercado.
- [`references/adapters.md`](references/adapters.md): contrato e processo para novos adapters.
- [`references/spec-kit-orca.md`](references/spec-kit-orca.md): Spec Kit e Orca por nível de risco.
- [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) e [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md): engenharia e colaboração.

## O que entra depois

1. Um adapter jurídico read-only com fonte oficial e fixture.
2. Um adapter imobiliário read-only com escopo territorial explícito.
3. Testes de contrato, frescor e falhas; só depois browser handoff ou ação autenticada.

Não entram por padrão: parecer jurídico, prova de titularidade, bypass de controles, submissão automática, lance, pagamento, assinatura ou uso de dado pessoal sem base e autorização.

## Fontes brasileiras de partida

- [LGPD — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)
- [Código de Processo Civil — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm)
- [Justiça 4.0 — CNJ](https://www.cnj.jus.br/tecnologia-da-informacao-e-comunicacao/justica-4-0/)
- [Legislação aplicada — STJ](https://processo.stj.jus.br/SCON/legaplic/)
- [CIB — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/perguntas-frequentes/cadastros/cib)
- [Consultar imóveis no Sinter — gov.br](https://www.gov.br/pt-br/servicos/consultar-imoveis-no-sinter?id=12870&origem=servico)
- [Mercado imobiliário — Banco Central](https://dadosabertos.bcb.gov.br/dataset/informacoes-do-mercado-imobiliario)
- [Banco de Nomes Geográficos — IBGE](https://www.ibge.gov.br/geociencias/metodos-e-outros-documentos-de-referencia/vocabulario-e-glossarios/42080-banco-de-nomes-geograficos-do-brasil.html?lang=pt-BR)
- [Imóveis à venda — Caixa](https://www.caixa.gov.br/voce/habitacao/imoveis-venda/Paginas/default.aspx)
