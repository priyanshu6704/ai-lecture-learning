import json

from langchain_chroma import Chroma
from pydantic import ValidationError

from backend.schemas.speaking import SpeakingQuestion
from backend.services.llm_service import get_llm
from backend.services.lecture_retriever import retrieve_lecture_context


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output.")
    return json.loads(cleaned[start:end + 1])


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

Respond with ONLY a single valid JSON object, no markdown fences, no
commentary, matching exactly this shape:
{{
  "question": "<string>",
  "topic": "<string>"
}}
"""

    response = llm.invoke(prompt)

    try:
        data = _extract_json(response.content)
        return SpeakingQuestion(**data)
    except (ValueError, json.JSONDecodeError, ValidationError):
        retry_prompt = prompt + f"""

Your previous response was invalid. Return ONLY the corrected JSON
object, no markdown fences, no commentary, no text before or after it.
"""
        response = llm.invoke(retry_prompt)
        data = _extract_json(response.content)
        return SpeakingQuestion(**data)