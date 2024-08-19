from fastapi import APIRouter
from pydantic import BaseModel

from teg import embedding
from teg.router import API_V1

router = APIRouter(
    prefix=API_V1 + "/text-embedding", tags=["text embedding generator API"]
)


class Text(BaseModel):
    text: str


@router.post("")
async def text_embedding(dto: Text) -> list[float]:
    return await embedding.gen(dto.text)
