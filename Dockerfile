FROM python:3.13.12-slim AS builder
ENV APP_DIR=/opt/text-embedding-generator
WORKDIR ${APP_DIR}

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-cache --no-dev

FROM python:3.13.12-slim AS server
ENV APP_DIR=/opt/text-embedding-generator
WORKDIR ${APP_DIR}
COPY multilingual-e5-large/ multilingual-e5-large/
COPY --from=builder ${APP_DIR}/.venv/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY src/ src/
ENTRYPOINT ["uvicorn", "teg.main:api", "--host", "0.0.0.0", "--port", "5200", "--app-dir", "src"]
