import asyncio

from sentence_transformers import SentenceTransformer

from teg import device

model = SentenceTransformer("./Qwen3-Embedding-0.6B", device=str(device))


def _gen(text: str) -> list[float]:
    embeddings = model.encode([text], normalize_embeddings=True)
    return embeddings[0].tolist()


async def gen(text: str) -> list[float]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _gen, text)
