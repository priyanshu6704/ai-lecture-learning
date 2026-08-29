
from backend.schemas.speaking_evaluation import SpeakingEvaluation
from backend.services.llm_service import get_llm


def evaluate_spoken_answer(
    question: str,
    transcript: str,
    lecture_context: str,
) -> SpeakingEvaluation:

    llm = get_llm()

    prompt = f"""
You are evaluating a student's spoken answer to a lecture-based question.

Your evaluation MUST be based only on the provided lecture context.

QUESTION:
{question}

STUDENT ANSWER:
{transcript}

LECTURE CONTEXT:
{lecture_context}

Evaluate how accurately the student's answer matches the lecture.

Accuracy rules:
- 0 = completely incorrect
- 25 = mostly incorrect
- 50 = partially correct
- 65 = acceptable understanding
- 80 = mostly accurate
- 100 = fully accurate
- Return a value between 0 and 100.
- Do not give credit for claims that are unsupported by the lecture context.

Provide:
1. accuracy
2. concise feedback explaining the evaluation

Do not invent information that is not present in the lecture context.
"""

    structured_llm = llm.with_structured_output(SpeakingEvaluation)

    evaluation = structured_llm.invoke(prompt)

    return evaluation

