# Estágio e cursos gratuitos BR — fontes e contrato

## Escopo

Referência para descoberta e comparação read-only de vagas de estágio,
aprendizagem e cursos gratuitos no Brasil. Não automatiza coleta, cadastro,
candidatura ou matrícula. Revalidar cada oferta na página exata no momento do
uso.

**Mapa verificado em:** `2026-08-05T15:12:51+01:00` (Europe/Lisbon).

## Limite entre estágio e curso livre

A [Lei nº 11.788/2008](https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11788.htm)
define estágio como ato educativo escolar supervisionado. Os requisitos incluem
matrícula e frequência regular nas modalidades previstas, termo de compromisso
entre estudante, concedente e instituição de ensino, além de compatibilidade das
atividades. O artigo 5º permite agentes de integração e veda cobrar do estudante
pelos serviços ali descritos.

Curso livre, MOOC ou certificado isolado não substitui vínculo estudantil. A
[Aprenda Mais](https://aprendamais.mec.gov.br/mod/page/view.php?id=134111)
declara que seus cursos gratuitos não equivalem a curso técnico, graduação ou
pós-graduação e não geram vínculo para estágio.

Registrar esses pontos como requisitos publicados, não como parecer jurídico ou
decisão individual de elegibilidade. Dúvida material vai para instituição de
ensino, concedente ou agente de integração responsável.

## Fontes para estágio e aprendizagem

Estas fontes são pontos de descoberta. O anúncio exato e a página oficial da
empresa ou órgão continuam necessários para verificar vaga, prazo e
legitimidade.

| Fonte | URL inicial | Papel | Evidência observada em 2026-08-05 | Limite |
|---|---|---|---|---|
| CIEE | <https://portal.ciee.org.br/> | `catalog` | portal de vagas de estágio e aprendizagem | acesso e oferta variam por perfil; confirmar anúncio e empresa |
| IEL Carreiras | <https://carreiras.iel.org.br/> | `catalog` | busca por estado, local, tipo, curso e modalidade | disponibilidade varia por UF e data; confirmar página da vaga |
| Nube | <https://www.nube.com.br/estudantes/painel_vagas/> | `catalog` | vagas de estágio e aprendizagem; cadastro estudantil anunciado como gratuito | candidatura pode exigir conta; confirmar anúncio, empresa e regras atuais |

Tratar `terms_url` e licença como `UNKNOWN` até abrir e registrar os termos
vigentes da fonte usada. Não criar provider automático a partir desta tabela.

## Fontes para cursos gratuitos

| Fonte | URL inicial | Papel | Evidência observada em 2026-08-05 | Limite |
|---|---|---|---|---|
| Aprenda Mais — MEC | <https://aprendamais.mec.gov.br/> | `catalog` | cursos on-line, abertos e gratuitos, com certificado para concluintes | curso livre; matrícula no portal não gera vínculo para estágio |
| Escola Virtual Gov | <https://www.escolavirtual.gov.br/catalogo> | `catalog` | catálogo de cursos autoinstrucionais gratuitos com certificado | confirmar público, disponibilidade e regra de aprovação na página do curso |
| Fundação Bradesco — Escola Virtual | <https://www.ev.org.br/cursos> | `official_producer` | cursos livres gratuitos e on-line; certificado conforme regra do curso | não afirmar reconhecimento pelo MEC; confirmar prazo e avaliação |
| SENAI | <https://www.senai.portaldaindustria.com.br/> | `catalog` | catálogo nacional inclui ofertas marcadas como gratuitas | nem todo curso é gratuito; preço, modalidade e vagas variam por estado/oferta |

“Gratuito” deve ser confirmado na oferta exata. Certificado pode depender de
conclusão, avaliação, nota ou prazo; ausência de informação vira `UNKNOWN`.

## Entrada normalizada

```yaml
intent: estagio | aprendiz | curso_gratuito | trilha
query: texto
area: texto | UNKNOWN
education_level: medio | tecnico | superior | outro | UNKNOWN
enrollment_status: regular | nao_regular | UNKNOWN
location:
  municipality: texto | UNKNOWN
  uf: sigla | UNKNOWN
modality: presencial | hibrido | remoto | EAD | qualquer | UNKNOWN
availability: texto | UNKNOWN
certificate_required: true | false | UNKNOWN
```

Minimizar dados. `enrollment_status` pode ser informado pela pessoa, mas não
deve ser comprovado por documento durante `lookup` ou `prepare`.

## Verificação por resultado

Para vaga de estágio/aprendizagem, registrar:

- título, organização anunciada e URL canônica;
- curso/nível/semestre aceitos ou `UNKNOWN`;
- município + UF, modalidade, jornada e prazo ou `UNKNOWN`;
- bolsa, benefícios e requisitos somente como publicados;
- fonte original, data da leitura e estado do link/candidatura;
- conflitos entre catálogo, empresa e edital.

Para curso, registrar:

- nome, instituição ofertante e URL da oferta;
- gratuidade explícita, modalidade, carga horária e prazo;
- público, pré-requisitos, regra de conclusão e certificado;
- classificação declarada: curso livre, MOOC, formação continuada ou outra;
- custo, reconhecimento ou elegibilidade não estabelecidos como `UNKNOWN`.

## Estados e handoff

- `ok`: página exata acessível e campos materiais citados.
- `no_result`: consulta acessível sem correspondência aos filtros.
- `stale`: oferta encontrada, mas prazo/frescor não sustenta uso atual.
- `blocked`: fonte impediu leitura pública.
- `auth_required`: detalhes ou próxima etapa exigem conta legítima.
- `manual_review`: conflito, custo ambíguo, termos desconhecidos ou possível
  cobrança indevida.
- `unsupported`: pedido exige inscrição, candidatura automática ou capacidade
  fora do contrato.

Handoff mínimo: URL exata, campos já verificados, campos a confirmar e ação
humana única. Não carregar CPF, documento, senha, cookie ou dado acadêmico para
o repositório, relatório público ou fixture.
