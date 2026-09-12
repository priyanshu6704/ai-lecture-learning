import os
from functools import lru_cache

from langchain_huggingface import HuggingFaceEndpointEmbeddings


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEndpointEmbeddings:
    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=os.environ.get("HF_TOKEN"),
    )