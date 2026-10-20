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

## logging

`log.ini`, passed to uvicorn with `--log-config` (`just dev` and the docker
image both do). JSON lines with trace / span IDs go to stdout; WARNING and
above also go to rotating gzip files under `.log/` (`zcat` / `zgrep` to read
the rotated ones).

## configuration

- `TEG_MODEL_PATH`: path (local dir or HF hub id) to the sentence-transformers
  model to load. Defaults to `./Qwen3-Embedding-0.6B`. Query `GET
  /api/v1/text-embedding/model-info` at runtime to check which model/dim is
  currently loaded.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP HTTP endpoint. OTel export is always on;
  unset means the SDK default `http://localhost:4318` (`http://lgtm:4318` in
  docker compose).
- `OTEL_SERVICE_NAME`: service name in traces / metrics / logs (`teg` in
  docker compose).
