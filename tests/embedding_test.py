import pytest

from teg import embedding


@pytest.mark.asyncio
async def test_gen():
    vec = await embedding.gen("hi")
    assert len(vec) == 1024
