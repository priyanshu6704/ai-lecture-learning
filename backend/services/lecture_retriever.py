from langchain_chroma import Chroma
from langchain_core.documents import Document

def retrieve_lecture_context(
        vector_store:Chroma,
        query:str,
        k:int=3,
)->list[Document]:
    results=vector_store.similarity_search(
        query,k=k,
    )
    return results