---
name: br-saude-perto
description: "Localizar, em modo somente leitura, UBS, hospitais, serviços do SUS e pontos do Farmácia Popular no Brasil usando fontes oficiais CNES/DATASUS ou Ministério da Saúde. Use quando o pedido exigir município/UF ou CEP, evidência temporal, status cadastral e do serviço, horários e distância com limitações explícitas."
---

# Saúde perto — Brasil

Localize serviços de saúde no Brasil sem transformar cadastro em promessa de atendimento. Use somente fontes oficiais e devolva evidência verificável, frescor e limitações.

## Fluxo

1. Exija `município + UF` ou `CEP` antes de consultar. Peça também a categoria (`UBS`, `hospital`, `serviço SUS` ou `Farmácia Popular`) e o serviço desejado, se houver. Não aceite localização vaga nem peça nome, CPF, CNS, senha ou outro dado pessoal.
2. Escolha a fonte primária:
   - [CNES/DATASUS — consulta de estabelecimentos](https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=cnes) para UBS, hospitais e registros de serviços SUS.
   - [DATASUS](https://datasus.saude.gov.br/) quando a consulta ou o arquivo oficial do CNES for disponibilizado por esse portal.
   - [Ministério da Saúde — Farmácia Popular](https://www.gov.br/saude/pt-br/composicao/sectics/daf/farmacia-popular) e sua lista oficial vigente para pontos credenciados.
3. Faça consulta pontual e read-only. Registre a URL exata consultada; não use snippet de busca, agregador, avaliação, mapa ou diretório privado como prova. Se a fonte exigir autenticação, bloquear acesso ou não permitir confirmar o registro, declare `blocked`/`auth_required`/`unknown` em vez de fazer fallback silencioso.
4. Filtre pelo município/UF informado e confira o registro correspondente. Separe cadastro, oferta declarada e disponibilidade atual: CNES ativo não prova que a unidade está aberta, que há vaga, equipe, estoque, plantão ou atendimento sem agendamento; participação no Farmácia Popular não prova estoque nem horário atual.
5. Para cada resultado, preserve os campos abaixo. Use `unknown` quando a fonte não informar; nunca complete por inferência.

## Saída obrigatória

Entregue primeiro um resumo curto e depois um registro por local:

```yaml
consulta:
  municipality: "município informado"
  uf: "UF informada | unknown"
  cep: "informado | não informado"
  categoria: "UBS | hospital | serviço SUS | Farmácia Popular"
  source_url: "URL oficial exata"
  retrieved_at: "YYYY-MM-DDThh:mm:ssZ"
  effective_at: "data de referência/publicação do registro | unknown"
  jurisdiction: "Brasil > UF > município"
resultados:
  - name: "nome como publicado"
    address: "endereço como publicado | unknown"
    source_url: "URL oficial exata do registro"
    cnes_id: "número CNES | unknown | não aplicável"
    cnes_status: "status publicado | unknown | não aplicável"
    service_status: "status do serviço/programa publicado | unknown"
    services: ["serviços explicitamente publicados"]
    opening_hours: "horário explicitamente publicado | unknown"
    distance_km: "valor | unknown"
    distance_method: "linha reta/Haversine, rota publicada ou unknown"
    limitations: ["limitações específicas desta distância e fonte"]
    status: "found | no_result | blocked | auth_required | unknown"
```

`effective_at` é a data do registro ou da lista, não substitua por `retrieved_at` quando a fonte não informar a vigência. `jurisdiction` deve refletir o alcance real do dado. `opening_hours` deve repetir o horário publicado; se ausente, escreva `unknown`, sem inferir horário comercial.

Calcule distância apenas quando houver pontos de origem e destino confiáveis: prefira distância em linha reta/Haversine e rotule-a como tal; use distância de rota somente se a própria fonte oficial a publicar. Com município sem ponto de origem, coordenadas ausentes ou geocodificação não verificável, use `distance_km: unknown`. Informe sempre método, precisão da origem e limitações; não chame um local de “mais próximo” quando a comparação não for equivalente.

## Limites de segurança

- Não diagnostique, faça triagem, recomende tratamento ou interprete resultado clínico.
- Não agende, cancele, autentique, envie formulário, faça pagamento ou altere cadastro.
- Não raspe em massa, contorne CAPTCHA/controle de acesso ou use credenciais, cookies, tokens, segredos ou PII.
- Não alegue cobertura nacional, disponibilidade em tempo real, gratuidade, estoque, vaga ou atendimento sem agendamento sem evidência explícita.
- Se não houver resultado, diferencie `no_result` de fonte bloqueada ou dado desatualizado e declare a limitação.
