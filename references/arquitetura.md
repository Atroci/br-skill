# Arquitetura e contexto

## Decisão inicial

O `k-skill` upstream mostra um ecossistema amplo: diretórios de skills, manifestos, instruções, stubs gerados, runtime compartilhado, browser, proxy e CI. Ele também separa perfis de acesso e impõe gates para login, CAPTCHA, pagamento e submissão. Isso é contexto de mapeamento, não uma licença para copiar estrutura ou conteúdo específico.

`br-skill` começa menor: uma skill raiz, referências brasileiras e contrato de adapter. Só adiciona runtime, pacote, scripts ou dezenas de skills quando houver caso de uso, fonte e teste que justifiquem isso.

## Camadas

```text
interface       -> SKILL.md e metadados do runtime
distribuição    -> pasta portátil e diretórios de descoberta por runtime
roteamento      -> domínio, jurisdição, dado, capacidade e risco
contexto        -> referências PT-BR e fontes oficiais
center          -> contratos comuns, evidência, gates e falhas
moat            -> adaptação brasileira: idioma, jurisdição, taxonomia e fontes
adapters        -> integração isolada por fonte e domínio, somente após fixture
orquestração    -> Spec Kit + Orca para trabalho paralelo revisável
entrega         -> teste, revisão, aprovação e publicação
```

## Center e Moat

**Center** é o núcleo comum: envelope de evidência, produtor versus agregador, estados `lookup|prepare|submit`, frescor, falhas, segurança e aprovação. A sequência mínima é `entrada → fonte → evidência → falha`; não é um pipeline obrigatório nem um runtime.

**Moat** é a vantagem localizada: PT-BR natural, UF e município, vocabulário de matrícula/RI/CIB/CEP, GTFS e transporte por operador, CLT/PJ/estágio, diferenças de tribunais e cartórios, fontes governamentais, consentimento e handoff brasileiro. Moat não significa raspar tudo nem prometer cobertura nacional.

Regra: nova lógica só vai para o Center se pelo menos dois adapters precisarem dela sem exceções locais e dois casos reais/fixtures confirmarem o mesmo comportamento. Regra: particularidade de uma fonte fica no adapter ou em referência de domínio. Isso evita um núcleo genérico que apaga diferenças brasileiras.

## Estrutura atual

```text
br-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── arquitetura.md
│   ├── plataformas.md
│   ├── brasil-juridico.md
│   ├── brasil-imobiliario.md
│   ├── brasil-gtfs.md
│   ├── carreira-br.md
│   ├── adapters.md
│   ├── council-adapter.md
│   ├── mcp-brasil.md
│   ├── roldao-method.md
│   ├── governanca-seguranca.md
│   └── spec-kit-orca.md
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── .gitignore
```

`adapters/` ainda não existe de propósito. Criá-la antes do primeiro contrato aprovado seria scaffolding sem necessidade.

`SKILL.md` na raiz é a unidade de distribuição. OpenCode, Codex, Gemini CLI e Google Antigravity podem descobrir a mesma pasta por seus diretórios nativos ou pelo alias compartilhado `.agents/skills`; não mantenha variantes por fornecedor. O conteúdo essencial permanece em Markdown e referências relativas à raiz do pacote.

## Mapa de contexto

1. Pedido do usuário: objetivo, público, jurisdição e capacidade.
2. Referência geral: regras de segurança, evidência e aprovação.
3. Referência de domínio: jurídico, imobiliário ou site.
4. Adapter: comportamento específico da fonte.
5. Contexto privado: somente no ambiente autorizado; nunca entra no repo público.

Segredos, PII, cookies, documentos de cliente, prompts internos e dados operacionais pertencem ao ambiente privado, não a esta skill pública.

## Fonte de verdade e engenharia

| Camada | Fonte | Pode ser gerada? |
|---|---|---|
| Comportamento | `SKILL.md` | não |
| Interface | `agents/openai.yaml` | não nesta fase |
| Conhecimento | `references/*.md` | não sem fonte |
| Adapter | futuro `adapters/<id>/` | não; código + teste são a verdade |
| Estado privado | ambiente do operador | nunca no repo |

Cada fonte deve ter acesso e frescor verificáveis. Quando uma página exigir autenticação ou estiver bloqueada, o resultado é uma falha declarada ou handoff, não um fallback silencioso.

## Fontes auxiliares e autoridade

MCP Brasil pode ajudar a descobrir APIs e organizar chamadas, mas é um projeto independente e agregador. MobilityData pode catalogar GTFS, mas o produtor oficial define arquivo, licença e frescor. Council pode organizar dissent e próximos passos, mas não cria evidência. Roldão informa contratos e checks, mas não justifica copiar hooks, agentes ou uma nova hierarquia de skills. Em todos os casos, a fonte primária e o timestamp continuam no envelope.

## Relação com o upstream

| Padrão observado no upstream | Decisão brasileira |
|---|---|
| Muitas skills em diretórios planos | Começar com uma skill raiz e referências por domínio |
| `skill.json` + `instruction.md` + stub gerado | Não copiar pipeline; adotar somente se runtime futuro exigir |
| Browser/proxy/action profiles | Modelar acesso e capacidade no contrato antes de implementar |
| Descoberta pública e fallbacks | Fonte oficial primária, estado de falha tipado e sem bypass |
| CI de pacote | `quick_validate.py` agora; testes de adapter depois |

## Portabilidade

O contrato é Markdown e funciona como instrução nos quatro runtimes. OpenCode, Codex, Gemini CLI e Google Antigravity podem carregar a mesma pasta, mas não se presume suporte nativo a Council, MCP, hooks, navegador ou bloqueio automático. Se uma capacidade faltar, registrar a limitação e continuar read-only; nunca fingir que uma barreira textual foi enforcement técnico.

## Limites de escala

O primeiro corte mapeia arquitetura e contrato. Não inclui catálogo completo do upstream, catálogo nacional de tribunais, integração autenticada, crawler genérico, pacote npm, servidor MCP, DuckDB, dashboard ou bridge executável. Esses itens entram apenas com problema concreto, fonte autorizada, repetição e gate de risco.
