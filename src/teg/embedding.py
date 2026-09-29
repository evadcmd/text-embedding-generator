import asyncio
from enum import StrEnum

from sentence_transformers import SentenceTransformer

from teg import device
from teg.config import MODEL_PATH

model = SentenceTransformer(MODEL_PATH, device=str(device))


class TextType(StrEnum):
    QUERY = "query"
    PASSAGE = "passage"


def _encode(texts: list[str], text_type: TextType) -> list[list[float]]:
    prompt_name = "query" if text_type == TextType.QUERY else None
    embeddings = model.encode(texts, normalize_embeddings=True, prompt_name=prompt_name)
    return embeddings.tolist()


async def gen_batch(
    texts: list[str], text_type: TextType = TextType.PASSAGE
) -> list[list[float]]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _encode, texts, text_type)


async def gen(text: str, text_type: TextType = TextType.PASSAGE) -> list[float]:
    return (await gen_batch([text], text_type))[0]


def model_info() -> dict[str, str | int]:
    return {"model_path": MODEL_PATH, "dim": model.get_sentence_embedding_dimension()}
