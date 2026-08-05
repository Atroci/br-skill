---
name: br-money-decisions
description: "Apoiar decisões financeiras no Brasil com dados oficiais e abertos do Banco Central, em modo somente leitura. Usar para explicar ou comparar cenários de Selic, PTAX, IPCA/inflação e taxas médias de crédito, com cálculo reproduzível, datas, fontes e limitações; não usar para movimentar dinheiro, recomendar investimento ou empréstimo como aconselhamento, autenticar contas ou registrar dados financeiros e PII."
---

# Decisões financeiras BR

Prestar apoio analítico, em PT-BR e somente leitura, para perguntas financeiras brasileiras. Usar dados oficiais abertos do Banco Central do Brasil (BCB), preservar o contexto temporal e mostrar como cada resultado foi obtido.

## Fluxo

1. Defina a `reference_date` pedida (data ou período) antes de buscar dados. Não substitua por `retrieved_at`.
2. Identifique `institution_product` (instituição e produto; por exemplo, banco e linha de crédito). Se faltar, marque `UNKNOWN` e peça o dado; não atribua uma taxa macro a uma instituição.
3. Busque primeiro fonte primária pública do BCB: [Dados Abertos](https://dadosabertos.bcb.gov.br/), [SGS](https://www3.bcb.gov.br/sgspub/) ou API/serviço oficial correspondente. Use a série/dataset exato e preserve sua unidade, frequência e definição.
4. Para Selic, PTAX, IPCA/inflação e taxas médias de crédito, registre o produtor indicado nos metadados. O IPCA pode ser produzido pelo IBGE e distribuído em série oficial do BCB; não esconda essa distinção.
5. Diferencie `effective_at` (quando o valor se aplica) de `retrieved_at` (quando foi consultado). Se a fonte estiver indisponível, atrasada ou inconsistente, retorne `stale`, `blocked` ou `manual_review`; não faça fallback silencioso.
6. Calcule com unidades explícitas e mostre a aritmética linha a linha. Arredonde apenas no resultado final, salvo regra da fonte.
7. Entregue o envelope abaixo em toda análise material:

```yaml
reference_date: "AAAA-MM-DD ou período"
institution_product: "instituição + produto; UNKNOWN se ausente"
jurisdiction: "BR ou escopo mais específico"
inputs:
  - name: "nome da série ou entrada"
    value: 0
    units: "BRL | USD | % | p.p. | dias | meses | anos"
    source_url: "https://..."
    retrieved_at: "AAAA-MM-DDThh:mm:ssZ"
    effective_at: "AAAA-MM-DD ou período"
formula: "fórmula simbólica"
arithmetic: "substituição numérica e resultado"
confidence: "high | medium | low"
limitations:
  - "cobertura, frescor, hipótese ou dado ausente"
```

## Cálculo e linguagem

- Marque cada afirmação como `FATO`, `CÁLCULO` ou `INFERÊNCIA`. `FATO` vem da fonte ou do usuário; `CÁLCULO` decorre da fórmula exibida; `INFERÊNCIA` é interpretação e deve ser proporcional à evidência.
- Declare a unidade em cada entrada e saída. Diferencie percentual de ponto percentual; nominal de efetivo; diário, mensal e anual; BRL de USD.
- Use fórmulas adequadas ao período e mostre a substituição. Exemplos:
  - variação: `((final - inicial) / inicial) × 100`;
  - taxa real no mesmo período: `((1 + nominal) / (1 + inflação)) - 1`;
  - conversão de taxa anual efetiva para mensal: `(1 + anual)^(1/12) - 1`, somente se as definições forem compatíveis.
- Não trate projeção, média histórica ou taxa de referência como promessa de preço, retorno, aprovação ou custo futuro. Se período, base, convenção ou composição não forem comparáveis, pare e declare a limitação.

## Limites obrigatórios

- Não mover dinheiro, efetuar pagamento, transferência, aplicação, contratação, cancelamento ou alteração de conta.
- Não autenticar, pedir credenciais, usar cookies ou acessar relatório financeiro privado.
- Não recomendar investimento, empréstimo ou produto como aconselhamento financeiro. Pode comparar cenários de modo descritivo, explicitar custos e encaminhar decisão a pessoa habilitada.
- Não armazenar nem registrar relatórios financeiros, PII, tokens ou segredos em arquivo, log, memória ou saída reutilizável. Remova ou generalize dados sensíveis antes de analisar.
- Se o pedido exigir ação, autenticação, dado privado ou recomendação personalizada, pare em `manual_review` e explique o limite.

## Saída mínima

Comece por `FATO`, depois `CÁLCULO` com aritmética e fórmula, e por fim `INFERÊNCIA` e `LIMITAÇÕES`. Termine com `confidence`, `source_url`, `retrieved_at`, `effective_at`, `jurisdiction` e o próximo passo humano quando houver `UNKNOWN`, `stale`, `blocked` ou `manual_review`.
