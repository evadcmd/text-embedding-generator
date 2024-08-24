import pytest
import torch

from teg import embedding


@pytest.mark.asyncio
async def test_gen():
    vec = await embedding.gen("hi")
    assert len(vec) == 1024


@pytest.mark.asyncio
async def test_score():
    positive = await embedding.gen("positive")
    negative = await embedding.gen("negative")
    text1 = await embedding.gen("おめでとうございます！")
    assert torch.inner(text1, positive) > torch.inner(text1, negative)
    text2 = await embedding.gen("I don't think it is going to work...")
    assert torch.inner(text2, positive) < torch.inner(text2, negative)
