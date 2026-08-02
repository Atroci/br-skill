# Domínio imobiliário brasileiro

## Escopo

Esta referência cobre descoberta pública, localização, dados cadastrais e séries de mercado. Anúncio, cadastro, mapa, preço de referência ou resultado do Sinter não prova propriedade, matrícula, ônus, posse, regularidade, valor de venda ou disponibilidade atual.

## Fontes oficiais de partida

| Fonte | Uso inicial | Limite |
|---|---|---|
| [CIB — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/perguntas-frequentes/cadastros/cib) | entender cadastro e identificação de imóvel | CIB não substitui cartório nem matrícula |
| [Sinter — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/sinter/cib) | contexto de integração cadastral | cobertura e campos precisam ser conferidos |
| [Consultar imóveis no Sinter — gov.br](https://www.gov.br/pt-br/servicos/consultar-imoveis-no-sinter?id=12870&origem=servico) | consulta por mapa/filtros, quando disponível | campos exibidos e autenticação devem ser confirmados por endpoint; não é certidão ou prova registral |
| [Banco Central — mercado imobiliário](https://dadosabertos.bcb.gov.br/dataset/informacoes-do-mercado-imobiliario) | séries e indicadores públicos | indicador agregado não avalia imóvel individual |
| [IBGE — Banco de Nomes Geográficos](https://www.ibge.gov.br/geociencias/metodos-e-outros-documentos-de-referencia/vocabulario-e-glossarios/42080-banco-de-nomes-geograficos-do-brasil.html?lang=pt-BR) | normalização de nomes geográficos | nome normalizado não confirma endereço registral |
| [Caixa — imóveis à venda](https://www.caixa.gov.br/voce/habitacao/imoveis-venda/Paginas/default.aspx) | descoberta de listagens, editais e regras públicas | oferta, login, proposta, comissão e leilão exigem handoff |

Fontes municipais, estaduais, cartórios e portais de leilão devem ser adicionados por jurisdição, com URL oficial verificada e data de coleta. Não crie um adapter nacional genérico baseado em sites de terceiros.

Consulta pública não autoriza presumir acesso a dados pessoais ou a todos os dados cadastrais. Classifique cada endpoint e campo separadamente: `public` somente para conteúdo explicitamente público; `auth_required` ou `manual_review` quando houver identidade, login, restrição de perfil ou dúvida sobre a base legal. Nunca registre CPF, nome de titular ou outro dado pessoal sem necessidade, finalidade e proteção documentadas.

## Matriz inicial de capacidades

| Adapter planejado | Capacidade inicial | Acesso | Estado |
|---|---|---|---|
| `sinter-imoveis` | `lookup` | público somente para campos/fluxos explicitamente públicos; confirmar endpoint | contrato a definir |
| `ibge-localidades` | `lookup` | público | contrato a definir |
| `bcb-mercado-imobiliario` | `lookup` | dados abertos | contrato a definir |
| `caixa-imoveis` | `lookup` e preparação de comparação | público; ação exige login | não enviar proposta |

## Localização brasileira

Use `pt-BR`, UF, município, bairro, logradouro, número, complemento, CEP, lote, quadra, matrícula, cartório/RI, CIB e área em `m²` quando presentes. Datas de apresentação podem usar `dd/mm/aaaa`; payloads devem manter ISO 8601 e número decimal com ponto. Exiba moeda como `R$` e registre se o valor é pedido, avaliação, série agregada ou outro tipo.

Registre timezone da coleta. `America/Sao_Paulo` é uma convenção operacional comum, mas a data/hora exibida deve preservar o instante e não presumir que todo município tenha a mesma necessidade de apresentação.

## Envelope de consulta

```yaml
uf: SP
municipio: exemplo
logradouro: opcional
cep: opcional e minimizado
identificador: cib, código ou referência pública, se houver
source: https://fonte-oficial.example
retrieved_at: 2026-08-02T00:00:00Z
data_class: cadastro | mercado | listagem | localização
result: fatos observáveis
limitations:
  - o que a fonte não prova
next_action: certidão, profissional ou consulta oficial específica
```

## Gates imobiliários

Não faça lance, proposta, pagamento, download autenticado, compra de certidão, assinatura ou alteração de cadastro. Handoff humano é obrigatório para matrícula/certidão, ônus, identidade, financiamento, arrematação, comissão, visita, contrato e qualquer decisão financeira.
