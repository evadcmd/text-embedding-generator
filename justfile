dev:
    mkdir -p .log
    uv run uvicorn teg.main:api --reload --app-dir src --log-config log.ini
test:
    uv run pytest --cov=teg -s tests/
