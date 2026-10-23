ARG PYTHON_VERSION=3.14
ARG PYTHON_IMAGE=python:${PYTHON_VERSION}-slim

FROM ${PYTHON_IMAGE} AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --inexact

COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable --inexact


FROM ${PYTHON_IMAGE} AS teg-api

ARG UID=1000
ARG GID=1000
ARG APP_DIR=/app
RUN groupadd --gid=${GID} app \
    && useradd --uid=${UID} --gid=app --create-home app \
    && mkdir -p ${APP_DIR}/.log \
    && chown -R app:app ${APP_DIR}

ARG PYTHON_VERSION
ARG SYS_PY_PATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=builder ${SYS_PY_PATH} ${SYS_PY_PATH}

WORKDIR ${APP_DIR}
COPY --chown=app:app Qwen3-Embedding-0.6B/ Qwen3-Embedding-0.6B/
COPY --chown=app:app log.ini ./

USER app
# only site-packages is copied over, not .venv/bin, so there's no uvicorn script on PATH
# don't buffer stdout logs
ENV PYTHONUNBUFFERED=1
ARG GIT_SHA
ENV GIT_SHA=${GIT_SHA}

ENTRYPOINT ["python", "-m", "uvicorn", "teg.main:api", "--host", "0.0.0.0", "--port", "5200", "--app-dir", "src", "--log-config", "log.ini"]
