FROM python:3.13.12-slim AS builder
ENV APP_DIR=/opt/text-embedding-generator
WORKDIR ${APP_DIR}

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
# TODO: add --frozen once uv.lock is regenerated (it's stale on main)
RUN uv sync --no-cache --no-dev

FROM python:3.13.12-slim AS server
ENV APP_DIR=/opt/text-embedding-generator
# logs go to stdout (log.conf isn't copied in, see teg/__init__.py); don't buffer them
ENV PYTHONUNBUFFERED=1
WORKDIR ${APP_DIR}
COPY Qwen3-Embedding-0.6B/ Qwen3-Embedding-0.6B/
COPY --from=builder ${APP_DIR}/.venv/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY src/ src/
# only site-packages is copied over, not .venv/bin, so there's no uvicorn script on PATH
ENTRYPOINT ["python", "-m", "uvicorn", "teg.main:api", "--host", "0.0.0.0", "--port", "5200", "--app-dir", "src"]
