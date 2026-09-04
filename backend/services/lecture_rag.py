import json
import re
import time

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import ValidationError

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


def _get_retry_after_seconds(e: Exception) -> float | None:
    """Groq returns a Retry-After header (and often restates the wait
    time in the error message) on 429s. Prefer that exact value over a
    blind exponential guess -- it's usually much shorter."""

    response = getattr(e, "response", None)
    if response is not None:
        headers = getattr(response, "headers", None) or {}
        retry_after = headers.get("retry-after") or headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass

    match = re.search(r"try again in ([\d.]+)s", str(e).lower())
    if match:
        return float(match.group(1))

    return None


def _invoke_with_retry(llm, prompt, max_retries=5):

    for attempt in range(max_retries):

        try:
            return llm.invoke(prompt)

        except Exception as e:

            error = str(e).lower()

            if "rate_limit" not in error and "429" not in error:
                raise

            wait_time = _get_retry_after_seconds(e)
            if wait_time is None:
                wait_time = min(30, 5 * (2 ** attempt))

            time.sleep(wait_time)

    raise Exception("Groq rate limit remained active after retries.")


def _extract_json(text: str) -> dict:
    """Strip ```json fences (or any leading/trailing prose) and parse."""

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


def _generate_study_notes_via_json_fallback(llm, prompt, max_retries=3) -> StudyNotes:
    """Only used if the primary tool-calling path below fails. Asks for
    plain JSON and validates it locally instead of relying on Groq's
    structured-output enforcement."""

    json_prompt = prompt + """

Respond with ONLY a single valid JSON object, no markdown fences, no
commentary, matching exactly this shape:
{
  "lecture_summary": "<string>",
  "key_concepts": ["<string>", "..."],
  "definitions": ["<string>", "..."],
  "important_points": ["<string>", "..."],
  "examples": ["<string>", "..."]
}
"""

    current_prompt = json_prompt

    for attempt in range(max_retries):

        response = _invoke_with_retry(llm, current_prompt)

        try:
            data = _extract_json(response.content)
            return StudyNotes(**data)

        except (ValueError, json.JSONDecodeError, ValidationError) as e:

            if attempt == max_retries - 1:
                raise Exception(
                    f"Model failed to produce valid StudyNotes JSON after "
                    f"{max_retries} attempts: {e}"
                )

            current_prompt = f"""
{json_prompt}

Your previous response was invalid: {e}

Return ONLY the corrected JSON object. No markdown fences, no commentary,
no text before or after the JSON.
"""


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

    return response.content
def generate_study_notes(
    documents: list[Document],
) -> StudyNotes:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=16000,
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

Write a reasonably detailed summary in full sentences, not just a bare
list of keywords.

LECTURE SECTION:

{chunk.page_content}
"""

        response = _invoke_with_retry(llm, prompt)

        summaries.append(response.content)

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

Preserve ALL of the following if present in the summaries, even if brief:
- concepts
- definitions
- important points
- formulas
- processes
- examples

Do not drop examples during merging just because they seem minor --
they are required output later.

SUMMARIES:

{combined}
"""

            response = _invoke_with_retry(llm, prompt)

            new_summaries.append(response.content)

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
A well-developed summary of the complete lecture, written as 2-3 full
paragraphs rather than a single short blurb. Explain the main ideas and
how they relate, not just list them.

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

    try:
        structured_llm = llm.with_structured_output(StudyNotes)
        return structured_llm.invoke(final_prompt)

    except Exception as e:
        error = str(e).lower()
        if "tool" in error or "json_validate" in error:
            # Primary path failed -- fall back to plain-JSON + local
            # validation instead of surfacing the error.
            return _generate_study_notes_via_json_fallback(llm, final_prompt)
        raise