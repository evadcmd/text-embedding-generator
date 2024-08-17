from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["liveness prove"])


@router.get("", status_code=200)
async def liveness_probe():
    return
