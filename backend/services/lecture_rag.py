from langchain_core.documents import Document
from langchain_chroma import Chroma

from backend.schemas.study_notes import StudyNotes

from backend.services.chunker import chunk_documents
from backend.services.vector_store import create_vector_store
from backend.services.lecture_retriever import retrieve_lecture_context
from backend.services.llm_service import get_llm


def build_lecture_knowledge_base(
    documents: list[Document],
) -> Chroma:

    chunks = chunk_documents(documents)

    vector_store = create_vector_store(chunks)

    return vector_store


def search_lecture(
    vector_store: Chroma,
    query: str,
    k: int = 3,
) -> list[Document]:

    return retrieve_lecture_context(
        vector_store=vector_store,
        query=query,
        k=k,
    )


def generate_study_notes(
    documents: list[Document],
) -> StudyNotes:

    lecture_text = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an AI study assistant.

Create structured study notes from the lecture content below.

IMPORTANT RULES:
1. Use ONLY information present in the lecture.
2. Do NOT invent facts or information.
3. Do NOT use outside knowledge.
4. If a section has no information in the lecture, return an empty list.
5. Keep the summary concise.
6. Keep all concepts, definitions, points, and examples grounded in the lecture.

LECTURE CONTENT:

{lecture_text}
"""

    llm = get_llm()

    structured_llm = llm.with_structured_output(StudyNotes)

    response = structured_llm.invoke(prompt)

    return response