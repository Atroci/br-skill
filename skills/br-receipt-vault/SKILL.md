---
name: br-receipt-vault
description: "Organizar localmente recibos, NF-e e NFC-e fornecidos pelo usuário: classificar campos, normalizar comerciante, produto, preços e datas, preservar incertezas, derivar categorias, criar candidatos a lembretes de garantia e devolução e manter histórico pessoal de gastos. Usar apenas dados e arquivos locais fornecidos; acionar para leitura, conferência ou resumo fiscal pessoal sem rede, login, pagamento, declaração ou envio de dados."
---

# Cofre de Recibos BR

## Limite operacional

- Aceitar somente texto, imagem, PDF, XML, JSON ou CSV fornecido pelo usuário e disponível localmente.
- Processar tudo localmente. Não chamar APIs, navegador, serviços externos ou adapters; não fazer login, upload, pagamento, declaração fiscal ou alteração em sistema de terceiros.
- Não ler `.env`, chaves, cookies, backups ou outros arquivos fora do escopo. Não alterar arquivos na raiz do repositório, router ou infraestrutura.
- Não registrar, imprimir, incluir em log, telemetria, nome de arquivo, argumento de comando ou resposta qualquer CPF, CNPJ, chave de acesso fiscal, QR code, token, credencial ou PII. Redigir o valor inteiro como `[REDACTED:tipo]` antes de persistir ou exibir.
- Manter o arquivo original intacto. Escrever somente o artefato local explicitamente pedido; se não houver caminho, devolver apenas uma saída sanitizada.

## Fluxo

1. **Delimitar e redigir.** Confirmar caminho e formato local; separar dados fiscais da PII; redigir identificadores antes de mostrar ou copiar trechos.
2. **Classificar.** Identificar `recibo`, `nf-e`, `nfc-e` ou `desconhecido` somente quando o documento sustentar a classificação. Marcar cada campo como `source`, `normalized`, `derived`, `uncertain`, `sensitive` ou `missing`.
3. **Extrair com proveniência.** Guardar o caminho relativo sanitizado, tipo de arquivo e localização da evidência (página, linha, coluna ou campo). Registrar `retrieved_at` como o instante local de leitura, em ISO 8601 com fuso; registrar `effective_at` como a data/hora de emissão impressa, ou `null` quando ausente.
4. **Normalizar sem inventar.** Preservar o valor de origem não sensível e o valor canônico; não corrigir conflito silenciosamente.
5. **Resolver incertezas.** Manter candidatos, alternativas e conflitos. Nunca fundir comerciantes, produtos ou documentos apenas por semelhança; usar `manual_review: true` quando houver dúvida.
6. **Derivar com base explícita.** Categorizar itens, propor lembretes e agregar histórico somente a partir dos dados fornecidos e das regras do usuário.
7. **Conferir.** Comparar soma de itens, descontos e total do documento; sinalizar divergências, possíveis duplicatas e datas ausentes para revisão, sem alterar o valor de origem.

## Classificação e normalização

- **Comerciante:** manter `merchant_source` somente se for nome empresarial não sensível; gerar `merchant_normalized` removendo espaços duplicados, pontuação incidental e variação evidente de caixa, preservando acentos. Não usar CPF/CNPJ para matching.
- **Produto:** manter `product_source` não sensível; gerar `product_normalized` com espaços, unidade e quantidade coerentes. Preservar SKU/GTIN apenas se não forem segredo; não transformar descrição ambígua em produto específico.
- **Preço:** converter `1.234,56` para número decimal em BRL com duas casas; separar quantidade, preço unitário, desconto e total do item quando a fonte permitir. Não converter moeda nem estimar centavos ausentes.
- **Data:** normalizar para `YYYY-MM-DD` ou data/hora ISO 8601. Preferir a data de emissão do documento; distinguir `effective_at` da leitura local `retrieved_at`.
- **Identificadores fiscais e PII:** classificar como `sensitive`, redigir integralmente e conservar apenas o tipo do campo e sua presença. Não armazenar fragmentos, hashes, XML bruto, linha digitável ou URL de QR code.
- **Campo ausente:** usar `null`, `field_status: missing`, `confidence: baixa` e `manual_review: true`; não preencher com data atual, preço médio ou suposição.

