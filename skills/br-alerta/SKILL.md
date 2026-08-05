---
name: br-alerta
description: "Consultar e resumir alertas meteorológicos e de risco locais no Brasil em modo somente leitura, usando fontes oficiais do INMET, Cemaden e INPE/CPTEC. Use quando a pergunta pedir aviso, observação ou previsão para um CEP ou município e exigir proveniência, vigência, frescor e limitações."
---

# Alertas BR

## Escopo

Faça somente consultas locais, públicas e read-only. Entregue fatos publicados pela fonte, com URL e horários; não notifique pessoas, altere dados, acione serviços ou recomende uma ação operacional como se fosse autoridade pública.

Antes de consultar, exija pelo menos um alvo:

- `CEP` fornecido pelo usuário; ou
- `município + UF`.

Se o município for ambíguo, peça a UF. Não peça rua, número, nome, telefone, coordenadas ou outro dado pessoal. Não guarde o CEP nem tente identificar uma pessoa. Se não for possível vincular o CEP com segurança a um município, marque `jurisdiction: UNKNOWN` e peça município + UF; não use geocodificador de terceiro.

## Fontes oficiais

Use apenas páginas públicas do produtor e registre a URL exata consultada. Estes são pontos de partida; revalide o endereço e o conteúdo a cada consulta:

- **INMET** — avisos e previsão meteorológica: <https://portal.inmet.gov.br/> e <https://alertas2.inmet.gov.br/>.
- **Cemaden** — monitoramento, previsões e alertas de desastres: <https://www.gov.br/cemaden/pt-br/paginas/monitoramento> e <https://www.gov.br/cemaden/pt-br/paginas/sala-de-situacao>.
- **INPE/CPTEC** — previsão e monitoramento de tempo e clima: <https://www.gov.br/inpe/pt-br/acesso-a-informacao/perguntas-frequentes/principais-produtos-e-servicos-do-inpe/previsao-de-tempo-e-clima> e <https://www.cptec.inpe.br/>.

Não trate uma busca, agregador, rede social, notícia ou catálogo como fonte. Não faça scraping, crawler, automação de navegador, login, CAPTCHA, coleta de API não documentada ou contorno de bloqueio. Se a página estiver bloqueada, autenticada ou indisponível, registre `BLOCKED`/`AUTH_REQUIRED`/`UNKNOWN`; não converta a falha em `NO_RESULT` e não faça fallback silencioso.

## Classificação obrigatória

Cada registro recebe exatamente uma classe. Preserve o rótulo da fonte; identidade do órgão não transforma qualquer conteúdo em aviso.

- `AVISO_OFICIAL` (`official_warning`): a própria fonte publica aviso/alerta, área, severidade e janela de validade. Não inclua previsão ou observação nesta classe sem rótulo explícito.
- `OBSERVACAO` (`observation`): medição, estação, radar, satélite, chuva registrada ou monitoramento observado. Descreva o que foi registrado; não conclua risco futuro.
- `PREVISAO` (`forecast`): condição estimada para o futuro por previsão, modelo, boletim ou nowcasting. Não chame de aviso oficial só porque contém a palavra “alerta” em uma notícia ou previsão.
- `INFERENCIA_DO_AGENTE` (`agent_inference`): síntese ou hipótese derivada de dois ou mais fatos. Marque como inferência, liste os fatos que a sustentam e nunca apresente sua severidade, alcance ou conclusão como oficial.

INMET costuma fornecer avisos e previsões; Cemaden fornece monitoramento e produtos de alerta de desastres; INPE/CPTEC fornece previsão, monitoramento e nowcasting. Essas funções orientam a busca, não substituem a classificação publicada em cada página. Não compare ou some níveis de severidade de órgãos diferentes.

## Procedimento

1. Confirme `CEP` ou `município + UF` e o período pedido. Sem alvo, peça o dado que falta.
2. Consulte a página pública oficial adequada, manualmente e somente para leitura.
3. Copie fatos, rótulo, área e horários publicados. Não preencha lacunas por contexto, média histórica ou outra fonte.
4. Separe registros por fonte e classe. Uma inferência, se solicitada, vem depois dos registros oficiais e permanece explicitamente não oficial.
5. Verifique validade e frescor na hora da leitura. Se o horário de emissão, atualização ou validade não existir, use `UNKNOWN`.
6. Entregue o envelope abaixo. Toda resposta precisa conter `limitations` não vazio.

## Envelope de saída

Use estes campos, com datas ISO 8601 em UTC quando a fonte fornecer o horário. `UNKNOWN` é obrigatório quando o dado não estiver publicado ou não puder ser confirmado.

```yaml
status: OK | NO_RESULT | STALE | BLOCKED | AUTH_REQUIRED | UNKNOWN
target:
  cep: "<CEP fornecido> | UNKNOWN"
  municipality: "<município> | UNKNOWN"
  uf: "<UF> | UNKNOWN"
classification: AVISO_OFICIAL | OBSERVACAO | PREVISAO | INFERENCIA_DO_AGENTE
source: INMET | CEMADEN | INPE_CPTEC
source_url: "<URL exata da página consultada>"
retrieved_at: "<momento da leitura, UTC>"
effective_at: "<emissão/início de eficácia publicado pela fonte> | UNKNOWN"
jurisdiction: "<município/UF, região ou área publicada> | UNKNOWN"
severity: "<rótulo original da fonte> | UNKNOWN"
opening_at: "<abertura/início da janela de validade> | UNKNOWN"
expiry_at: "<expiração/fim da janela de validade> | UNKNOWN"
freshness: fresh | stale | unknown
facts:
  - "<fato textual curto, sem extrapolação>"
limitations:
  - "<cobertura, precisão local, horário ausente, bloqueio ou outra limitação>"
```

`retrieved_at` é quando o agente leu a página; `effective_at` é quando o produto passa a valer, se publicado; `opening_at` e `expiry_at` são a abertura e o fim da janela informada pela fonte. Não use `retrieved_at` para inventar vigência. `severity` deve repetir o nível original (por exemplo, cor ou nível do órgão), sem converter níveis entre órgãos; numa `INFERENCIA_DO_AGENTE`, use `UNKNOWN` e explique a derivação em `facts`/`limitations`.

Classifique `fresh` somente quando a fonte tiver horário/validade compatível com o momento da leitura; `stale` quando a validade expirou ou o próprio produto indica desatualização; `unknown` quando isso não puder ser verificado. Informe a idade ou o motivo em `limitations`.

## Limites

- Não invente cobertura municipal, severidade, horário, coordenada, causa, probabilidade ou impacto.
- Não transforme ausência de item em ausência de risco; `NO_RESULT` significa apenas que não houve item na fonte acessível e consultada para aquele alvo/período.
- Não esconda bloqueio, dado faltante ou divergência entre fontes. Mantenha cada estado explícito e inclua a URL consultada.
- Não crie adapters, scripts, dependências, roteadores ou integrações. Esta skill é instrução documental e não executa coleta automática.
- Não envie mensagens, e-mails, notificações, chamados ou publicações; não faça login nem use segredos.
- O resultado é informativo e não substitui a página oficial, a Defesa Civil local ou instrução de emergência vigente.
