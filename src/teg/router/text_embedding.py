from fastapi import APIRouter
from pydantic import BaseModel

from teg import embedding
from teg.embedding import TextType
from teg.router import API_V1

router = APIRouter(
    prefix=API_V1 + "/text-embedding", tags=["text embedding generator API"]
)


class Text(BaseModel):
    text: str
    type: TextType = TextType.PASSAGE


class TextBatch(BaseModel):
    texts: list[str]
    type: TextType = TextType.PASSAGE


@router.post("")
async def text_embedding(dto: Text) -> list[float]:
    return await embedding.gen(dto.text, dto.type)


@router.post("/batch")
async def text_embedding_batch(dto: TextBatch) -> list[list[float]]:
    return await embedding.gen_batch(dto.texts, dto.type)


@router.get("/model-info")
async def model_info() -> dict[str, str | int]:
    return embedding.model_info()
