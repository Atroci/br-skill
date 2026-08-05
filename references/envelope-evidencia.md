# Envelope de evidência

Contrato comum do Center. Workflows podem acrescentar campos de domínio, mas
não podem remover proveniência, frescor, jurisdição, limitações ou estado de
acesso.

## Contrato mínimo

    capability: lookup | prepare | submit
    status: ok | no_result | stale | blocked | auth_required | manual_review | unsupported
    request:
      intent: "pedido normalizado"
      jurisdiction: "BR | UF | município | desconhecida"
      inputs: {}
    source:
      provider: "produtor ou arquivo"
      source_url: "URL exata ou local-only"
      source_role: official_producer | catalog | aggregator | user_file
      retrieved_at: "ISO 8601 com fuso"
      effective_at: "vigência/data de referência | unknown"
      access_mode: public | api-key | login | payment | signature | local-only
      terms_url: "URL dos termos | unknown"
    result:
      facts: []
      calculations: []
      inferences: []
      confidence: high | medium | low | unknown
    limitations: []
    handoff:
      required: false
      reason: "passo humano ou unknown"
    privacy:
      contains_pii: false
      retention: none | local-only | approved-storage
      redactions: []

## Regras

1. Registrar retrieved_at no momento da leitura; não usar esse campo para
   inventar effective_at.
2. Marcar como unknown o que a fonte não publica. Não converter ausência de
   resultado em ausência do fato.
3. Separar facts da matemática reproduzível em calculations e da leitura do
   agente em inferences.
4. Usar official_producer para o produtor primário. Catálogo, MCP, anúncio,
   busca e agregador podem orientar descoberta, mas não sustentam sozinhos uma
   conclusão material.
5. Preservar blocked, auth_required e manual_review; nunca fazer fallback
   silencioso.
6. submit exige handoff explícito e aprovação no ponto de ação. Nenhum
   workflow desta onda envia, paga, assina, protocola, agenda ou altera dados.
7. Não armazenar segredo, cookie, token, CPF, CNPJ completo, chave Pix,
   documento de saúde ou relatório financeiro. Redigir antes de exibir ou
   persistir; para dados locais, usar local-only e retenção mínima.

## Estado não é resultado

- no_result: consulta acessível, sem correspondência na fonte consultada.
- stale: houve resultado, mas frescor ou vigência não sustenta uso atual.
- blocked: a fonte ou caminho foi impedido.
- auth_required: a próxima etapa exige login legítimo do usuário.
- manual_review: conflito, licença, cobertura, correspondência ou risco que
  o workflow não resolve.
- unsupported: entrada, formato ou capacidade fora do contrato.

O router deve carregar o SKILL.md específico depois de classificar domínio,
jurisdição, capacidade e risco. O resultado final deve incluir o envelope ou
apontar explicitamente para o campo equivalente do workflow.
