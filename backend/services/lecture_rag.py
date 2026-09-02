import time

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.schemas.study_notes import StudyNotes
from backend.services.chunker import chunk_documents
from backend.services.vector_store import create_vector_store
from backend.services.lecture_retriever import retrieve_lecture_context
from backend.services.llm_service import get_llm


def build_lecture_knowledge_base(
    documents: list[Document],
) -> Chroma:

    chunks = chunk_documents(documents)
    return create_vector_store(chunks)


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


def _invoke_with_retry(llm, prompt, max_retries=5):

    for attempt in range(max_retries):

        try:
            return llm.invoke(prompt)

        except Exception as e:

            error = str(e).lower()

            if "rate_limit" not in error and "429" not in error:
                raise

            wait_time = min(60, 10 * (2 ** attempt))
            time.sleep(wait_time)

    raise Exception("Groq rate limit remained active after retries.")


def _summarize_chunk(llm, text):

    prompt = f"""
You are an AI study assistant.

Summarize this lecture section using ONLY the information
contained in the section.

Keep important:
- concepts
- definitions
- principles
- formulas
- processes
- examples

Do not add outside knowledge.

LECTURE SECTION:

{text}
"""

    response = _invoke_with_retry(llm, prompt)

    time.sleep(2)

    return response.content
def generate_study_notes(
    documents: list[Document],
) -> StudyNotes:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=6000,
        chunk_overlap=300,
    )

    chunks = splitter.split_documents(documents)

    llm = get_llm()

    summaries = []

    for chunk in chunks:

        prompt = f"""
You are an AI study assistant.

Summarize this lecture section.

Use ONLY information from the lecture section.
Do not use outside knowledge.

Preserve:
- important concepts
- definitions
- important points
- formulas
- processes
- examples

Keep the summary concise.

LECTURE SECTION:

{chunk.page_content}
"""

        response = _invoke_with_retry(llm, prompt)

        summaries.append(response.content)

        time.sleep(2)

    while len(summaries) > 4:

        new_summaries = []

        for i in range(0, len(summaries), 4):

            batch = summaries[i:i + 4]

            combined = "\n\n".join(batch)

            prompt = f"""
Combine these lecture summaries.

Use ONLY the information provided.
Remove duplicate information.
Do not add outside knowledge.
Keep important information.

SUMMARIES:

{combined}
"""

            response = _invoke_with_retry(llm, prompt)

            new_summaries.append(response.content)

            time.sleep(2)

        summaries = new_summaries

    final_context = "\n\n".join(summaries)

    final_prompt = f"""
Create study notes for the lecture using ONLY the
information provided below.

You are calling the StudyNotes tool.

The tool has EXACTLY five required fields:

1. lecture_summary
2. key_concepts
3. definitions
4. important_points
5. examples

Every field MUST be provided.

Field requirements:

lecture_summary:
A concise paragraph summarizing the complete lecture.

key_concepts:
A list of important concepts from the lecture.

definitions:
A list of definitions explicitly supported by the lecture.

important_points:
A list of important facts, principles, formulas, or processes.

examples:
A list of examples explicitly mentioned in the lecture.

If a category has no information, provide an empty list.

Do not omit any field.

Do not add information that is not present.

LECTURE SUMMARIES:

{final_context}
"""

    structured_llm = llm.with_structured_output(
        StudyNotes
    )

    response = structured_llm.invoke(final_prompt)

    return response