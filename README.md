# text embedding generator

```bash
$ brew install uv just git-lfs
```

in project folder

```bash
$ git lfs install
$ git clone https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
```

run server

```bash
$ uv sync
$ just dev
```

test

```bash
$ just test
```

swagger
http://127.0.0.1:8000/docs#/

you could also use docker compose to boot it up

```bash
$ docker compose up -d
```

swagger http://127.0.0.1:5200/docs#/

to send traces / metrics / logs to taruza's LGTM stack on the same docker host
(the external `lgtm-net` network must exist)

```bash
$ docker compose -f docker-compose.yml -f compose.lgtm-shared.yaml up -d
```

## configuration

- `TEG_MODEL_PATH`: path (local dir or HF hub id) to the sentence-transformers
  model to load. Defaults to `./Qwen3-Embedding-0.6B`. Query `GET
  /api/v1/text-embedding/model-info` at runtime to check which model/dim is
  currently loaded.
- `TEG_LOG_CONF`: logging config file. Defaults to `./log.conf`, which also
  writes rotating files under `.log/`. When the file doesn't exist (e.g. in the
  docker image), logs only go to stdout.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP HTTP endpoint, e.g. `http://lgtm:4318`.
  Unset or empty means OTel export is off.
- `OTEL_SERVICE_NAME`: service name in traces / metrics / logs (`teg` in
  docker compose).
