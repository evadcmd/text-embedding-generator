from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from teg.router import liveness_probe, text_embedding

api = FastAPI(title="text embedding generator API")

Instrumentator().instrument(api).expose(api, tags=["Metrics"])

api.include_router(liveness_probe.router)
api.include_router(text_embedding.router)
