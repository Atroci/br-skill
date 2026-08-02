# Roldão Method — mapa para br-skill

## Decisão

`roldao-method` é referência de engenharia brasileira, não base para copiar seu framework. O que entra em `br-skill` é um contrato mínimo e observável:

`entrada → fonte → evidência → falha`

Esse contrato declara capacidade (`lookup`, `prepare` ou `submit`), estado, `FACT/INFERENCE/ASSUMPTION/UNKNOWN`, non-goals, proveniência, fixture e gate humano. A skill continua Markdown-first, runtime-neutral e read-only.

Fonte consultada: [`roldaobatista/roldao-method`](https://github.com/roldaobatista/roldao-method/tree/main), consultada em `2026-08-02`. O repositório menciona agentes, workflows, skills, addons, hooks, LGPD, Pix, NF-e e eSocial; menções e contagens do upstream não são cobertura nem certificação para este pacote.

## O que adotar

- regra de três: um padrão recorrente pode virar skill somente depois de três casos independentes e comparáveis;
- non-goals, IDs e rastreabilidade `spec → story → task → commit` quando mais de um domínio realmente precisar deles;
- fixtures sintéticas válidas, inválidas e ambíguas;
- check offline pequeno, usando stdlib/runtime já disponível;
- aceite por tarefa observável, não por número de hooks, agentes ou arquivos;
- documentação PT-BR clara, fonte de verdade única e CI reproduzível.

## O que adaptar

| Padrão upstream | Adaptação BR Skill |
|---|---|
| agentes e workflows por comando | fases Orca supervisionadas; instrução textual quando o runtime não suporta subagente |
| hooks bloqueadores | gates documentados e CI portátil; enforcement técnico só quando comprovado |
| regras com IDs | IDs somente quando ajudam a ligar evidência, tarefa e decisão |
| addons com vários artefatos | promoção futura após três artefatos coesos e necessidade repetida |
| métrica de tarefas | três a cinco tarefas reais, cada uma com saída verificável e limite explícito |

## O que rejeitar nesta fase

Não portar a CLI, a árvore inteira de agents/workflows, hooks Claude-only, addon framework, contagens de cobertura, dependências runtime, scraping, mutação externa ou claims legais/fiscais prontos. LGPD, CLT, Pix, NF-e, eSocial e qualquer obrigação regulatória precisam de fonte atual, jurisdição e revisão profissional; o nome de um template não é norma.

Não criar `skills/<dominio>/` só para parecer modular. A pasta `references/` existente é suficiente até o contrato aparecer em dois domínios sem exceções locais.

## Fases de promoção

1. **Contrato:** registrar entrada, fonte, evidência, falha, capacidade, estado e non-goals em Markdown.
2. **Falsificação:** adicionar fixture redigida e um check offline que diferencie `blocked` de `no_result` e preserve `UNKNOWN`.
3. **Promoção:** somente após três casos independentes, tarefa observável, revisão Orca e funcionamento textual nos quatro runtimes. Um adapter executável exige ainda fonte autorizada, teste read-only e aprovação separada.

## Kill criteria

Parar se a abstração apagar uma diferença de domínio, se um check transformar ausência em `false`, se a fonte não puder ser citada, se uma fixture contiver PII/segredo, se um hook for tratado como portabilidade garantida ou se o fluxo induzir login, submissão, pagamento ou mutação.

## Labels

- **FACT:** afirmação suportada pelo repositório de referência ou por uma fonte citada.
- **INFERENCE:** decisão de recorte para `br-skill`.
- **ASSUMPTION:** condição que precisa ser testada no runtime ou em tarefa real.
- **UNKNOWN:** contagem, compatibilidade, benchmark, cobertura ou regra não comprovada.
