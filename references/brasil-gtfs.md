# Transporte público no Brasil — contrato GTFS

**Status:** referência read-only; não cria adapter executável. **Coleta do mapa:** `2026-08-02` (Europe/Lisbon). **Escopo:** registros `location.country_code=BR` e `data_type=gtfs` localizados no catálogo MobilityData/Mobility Database; não é inventário nacional.

O catálogo é diretório. O produtor oficial define arquivo, licença e periodicidade; o arquivo atual só existe depois de baixar bytes autorizado e registrar hash/frescor. `urls.latest` do catálogo é espelho, não prova de atualidade. A ausência de GTFS-RT no catálogo consultado é `no_result` do catálogo, não prova de ausência no Brasil.

Fontes do padrão: [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/), [GTFS Realtime Reference](https://gtfs.org/documentation/realtime/reference/) e [MobilityData catalog](https://github.com/MobilityData/mobility-database-catalogs). Fontes oficiais de produtor são indicadas na coluna própria; todos os links precisam ser rechecados na consulta.

## Feeds estáticos localizados

| ID | Operador/cobertura | Status observado | Produtor ou acesso | Licença/frescor/limite |
|---|---|---|---|---|
| `mdb-7` | EPTC — Porto Alegre/RS e região; ônibus | MDB `inactive`; validade observada 2025-09-12–2025-12-13 | [arquivo EPTC](https://dadosabertos.poa.br/dataset/1fe9c2c1-9fbe-48ea-841b-61e30597ecd6/resource/b3bce61f-78ee-49eb-be57-6236d82bd5e0/download/outputfiles.zip) · [dataset](https://dadosabertos.poa.br/dataset/gtfs) | CC BY declarado; feed expirado na data do mapa; não tratar como atual |
| `mdb-8` | SPTrans — São Paulo/SP e entorno; ônibus, metrô e trem | MDB `active`; `is_official=true` | [download SPTrans](https://www.sptrans.com.br/umbraco/Surface/PerfilDesenvolvedor/BaixarGTFS?memberName=sptrans) · [desenvolvedores](https://www.sptrans.com.br/desenvolvedores/) | termos de uso do cadastro; licença formal `UNKNOWN`; Olho Vivo é API separada, não GTFS-RT catalogado |
| `mdb-9` | BHTRANS convencional — Belo Horizonte/MG e RMBH; ônibus | MDB `active` | [recurso CKAN](https://ckan.pbh.gov.br/dataset/77764a7e-63fc-4111-ace3-fb7d3037953a/resource/f0fa78dc-74c3-49fa-8971-c310a76a07fa/download/gtfsfiles.zip) · [dataset atual](https://dados.pbh.gov.br/dataset/gtfs) | CC BY; portal declara atualização semanal/arquivo diário; portal antigo desativado, conflito exige `manual_review` |
| `mdb-687` | BHTRANS suplementar — Belo Horizonte/MG e RMBH; ônibus | MDB `active` | [recurso CKAN](https://ckan.pbh.gov.br/dataset/af0c47bb-5a82-4ae1-874f-e45dea1397ff/resource/b2a9341e-4471-45cc-a8c0-11be805590bc/download/gtfsfiles.zip) · [dataset atual](https://dados.pbh.gov.br/dataset/gtfs) | CC BY; feed antigo e dataset agregado precisam ser comparados |
| `mdb-930` | Prefeitura de Bagé/RS; ônibus | catálogo/MDB `inactive` | [arquivo histórico](https://github.com/rodrigowindows/GTFS/raw/master/GTFS_Bage.zip) | fonte comunitária, licença `UNKNOWN`, validade 2016–2017; não usar como atual |
| `mdb-1791` | SMTR — Rio de Janeiro/RJ; ônibus municipais e BRT | MDB `active`; `is_official=true` | [ArcGIS data](https://www.arcgis.com/sharing/rest/content/items/8ffe62ad3b2f42e49814bf941654ea6c/data) · [item](https://www.arcgis.com/home/item.html?id=8ffe62ad3b2f42e49814bf941654ea6c) · [data.rio](https://www.data.rio/datasets/gtfs-do-rio-de-janeiro/about) | atualização mensal declarada; escopo SPPO ônibus/BRT, não prova trens/metrô |
| `mdb-1822` | Metrofor — Fortaleza/CE; metroferroviário | `deprecated` | [arquivo 2021](https://www.metrofor.ce.gov.br/wp-content/uploads/sites/32/2021/12/gtfs_metrofor.zip) · [termos](https://www.metrofor.ce.gov.br/gtfs/) | versão histórica; não usar como feed atual |
| `mdb-1863` | Etufor — Fortaleza/CE; ônibus | `deprecated` | [arquivo antigo](https://dados.fortaleza.ce.gov.br/dataset/51afc610-d48b-4fa8-8dea-9c65747148c7/resource/fc9109ec-48a9-4af3-a7c8-4909cc1e4ac0/download/exportacao.zip) | validade expirada; não usar como atual |
| `mdb-2010` | Metrofor — Fortaleza/CE; metroferroviário | `deprecated` | [arquivo 2023](https://www.metrofor.ce.gov.br/wp-content/uploads/sites/32/2023/12/gtfs_metrofor.zip) · [termos](https://www.metrofor.ce.gov.br/gtfs/) | URL datada/validade expirada |
| `mdb-2011` | Etufor — Fortaleza/CE; ônibus | `deprecated`; redirecionado para registro mais novo | [arquivo histórico](https://dados.fortaleza.ce.gov.br/dataset/51afc610-d48b-4fa8-8dea-9c65747148c7/resource/51e3d494-3b41-4328-a971-964e2cdd8a22/download/gtff-202311.zip) | não usar sem conferir registro atual |
| `mdb-2367` | Metrofor — Fortaleza/CE; metroferroviário | registro mais novo; `is_official=true` | [arquivo 2025](https://www.metrofor.ce.gov.br/wp-content/uploads/sites/32/2025/01/gtfs_metrofor.zip) · [termos](https://www.metrofor.ce.gov.br/gtfs/) | página oficial é autoridade; periodicidade/validade do arquivo atual `UNKNOWN` |
| `mdb-2632` | Viação Senhor do Bonfim — Angra dos Reis/RJ | `is_official=true` no catálogo; autoridade independente `UNKNOWN` | [download Google Drive](https://drive.usercontent.google.com/uc?id=1l8BUIOaNZiu7hbO1UxMB1e9EaXm5s4Wa&export=download) | URL de arquivo, sem página institucional confirmada; licença/frescor `UNKNOWN` |
| `mdb-2934` | Etufor — Fortaleza/CE; ônibus | `active`; `is_official=true` | [recurso atual](https://dados.fortaleza.ce.gov.br/dataset/d6f1e64c-aca3-4867-8f39-53b7c9c2d211/resource/7058bfbe-5ba2-45f4-9a91-af1508a7c05b/download/arquivo_gtfs_03.10.2025.zip) | dataset ativo; data do arquivo no nome; atualizar antes de consultar |
| `mdb-2935` | ARCE — região metropolitana de Fortaleza/CE; ônibus | `active`; `is_official=true` | [arquivo ARCE](https://www.arce.ce.gov.br/wp-content/uploads/sites/53/2018/11/GTFS_Arce_01082025.zip) · [transportes](https://www.arce.ce.gov.br/download/transportes/) | página oficial; versão 2025 no nome; atualizar antes de usar |
| `mdb-3225` | URBS — Curitiba/PR; transporte urbano | fonte catalogada não oficial (`is_official=false`) | [cópia GitHub](https://github.com/benaytms/urbs-gtfs/releases/download/latest/gtfs_curitiba.zip) · [portal URBS](https://www.urbs.curitiba.pr.gov.br/) | usar portal URBS como autoridade; cópia comunitária não prova licença/frescor |

**Regra de atualização:** os 15 registros são o conjunto localizado no snapshot consultado; status e URLs podem mudar. Não publicar “todos os GTFS do Brasil” sem nova busca, lista de fontes consultadas, data e limites.

## GTFS-RT

O catálogo filtrado não retornou registro brasileiro `gtfs-rt`. O mapa encontrou menção explícita a GTFS-RT em material de Belo Horizonte, mas endpoint, bytes e frescor não foram validados nesta fase: `manual_review`. SPTrans/Olho Vivo, posições de veículos em portais e APIs proprietárias não devem ser chamados de GTFS-RT sem feed protobuf e contrato do produtor. Qualquer vínculo static↔RT precisa resolver IDs e janela temporal; feed RT órfão é `unsupported`/`manual_review`.

## Checks read-only

1. **ZIP/CSV:** confirmar ZIP válido, tamanho limitado, UTF-8/CSV e ausência de path traversal; não baixar sem autorização e limite.
2. **Arquivos obrigatórios:** `agency.txt`, `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt` e `calendar.txt` ou `calendar_dates.txt`, conforme a referência GTFS; validar cabeçalho, tipos e enums.
3. **Integridade:** chaves únicas, FKs sem órfãos, `stop_times` ordenado, horários coerentes, IDs persistentes e nenhuma duplicata que altere semântica.
4. **Espaço/UF:** latitude/longitude válidas, timezone IANA, bbox e município/UF compatíveis com cobertura declarada; divergência vira `manual_review`.
5. **Calendário:** datas `YYYYMMDD`, exceções, validade na data pedida e janela futura; feed vencido é `stale`, não “sem serviço”.
6. **Recursos:** validar `wheelchair_*`, `shapes`, fares-v1/v2, transfers e `feed_info` somente quando anunciados; ausência não prova indisponibilidade.
7. **Realtime:** protobuf/FeedHeader/timestamp, entidades e referências static; medir atraso, não inferir “ao vivo” do nome do endpoint.
8. **Frescor/cobertura:** comparar `feed_info`, validade, `Last-Modified`/`ETag`, periodicidade declarada, agências/rotas/paradas e cobertura do modal; registrar discrepância catálogo↔produtor↔arquivo.

Estados: `ok`, `no_result`, `stale`, `blocked`, `auth_required`, `manual_review`, `unsupported`. `no_result` só vale para fonte acessível consultada; falha HTTP, CAPTCHA, auth, parser ou termo desconhecido mantém estado específico.

## Limites

Esta referência não prova segurança, acessibilidade física, chegada do veículo, tarifa vigente, reserva, pagamento, disponibilidade operacional ou titularidade de dados pessoais. Não fazer login, contornar CAPTCHA, comprar passagem, reservar, alterar rota pública ou coletar PII. A resposta deve conter fonte, data, jurisdição, cobertura, check executado e limitação; ausência de feed não é fallback para outro operador.
