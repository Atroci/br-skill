---
name: br-remedio-seguro
description: "Comparar, em fontes oficiais brasileiras, registro e alertas ou recolhimentos da Anvisa e tetos de preço da CMED para o medicamento exato por princípio ativo, concentração, forma e embalagem. Usar em consultas read-only de situação regulatória, segurança publicada ou preço máximo permitido; não usar para orientação clínica, compra, autenticação ou ação externa."
---

# Remédio seguro BR

## Objetivo

Produzir uma comparação factual e rastreável entre a consulta de registro do medicamento na Anvisa, alertas ou recolhimentos aplicáveis e a lista oficial de preços da CMED. Trabalhar somente com fontes públicas, leitura read-only e jurisdição brasileira; não transformar o resultado em orientação médica, jurídica ou comercial.

## Identificar o medicamento sem inferir

Antes de consultar, obter e repetir a identidade exata:

- princípio ativo completo, incluindo sal, éster ou hidrato quando informado;
- concentração ou dose por unidade/volume;
- forma farmacêutica e apresentação (por exemplo, comprimido, solução ou injetável);
- quantidade da embalagem;
- nome comercial, fabricante ou titular e número de registro, se fornecidos;
- Brasil e, para preço, UF e alíquota de ICMS quando necessárias.

Não tratar mesmo princípio ativo e dose como a mesma apresentação. Não escolher outra concentração, forma, quantidade, marca, laboratório ou sal para preencher lacunas. Se faltar um campo que impeça a correspondência, solicitar o dado ou retornar `manual_review`/`unsupported`; não adivinhar.

## Fluxo de consulta

1. Consultar o registro no [serviço oficial da Anvisa](https://www.gov.br/anvisa/pt-br/sistemas/consulta-a-registro-de-medicamentos). Conferir princípio ativo, concentração, forma, apresentação, titular, número e situação do registro. `no_result` significa apenas que não houve correspondência na consulta realizada; não afirmar “não registrado” sem escopo e fonte suficientes.
2. Consultar [Alertas da Anvisa](https://consultas.anvisa.gov.br/) e notícias ou atos oficiais de suspensão e recolhimento. Pesquisar o princípio ativo, produto, titular, apresentação e, se houver, lote. Conferir se a medida é alerta, suspensão, recolhimento voluntário ou determinado, quais lotes e qual data. “Nenhum resultado” não exclui alerta quando a consulta estiver bloqueada, incompleta ou sem cobertura declarada.
3. Consultar a [lista de preços da CMED](https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos) e a [orientação oficial de consulta](https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos/como-consultar/como-consultar-as-listas). Usar a edição vigente na data da análise, ou a edição histórica correspondente à data solicitada. Filtrar princípio ativo ou medicamento, concentração, forma e quantidade; confirmar fabricante quando houver homônimos.
4. Para venda ao consumidor, reportar o `PMC` (Preço Máximo ao Consumidor) e a alíquota de ICMS/UF da linha correspondente. Usar `PF` ou `PMVG` somente quando a lista e o contexto oficial indicarem que são o teto aplicável. Não calcular ou substituir um preço ausente com outra coluna.

Não usar agregador, anúncio, farmácia, snippet de busca, marketplace, bula não oficial ou resposta de outro agente como autoridade. Podem ajudar a localizar uma fonte, mas cada fato deve ser revalidado e citado pela fonte oficial primária.

## Contrato de evidência

Registrar uma linha por fonte consultada, inclusive quando houver bloqueio ou ausência de resultado. Preencher todos os campos abaixo; usar `não aplicável` com justificativa, nunca deixar campo vazio:

| Campo | Exigência |
| --- | --- |
| `source_url` | URL exata da página, consulta, ato ou arquivo oficial que sustenta o fato. |
| `source_type` | `anvisa_registry`, `anvisa_alert`, `anvisa_recall` ou `cmed_price`. |
| `retrieved_at` | Data e hora da coleta em ISO 8601, com fuso. |
| `effective_at` | Data, mês da edição ou intervalo em que registro, alerta ou preço produz efeito; marcar `unknown` quando a fonte não informar. |
| `jurisdiction` | `Brasil`; para CMED, incluir UF e ICMS quando relevantes; para alerta, indicar escopo nacional ou restrito. |
| `alert_date` | Data de publicação ou vigência do alerta, ou `não aplicável` com justificativa. |
| `recall_date` | Data do recolhimento voluntário/determinado, ou `não aplicável` com justificativa. |
| `freshness` | `fresh`, `aging`, `stale` ou `unknown`, sempre com motivo e relação entre `retrieved_at` e `effective_at`. |
| `uncertainty` | `none`, `low`, `medium` ou `high`, com a causa: correspondência parcial, lote ausente, fonte bloqueada, data ausente ou conflito. |

Para alertas e recolhimentos, conservar também produto, titular, lote, medida e data publicada. Para CMED, conservar edição, tipo de preço, valor, moeda, alíquota e linha correspondente. Não inventar um prazo universal de frescor: justificar a classificação com a data ou com a limitação observável.

## Separar teto CMED de preço varejista

Manter dois fatos independentes:

- `preco_teto_cmed`: valor oficial da linha da CMED, tipo (`PMC`, `PF` ou `PMVG`), edição e `effective_at`;
- `preco_varejo_observado`: valor visto em estabelecimento ou cotação pública, com estabelecimento, URL, `observed_at`, embalagem e condições.

O teto é limite regulatório, não promessa de preço de venda. O varejo pode cobrar menos; não preencher preço observado a partir do teto nem chamar `PMC` de “preço atual”. Só comparar os dois quando embalagem, UF/ICMS, moeda e período forem compatíveis. Se o preço observado estiver acima do teto, relatar “possível divergência a verificar” com evidência; não acusar infração. Sem observação independente, declarar `preco_varejo_observado: unavailable`.

## Limites obrigatórios

- Reportar somente status e fatos publicados; nunca recomendar iniciar, parar, trocar, ajustar ou suspender medicamento, dose ou tratamento.
- Não comprar, encomendar, autenticar ou avaliar lote físico, embalagem, foto, procedência ou falsificação.
- Não solicitar, armazenar ou imprimir nome de paciente, CPF, receita, histórico clínico, pedido, contato, credencial, cookie, token ou segredo. Mascarar/remover qualquer PII ou segredo recebido e não reproduzi-lo.
- Não contornar login, CAPTCHA, paywall ou controle de acesso. Se a fonte falhar, marcar `blocked`, `auth_required`, `stale`, `no_result` ou `manual_review` conforme o caso, informar a URL e o que ficou desconhecido.
- Nunca fazer fallback silencioso para fonte secundária, edição antiga ou outro medicamento. Conflito entre fontes exige preservar ambas, apontar a divergência e marcar revisão manual.

## Formato de saída

Entregar, em PT-BR, nesta ordem:

1. **Alvo exato**: identidade e jurisdição consultadas.
2. **Anvisa — registro**: correspondência, situação e evidência.
3. **Anvisa — alertas/recolhimentos**: correspondência por produto/lote, datas, escopo e evidência; separar ausência de resultado de fonte bloqueada.
4. **CMED — teto**: `PMC`/`PF`/`PMVG`, valor, edição, UF/ICMS e `effective_at`.
5. **Varejo observado**: somente se houver evidência independente; manter separado do teto.
6. **Frescor, incerteza e limitações**: listar campos desconhecidos, bloqueios, conflitos e o que não pode ser concluído.

Encerrar com a nota de escopo: “Informação regulatória e de preço; não substitui avaliação de profissional de saúde e não confirma autenticidade ou segurança de uma unidade física.”
