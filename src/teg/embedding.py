import torch.nn.functional as F
from torch import Tensor
from transformers import AutoModel, AutoTokenizer
from teg import device


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


tokenizer = AutoTokenizer.from_pretrained("./multilingual-e5-large")
model = AutoModel.from_pretrained("./multilingual-e5-large").to(device)


# Each input text should start with "query: " or "passage: ", even for non-English texts.
# For tasks other than retrieval, you can simply use the "query: " prefix.
def _gen(text: str) -> list[float]:
    batch_dict = tokenizer(
        [f"query: {text}"],
        max_length=512,
        padding=True,
        truncation=True,
        return_tensors="pt",
    ).to(device)

    outputs = model(**batch_dict)
    embeddings = F.normalize(
        average_pool(outputs.last_hidden_state, batch_dict["attention_mask"]),
        p=2,
        dim=1,
    )
    return embeddings[0].tolist()


import asyncio


async def gen(text: str) -> list[float]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _gen, text)
