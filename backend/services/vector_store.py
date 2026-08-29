from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from backend.services.embedding_service import get_embeddings


def create_vector_store(
        documents:list[Document],
)-> Chroma:
    embeddings=get_embeddings()
    vector_store=Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="lecture_documents",
    )
    return vector_store