# trunk-ignore-all(checkov/CKV_DOCKER_2)
# trunk-ignore-all(checkov/CKV_DOCKER_3)
FROM python:3.12.4-slim

WORKDIR /opt/text-embedding-generator
COPY . .
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

ENTRYPOINT [ "uvicorn", "teg.main:api", "--host", "0.0.0.0", "--port", "5200" ]