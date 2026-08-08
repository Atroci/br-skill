# Router Brasil

Router operacional da primeira onda do br-skill. Classificar intenção antes
de ler uma skill de domínio; carregar somente o workflow escolhido e o
envelope comum em references/envelope-evidencia.md.

## Classificação

Extrair quatro eixos:

1. Domínio: clima/risco, saúde, medicamento, dinheiro, compras, recibos,
   jurídico, imóvel, carreira, estágio/formação, freelance ou transporte.
2. Jurisdição: Brasil, UF, município, CEP, plataforma ou desconhecida.
3. Capacidade: lookup, prepare ou submit.
4. Risco: baixo, PII/local, autenticado, financeiro, saúde, jurídico ou
   efeito externo.

Se domínio ou jurisdição material estiverem ausentes, pedir somente o dado
necessário. Não adivinhar localização, identidade, cobertura ou intenção.

### Exemplos de pedido freelance

| Pedido | Capacidade | Operação | Saída esperada |
| --- | --- | --- | --- |
| “Organize estas URLs permitidas e remova duplicatas” | `lookup` | `discover` + `organize` | oportunidades locais com proveniência |
| “Compare estas oportunidades com meu perfil” | `lookup` | `score` | score explicado |
| “Escreva uma proposta para uma oportunidade pontuada” | `prepare` | `draft` | draft versionado |
| “Envie somente os IDs que aprovei” | `submit` | `review` + `submit` | handoff ou estado de envio por ID |

Score e draft não são autorização. Sem acesso permitido, adapter aprovado ou aprovação pontual, a rota termina em `manual_review`, `blocked`, `auth_required` ou `unsupported`.

## Rotas da primeira onda

| Intenção | Skill | Entradas mínimas | Saída/gate |
| --- | --- | --- | --- |
| alerta, chuva, enchente, fogo, deslizamento, calor | [br-alerta](../skills/br-alerta/SKILL.md) | CEP ou município + UF | alerta/observação/previsão separados; sem notificação automática |
| UBS, hospital, SUS, Farmácia Popular | [br-saude-perto](../skills/br-saude-perto/SKILL.md) | município + UF ou CEP; serviço | cadastro e status publicado; não promete vaga, estoque ou atendimento |
| registro, alerta, recolhimento ou teto de medicamento | [br-remedio-seguro](../skills/br-remedio-seguro/SKILL.md) | princípio ativo, dose, forma e embalagem | Anvisa/CMED; não é orientação clínica |
| Selic, PTAX, inflação, crédito, custo de parcelas | [br-money-decisions](../skills/br-money-decisions/SKILL.md) | data/período, produto e entradas | fatos + cálculo + inferência; não movimenta dinheiro nem aconselha |
| menor preço, cesta, EAN, lojas próximas | [menor-preco-br](../skills/menor-preco-br/SKILL.md) | itens exatos, local, quantidade e frescor | comparação read-only ou handoff de login; não replica dataset |
| recibo, NF-e, NFC-e, gasto, garantia, devolução | [br-receipt-vault](../skills/br-receipt-vault/SKILL.md) | arquivo local fornecido pelo usuário | processamento local, redaction e revisão manual |
| estágio, jovem aprendiz, primeira experiência, curso gratuito, curso livre, certificado | [br-estagio-cursos](../skills/br-estagio-cursos/SKILL.md) | intenção + área; município/UF ou remoto/EAD | descoberta/comparação read-only; candidatura e matrícula exigem handoff |
| escanear vagas, varrer portal, listar vagas de uma empresa, buscar vaga em massa no Brasil | [br-vagas-scanner](../skills/br-vagas-scanner/SKILL.md) | fonte pedida (empresa no Gupy, quadro, ou nome do catálogo) | vagas normalizadas com fonte/frescor/confiança; fontes fora do catálogo verificado ficam `manual_review` |
| freela, gig, bid, proposta, cliente de projeto, candidatura freelance | [br-proposal-agent](../skills/br-proposal-agent/SKILL.md) | plataforma/URL ou arquivo + perfil autorizado + operação | score e draft locais; envio exige aprovação por ID |

## Rotas existentes e próximas

| Intenção | Contexto | Limite atual |
| --- | --- | --- |
| imóvel, aluguel, condomínio, IPTU, matrícula, commute | [brasil-imobiliario.md](../references/brasil-imobiliario.md) | preparar pesquisa; anúncio não prova propriedade ou disponibilidade |
| lei, processo, tribunal, prazo, certidão | [brasil-juridico.md](../references/brasil-juridico.md) | pesquisa e evidência; não emitir parecer |
| vaga de emprego, CLT, PJ, candidatura de emprego | [carreira-br.md](../references/carreira-br.md) + [carreira-scanner-br.md](../references/carreira-scanner-br.md) | descoberta/deduplicação; submissão exige handoff; scanner cobre só Gupy e Programathor nesta rodada |
| linha, parada, horário, GTFS, ônibus | [brasil-gtfs.md](../references/brasil-gtfs.md) | separar Schedule, RT, calendário e cobertura; adapter atual é sintético |

Essas rotas não fingem que existe skill executável ou cobertura nacional. Se
não houver workflow adequado, retornar manual_review/unsupported e apontar
o contexto que falta.

## Sequência segura

1. Normalizar pedido, idioma pt-BR, localização e unidade.
2. Escolher rota e ler SKILL.md correspondente.
3. Escolher fonte primária ou contrato da plataforma; registrar URL, produtor, termos, jurisdição e
   timestamps.
4. Produzir resultado com estado explícito e limitações não vazias.
5. Parar antes de login, CAPTCHA, upload, pagamento, assinatura, protocolo,
   agendamento, compra, notificação ou outra alteração externa.
6. Se a ação for autorizada em etapa posterior, entregar handoff com os
   campos necessários; não transformar lookup em submit.

## Fallback

Não usar um agregador, MCP, Council, busca web ou resposta de outro agente para
substituir fonte primária. Eles podem organizar descoberta ou dissent; a
evidência final continua dependente do produtor. Se a fonte não abrir, manter
blocked, auth_required ou unknown e informar o próximo passo humano.
