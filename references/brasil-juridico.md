# Domínio jurídico brasileiro

## Escopo

Esta referência cobre pesquisa, organização e preparação de evidência pública. Não produz parecer, estratégia processual, garantia de resultado, protocolo ou aconselhamento jurídico.

O Brasil exige separar legislação federal, atos locais, tribunal, ramo da Justiça, UF, município, classe processual, data de vigência e versão da fonte. “Lei brasileira” não é contexto suficiente para uma resposta operacional.

## Fontes oficiais de partida

| Fonte | Uso | Limite |
|---|---|---|
| [Planalto — LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm) | texto legal federal e proteção de dados | confirmar versão, vigência e norma aplicável |
| [Planalto — CPC](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm) | texto do Código de Processo Civil | não substitui análise do caso concreto |
| [CNJ — Justiça 4.0](https://www.cnj.jus.br/tecnologia-da-informacao-e-comunicacao/justica-4-0/) | mapa institucional e serviços de Justiça digital | não presume cobertura ou API de cada tribunal |
| [STJ — legislação aplicada](https://processo.stj.jus.br/SCON/legaplic/) | pesquisa de legislação aplicada no STJ | resultado não é parecer nem cobertura exaustiva |

Para lei estadual, tribunal, prefeitura, cartório ou órgão regulador, o adapter deve registrar fonte oficial específica da jurisdição. Não existe um endpoint nacional presumido nesta versão.

## Matriz inicial de capacidades

| Adapter planejado | Capacidade inicial | Acesso | Estado |
|---|---|---|---|
| `legislacao-planalto` | `lookup` | público | contrato a definir |
| `justica-cnj` | `lookup` | público, conforme serviço | contrato a definir |
| `jurisprudencia-stj` | `lookup` | público | contrato a definir |
| `tribunal-por-jurisdicao` | `lookup` ou `prepare` | varia | somente após fonte/UF definida |

Os nomes acima são planejamento, não módulos implementados.

## Envelope de evidência

```yaml
source: https://fonte-oficial.example
retrieved_at: 2026-08-02T00:00:00Z
jurisdiction: BR / UF / município / tribunal
query: texto ou parâmetros sem PII desnecessária
facts:
  - fato observável na fonte
limitations:
  - cobertura, vigência, autenticação ou ausência de resultado
capability: lookup
next_action: validação profissional ou handoff humano
```

`retrieved_at` é exemplo de formato; o adapter deve preencher o instante real. Não confunda data de publicação, data de vigência e data de coleta.

## Gates

- `lookup`: pode consultar conteúdo público e devolver evidência com link.
- `prepare`: pode organizar rascunho, campos e próximos passos, sem enviar.
- `submit`: fica fora da primeira fase; exige autorização explícita, autenticação legítima, confirmação final e auditoria.

Pare e peça validação quando houver identidade, sigilo, procuração, assinatura, custas, prazo processual, CAPTCHA, upload de documento, protocolo ou qualquer efeito jurídico externo.

## Dados pessoais e segurança

Trate CPF, RG, endereço residencial, processo sigiloso, saúde, dados financeiros e documentos como sensíveis até classificação contrária. Minimize entrada, redija fixtures, não grave resposta privada e não use dado real para “testar” adapter público.
