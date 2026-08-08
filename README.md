# BR Skill

Skill independente para trabalho localizado no Brasil: sites, fontes públicas, pesquisa jurídica, dados imobiliários e adapters revisáveis.

O repositório é inspirado no mapa técnico de [`NomaDamas/k-skill`](https://github.com/NomaDamas/k-skill), mas não é fork nem cópia do conteúdo coreano. O upstream serve apenas como referência arquitetural. Esta versão começa com um contrato pequeno, documentação em PT-BR e fontes brasileiras.

## Estado

- caminho local: `www/projects/br-skill/`
- branch inicial: `main`
- remoto: [Atroci/br-skill](https://github.com/Atroci/br-skill), público; base local desta onda: `d6d9afb`
- adapter executável: validator GTFS Schedule local/sintético em `adapters/gtfs_static/`; não consulta feed real
- workflows PT-BR read-only e fluxo local de propostas freelance sob `skills/`, selecionados por `routers/roteador-brasil.md`
- prioridade: fontes oficiais, leitura read-only, evidência, PT-BR e aprovação humana

## Uso local

Durante desenvolvimento, carregue a pasta inteira pelo caminho local conforme o runtime utilizado. Não copie apenas `SKILL.md`: as referências são parte do contrato. Para instalação pública:

```bash
npx --yes skills add https://github.com/Atroci/br-skill --skill br-skill -g
```

O remoto e o commit inicial já foram publicados; confirme a versão instalada antes de usar em produção.

## Uso rápido para freelance

Carregue a pasta inteira e informe plataforma, fonte, perfil autorizado e operação. Use `lookup` para ler, organizar e pontuar, `prepare` para redigir e revisar, e `submit` somente para uma ação aprovada.

```text
Organize e pontue estas URLs públicas da plataforma X com meu perfil local. Não envie nada.
```

```text
Gere um draft para opportunity_id platform:123. Use apenas provas autorizadas, preço condicionado e prazo sustentado.
```

```text
Mostre a fila de review. Depois da minha aprovação explícita para platform:123 e draft_version 2, faça handoff ou submit permitido e pare se houver bloqueio.
```

O resultado deve separar fatos, inferências e desconhecidos, registrar estado local redigido e mostrar limitações. Score não autoriza envio.

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
- [`routers/roteador-brasil.md`](routers/roteador-brasil.md): router por domínio, jurisdição, capacidade e risco.
- [`references/envelope-evidencia.md`](references/envelope-evidencia.md): contrato comum de resultado e handoff.
- [`skills/`](skills/): workflows portáteis, cada um com `SKILL.md` e metadados opcionais do Codex.
- [`references/arquitetura.md`](references/arquitetura.md): camadas, contexto, Center, Moat e relação com o upstream.
- [`references/plataformas.md`](references/plataformas.md): instalação e descoberta em OpenCode, Codex, Gemini CLI e Antigravity.
- [`references/brasil-juridico.md`](references/brasil-juridico.md): pesquisa jurídica e fontes oficiais.
- [`references/brasil-imobiliario.md`](references/brasil-imobiliario.md): imóveis, cadastro, localização e mercado.
- [`references/brasil-gtfs.md`](references/brasil-gtfs.md): feeds GTFS brasileiros localizados e checks de transporte.
- [`references/carreira-br.md`](references/carreira-br.md): contrato amplo de carreira BR, CLT/PJ e revisão humana.
- [`references/estagio-cursos-br.md`](references/estagio-cursos-br.md): fontes e contrato para estágio, aprendizagem e cursos gratuitos.
- [`references/adapters.md`](references/adapters.md): contrato e processo para novos adapters.
- [`references/council-adapter.md`](references/council-adapter.md): síntese Council com dissent e evidência preservados.
- [`references/mcp-brasil.md`](references/mcp-brasil.md): mapa do MCP Brasil e contrato opcional runtime-neutral.
- [`references/roldao-method.md`](references/roldao-method.md): regra de promoção de skills e checks mínimos.
- [`references/governanca-seguranca.md`](references/governanca-seguranca.md): CI, PR, issues, segurança e gates.
- [`references/spec-kit-orca.md`](references/spec-kit-orca.md): Spec Kit e Orca por nível de risco.
- [`references/fluxo-progressivo.md`](references/fluxo-progressivo.md): prompts PT-BR e fluxo progressivo para os quatro runtimes.
- [`references/skillopt.md`](references/skillopt.md): SkillOpt como inspiração controlada para evoluir instruções.
- [`references/propostas-freela.md`](references/propostas-freela.md): contrato portátil para oportunidades, drafts, envio aprovado e aprendizado local.
- [`references/ecossistema-brasil.md`](references/ecossistema-brasil.md): mapa Council, ganhos, lacunas e rejeições por upstream.
- [`adapters/gtfs_static/README.md`](adapters/gtfs_static/README.md): contrato e limites do validator GTFS offline.
- [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) e [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md): engenharia e colaboração.

## Onda atual

- implementar workflows reais sem confundir instrução portátil com adapter executável;
- manter workflows de descoberta em modo read-only, com fontes, timestamps e limites explícitos;
- mapear fontes e contratos sem prometer cobertura nacional;
- separar catálogo, produtor oficial e arquivo atual;
- manter Council, MCP e Orca como capacidades auxiliares, nunca como autoridade;
- aplicar fluxo progressivo com Spec Kit opcional, gates Orca e verificação CI;
- executar CI leve em PR/push; branch protection e required checks continuam configuração separada do repositório.

## O que entra depois

1. `br-housing-compare`, `br-mobility` e `br-job-match` como workflows delimitados.
2. Adapter de consulta BrasilAPI/IBGE/CEP com fonte, frescor e fixture explícitos.
3. Adapter GTFS read-only com produtor autorizado, termos e arquivo atual; sem assumir tempo real.
4. Adapters jurídico e imobiliário read-only, cada um com jurisdição e fixture explícitas.
5. Testes de contrato, frescor e falhas; só depois browser handoff ou ação autenticada.

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
