---
name: menor-preco-br
description: "Comparar cestas de compras no Brasil com preços observados em fontes públicas oficiais do Menor Preço Brasil ou fontes estaduais compatíveis. Use para comparar produtos por preço, pacote, EAN, loja, distância, custo de deslocamento e frescor, preservando evidência e limites de acesso."
---

# Menor Preço Brasil

Comparar uma cesta sem transformar preço publicado em garantia de disponibilidade. Priorizar consulta pública, read-only e fonte primária; não inventar endpoint, cobertura ou preço.

## Fluxo

1. Fixar localidade (UF, município, endereço ou raio), data/hora da consulta, quantidade, marca/variante, tamanho e unidade de cada item.
2. Priorizar o Menor Preço Brasil oficial. Usar fonte estadual somente quando o órgão responsável, jurisdição, acesso público/read-only e termos de uso estiverem claros.
3. Consultar a fonte sem alterar dados. Registrar URL/domínio, operador, jurisdição, consulta, termos/licença e horário observado em ISO 8601 com fuso.
4. Comparar somente correspondências exatas e calcular a cesta com os campos obrigatórios abaixo.
5. Expor limitações, frescor e confiança junto do resultado; não fazer fallback silencioso para agregador, anúncio ou fonte não autorizada.

## Correspondência exata

- Tratar EAN/GTIN idêntico como requisito quando disponível. Sem EAN, exigir título, marca, variante, quantidade, peso/volume e unidade compatíveis.
- Não substituir unidade, tamanho, sabor, marca, versão, item avulso por multipack ou produto parecido. Se não houver match exato, não estimar: marcar `manual_review`.
- Separar preço unitário, quantidade solicitada e subtotal. Declarar promoções, condições, retirada/entrega e validade quando a fonte publicar.

## Resultado obrigatório

Registrar, para cada item e opção de compra:

- produto, pacote/unidade, EAN/GTIN, quantidade, preço unitário e subtotal;
- comerciante somente quando nome/endereço forem públicos na fonte; caso contrário, `não divulgado`;
- número de lojas consultadas e número de lojas com correspondência exata;
- distância e método (rota/linha reta), quando disponível, mais custo de deslocamento informado ou calculado; não tratar distância como custo;
- subtotal da cesta, custo de deslocamento, taxas explicitamente incluídas/excluídas e `total_da_cesta`;
- URL/domínio, operador/jurisdição, termos de uso/licença e limitações da fonte;
- `observado_em`, `atualizado_em`/validade da fonte quando disponíveis e avaliação de frescor.

Calcular `subtotal_da_cesta = soma(preço_unitário × quantidade)` e `total_da_cesta = subtotal_da_cesta + custo_de_deslocamento`. Comparar uma única loja apenas quando todos os itens tiverem match exato nela; para cesta dividida, listar lojas e deslocamentos separadamente. Não incluir entrega, pedágio, estacionamento ou tarifa sem valor observável.

## Frescor e confiança

- Comparar `observado_em` com `atualizado_em`/validade e termos da fonte. Se o limite de frescor não estiver publicado, dizer `frescor desconhecido` e reduzir a confiança.
- Classificar `alta` quando EAN/pacote são exatos, preço e local são públicos e a observação é recente; `média` quando falta um desses sinais sem afetar o match; `baixa` quando há dado antigo, incompleto ou condição não verificável. `baixa` não sustenta recomendação sem `manual_review`.
- Explicar a razão da confiança e nunca apresentar disponibilidade futura como fato.

## Acesso, autenticação e estados

- Se GOV.BR ou fonte estadual pedir login, CPF, MFA, CAPTCHA, certificado, assinatura ou outro controle, parar e marcar `auth_required`. Orientar o usuário a concluir o acesso na própria sessão e retornar apenas resultado permitido; nunca pedir, guardar ou reutilizar credenciais, tokens, cookies ou códigos.
- Sem caminho público compatível, fonte indisponível ou termos que não permitam a consulta: marcar `blocked` e explicar o bloqueio.
- Match ambíguo, comerciante não público, frescor/termos incertos ou custo de viagem não verificável: marcar `manual_review`.
- Nunca contornar login/MFA/CAPTCHA, raspar área autenticada ou espelhar/comercializar dataset. Não assumir que “público” significa licença para redistribuição.
