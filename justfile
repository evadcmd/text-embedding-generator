# Where lgtm comes from: "shared" joins the standalone lgtm on lgtm-net,
# "local" runs its own in this project. Override with `just lgtm=local up`.
lgtm := "shared"
compose := "docker compose -f compose.yaml -f compose.lgtm-" + lgtm + ".yaml"

dev:
    mkdir -p .log
    uv run uvicorn teg.main:api --reload --app-dir src --log-config log.ini
test:
    uv run pytest --cov=teg -s tests/

up *args:
    GIT_SHA="$(git rev-parse --short=12 HEAD)$(git diff --quiet HEAD || echo -dirty)" {{ compose }} up -d --build {{ args }}

# Stop and remove containers, the project network and the images we build.
# --rmi local keeps pulled images; `all` would re-pull them on every `just up`.
# Volumes stay: no -v. In shared mode lgtm-net is external, so compose never removes it.
down *args:
    {{ compose }} down --rmi local --remove-orphans {{ args }}

pyrefly *args="check":
    uv run pyrefly {{ args }} --min-severity warn

ruff *args="check":
    uv run ruff {{ args }}
