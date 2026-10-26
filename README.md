# text embedding generator

```bash
$ brew install uv just git-lfs
```

in project folder

```bash
$ git lfs install
$ git clone https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
```

run server (Python 3.14; `uv sync` fetches it if missing)

```bash
$ uv sync
$ just dev
```

swagger
http://127.0.0.1:8000/docs#/

the model runs on cuda, then mps, then cpu, whichever is available first.

## API

- `POST /api/v1/text-embedding`: `{"text": "...", "type": "passage"}` ->
  `list[float]`
- `POST /api/v1/text-embedding/batch`: `{"texts": ["...", "..."], "type":
  "passage"}` -> `list[list[float]]`
- `GET /api/v1/text-embedding/model-info`: `{"model_path": "...", "dim": 1024}`
- `GET /healthz`: liveness probe
- `GET /metrics`: Prometheus metrics

`type` is `query` or `passage` (default). `query` encodes with the model's
`query` prompt, `passage` with no prompt, so embed search queries as `query`
and the documents they search as `passage`. Embeddings are L2-normalized, so
dot product equals cosine similarity.

```bash
$ curl -s http://127.0.0.1:8000/api/v1/text-embedding \
    -H 'Content-Type: application/json' \
    -d '{"text": "hello", "type": "query"}'
```

## docker compose

the image copies `Qwen3-Embedding-0.6B/` in, so clone the model first.

```bash
$ just up                # joins taruza's LGTM stack on the external `lgtm-net` network
$ just lgtm=local up     # runs its own LGTM in this project instead
$ just down              # same lgtm=... as up
```

`just up` builds the image with `GIT_SHA` set to the current commit
(`-dirty` with uncommitted changes) and passes extra args through to `docker
compose up`, e.g. `just up --force-recreate`. `just down` removes the
containers, the project network and the built images, but keeps volumes.

- swagger: http://127.0.0.1:5200/docs#/
- Grafana (`lgtm=local` only): http://127.0.0.1:3000
- `teg-api` also joins the `teg-net` network, so other compose projects can
  reach it at `http://teg-api:5200` by joining `teg-net` as an external
  network.

## development

```bash
$ just test      # pytest with coverage
$ just ruff      # ruff check; `just ruff format` to format
$ just pyrefly   # pyrefly check (strict preset)
```

CI runs `ruff format --check`, `ruff check` and `pyrefly check` on every push
to main and on every PR.

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