Use confiança ordinal, sem falsa precisão:

- `alta`: valor legível e sustentado por uma única evidência clara ou por evidências concordantes;
- `média`: normalização plausível, mas com abreviação, OCR ou pequena divergência;
- `baixa`: candidato, conflito, truncamento ou inferência; sempre exigir revisão manual.

## Contrato de saída

Produzir estrutura local sanitizada com estes campos mínimos; ampliar somente quando a fonte justificar:

```json
{
  "document_kind": "nfc-e",
  "effective_at": "2026-08-05T14:20:00-03:00",
  "retrieved_at": "2026-08-05T17:30:00+01:00",
  "merchant": {
    "merchant_source": "Nome da loja",
    "merchant_normalized": "Nome da Loja",
    "field_status": "normalized",
    "confidence": "alta",
    "manual_review": false
  },
  "items": [
    {
      "product_source": "Descrição impressa",
      "product_normalized": "Descrição normalizada",
      "quantity": 1,
      "unit_price_brl": 12.5,
      "total_price_brl": 12.5,
      "category": "alimentação",
      "category_basis": "produto e comerciante da fonte",
      "confidence": "média",
      "manual_review": true
    }
  ],
  "totals": {
    "document_total_brl": 12.5,
    "items_total_brl": 12.5,
    "reconciled": true
  },
  "provenance": {
    "source_file": "dados/recibo-01.pdf",
    "source_type": "pdf",
    "source_locator": "página 1, bloco de itens",
    "redactions": ["cpf", "cnpj", "chave-fiscal", "qr-code"]
  },
  "reminders": [],
  "spending_history": {}
}
```

`merchant_source` e `product_source` só podem conter texto não sensível. Se um trecho misturar PII, substituir o trecho inteiro por marcador e registrar a redação em `provenance.redactions`.

Para qualquer match incerto, usar em vez de descartar ou escolher silenciosamente:

```json
{
  "match_status": "candidato",
  "selected": null,
  "alternatives": ["produto A", "produto B"],
  "reason": "descrição truncada na fonte",
  "confidence": "baixa",
  "manual_review": true
}
```

## Categorias, lembretes e histórico

- Categorizar somente com evidência de produto/comerciante ou regra fornecida pelo usuário. Preferir `alimentação`, `casa`, `transporte`, `saúde`, `educação`, `vestuário`, `eletrônicos`, `serviços`, `lazer`, `assinaturas`, `impostos-taxas` e `outros`.
- Manter `category_basis`, `confidence` e `manual_review` por item. Usar `outros` e revisão manual quando houver mais de uma categoria plausível; não inferir finalidade pessoal a partir de PII.
- Criar lembretes como candidatos, não como conclusão jurídica: `guardar_comprovante`, `verificar_devolução` ou `verificar_garantia`. Definir `due_at` somente quando a fonte ou uma regra explícita do usuário fornecer prazo; caso contrário, usar `null`, `basis`, confiança baixa e revisão manual.
- Agregar histórico pessoal apenas localmente, por mês de `effective_at`, comerciante e categoria: total em BRL, quantidade de itens/documentos e fontes incluídas. Não enriquecer com dados externos, não fazer previsão financeira e não incluir identificadores fiscais ou PII.
- Ao suspeitar de duplicata, manter ambos os registros com `possible_duplicate_of`, fonte e revisão manual; não somar nem apagar até confirmação.

## Resultado seguro

Antes de entregar, verificar que a saída não contém CPF, CNPJ, chave fiscal, QR code, credencial, token, endereço, telefone, e-mail ou outro dado pessoal não necessário; que cada documento tem `source_file`, `retrieved_at`, `effective_at`, `confidence` e `manual_review`; e que toda categoria, normalização, soma ou lembrete derivado aponta sua base. Se não puder cumprir o limite local, parar e pedir arquivo já redigido.
