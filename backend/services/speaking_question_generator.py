from langchain_chroma import Chroma
from backend.schemas.speaking import SpeakingQuestion
from backend.services.llm_service import get_llm
from backend.services.lecture_retriever import retrieve_lecture_context

def generate_speaking_question(
        vector_store: Chroma,
        topic: str,
)-> SpeakingQuestion:
    documents=retrieve_lecture_context(
        vector_store=vector_store,
        query=topic,
        k=3,
    )
    context="\n\n".join(
        document.page_content
        for document in documents
    )
    llm=get_llm()
    structured_llm = llm.with_structured_output(
        SpeakingQuestion
    )

    prompt = f"""
You are generating a speaking challenge question for a learner.

Use ONLY the lecture context provided below.

LECTURE CONTEXT:
{context}

TASK:
Generate one clear question that the learner should answer verbally.

RULES:
1. Use only information from the lecture context.
2. Do not use external knowledge.
3. Do not invent concepts or facts.
4. The question should test understanding, not simple memorization.
5. The question should be answerable from the provided context.
6. Return the main concept being tested as the topic.

TOPIC REQUESTED:
{topic}
"""

    return structured_llm.invoke(prompt)