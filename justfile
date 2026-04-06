dev:
    uv run uvicorn teg.main:api --reload --app-dir src

test:
    uv run pytest --cov -s src/teg/
