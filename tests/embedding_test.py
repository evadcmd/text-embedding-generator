import pytest
import torch

from teg import embedding
from teg.embedding import TextType


@pytest.mark.asyncio
async def test_gen():
    vec = await embedding.gen("hi")
    assert len(vec) == 1024


@pytest.mark.asyncio
async def test_gen_batch():
    vecs = await embedding.gen_batch(["hi", "there"])
    assert len(vecs) == 2
    assert len(vecs[0]) == 1024


@pytest.mark.asyncio
async def test_score():
    positive = await embedding.gen("positive")
    negative = await embedding.gen("negative")
    text1 = await embedding.gen("おめでとうございます！", TextType.QUERY)
    assert torch.inner(text1, positive) > torch.inner(text1, negative)
    text2 = await embedding.gen(
        "I don't think it is going to work...", TextType.QUERY
    )
    assert torch.inner(text2, positive) < torch.inner(text2, negative)


def test_model_info():
    info = embedding.model_info()
    assert info["dim"] == 1024
