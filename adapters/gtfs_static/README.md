# Adapter GTFS estático

Validator mínimo, local e read-only para um diretório sintético de GTFS
Schedule. Não baixa arquivo, não acessa URL, não chama GTFS-RT e não grava
resultado.

## Fonte e jurisdição sintéticas

- `source.name`: Fixture GTFS sintética BR Skill.
- `source.url`: `https://gtfs.example.invalid/synthetic` — identificador
  documental, nunca acessado.
- `source.role`: `synthetic_fixture`.
- `source.accessed_at`: `N/A`; fixture criada localmente, sem coleta externa.
- `source.license`: `UNKNOWN`; não representa produtor ou licença real.
- `jurisdiction`: `BR / UF e município sintéticos`; não afirma cobertura,
  operação ou disponibilidade em local real.
- `access`: `local-fixture`.

## Contrato

Entrada é caminho de diretório contendo apenas o núcleo exercitado:
`agency.txt`, `routes.txt`, `stops.txt`, `trips.txt`, `stop_times.txt` e
`calendar.txt`, em CSV UTF-8. A capacidade é `lookup` estrutural: recebe
caminho local e devolve `ValidationResult` com `status`, `errors` e `checks`.

O validator cobre, nesta ordem geral:

- presença, cabeçalho, UTF-8 e quantidade de colunas;
- chaves únicas de `agency`, `routes`, `stops`, `trips` e `calendar`;
- FKs `routes→agency`, `trips→routes/calendar` e
  `stop_times→trips/stops`;
- URL sintática, fuso local reconhecido e latitude/longitude finitas dentro
  dos limites;
- `route_type` inteiro no enum base `0..12`;
- dias do calendário como `0/1`, datas `YYYYMMDD` e intervalo válido;
- horário `HH:MM:SS` (incluindo horas pós-meia-noite até `99`), chegada não
  posterior à partida, sequência positiva sem duplicata e ordenada por viagem.

O resultado não contém valores das linhas, reduzindo risco de ecoar dados de
um feed fornecido pelo usuário.

## Estados

- `ok`: arquivos e invariantes mínimos passaram.
- `no_result`: diretório do feed não foi encontrado; não significa ausência de
  serviço numa fonte acessível.
- `unsupported`: estrutura, tipo, chave, referência ou valor não suportado.
- `blocked`: leitura local impedida por permissão ou erro de sistema.
- `stale`: frescor ou validade da fonte não foi comprovado; deve ser preservado
  pelo chamador, pois este validator não coleta metadados.
- `auth_required`: fonte exige autenticação; não é tentada por este adapter.
- `manual_review`: conflito de produtor, jurisdição, licença ou cobertura que
  a checagem sintética não resolve.

Os três últimos estados são estados de aquisição/handoff e não são inferidos
do conteúdo sintético. Falha de parser ou arquivo obrigatório ausente fica em
`unsupported`, não em `no_result`.

## Limites

Este não é implementação completa do padrão GTFS. Ficam fora: ZIP e proteção
contra path traversal, rede/HTTP, autenticação, `calendar_dates`, `feed_info`,
`shapes`, `frequencies`, `transfers`, tarifas, acessibilidade completa,
`route_type` estendido, validação semântica de DST, GTFS-RT, frescor real,
cobertura geográfica, disponibilidade operacional e qualquer PII. A fixture
é redigida e sintética; os valores não são bytes, dados ou evidência de
produtor real.

## Execução

Na raiz do repositório:

```bash
python3 adapters/gtfs_static/test_adapter.py
```

Uso programático:

```python
from adapter import validate_feed

resultado = validate_feed("adapters/gtfs_static/fixtures/synthetic_feed")
```

O teste não usa rede nem dependência fora da biblioteca padrão.
