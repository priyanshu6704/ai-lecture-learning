import difflib

from langchain_core.prompts import ChatPromptTemplate

from backend.schemas.mcq import MCQGame
from backend.services.lecture_retriever import retrieve_lecture_context
from backend.services.llm_service import get_llm


def _normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _fix_correct_answers(mcq_game: MCQGame) -> MCQGame:
    """Defensive pass: guarantee every question's correct_answer is
    character-identical to one of its options. The prompt now instructs
    the model to copy it verbatim, but this catches any drift (extra
    whitespace, trailing punctuation, minor rewording) so a mismatch
    never silently causes every answer to be marked wrong."""

    for mcq in mcq_game.questions:

        if mcq.correct_answer in mcq.options:
            continue

        normalized_target = _normalize(mcq.correct_answer)
        exact_normalized_match = next(
            (opt for opt in mcq.options if _normalize(opt) == normalized_target),
            None,
        )
        if exact_normalized_match is not None:
            mcq.correct_answer = exact_normalized_match
            continue

        closest = difflib.get_close_matches(
            mcq.correct_answer, mcq.options, n=1, cutoff=0.0
        )
        mcq.correct_answer = closest[0] if closest else mcq.options[0]

    return mcq_game


def generate_mcq_game(vector_store, number_of_questions: int = 10) -> MCQGame:

    query = "Important concepts, definitions, principles, examples and key points from the lecture"

    documents = retrieve_lecture_context(
        vector_store=vector_store,
        query=query,
        k=8,
    )

    lecture_context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an educational quiz generator.

Generate multiple-choice questions ONLY from the provided lecture context.

Strict rules:
1. Do not use knowledge outside the lecture context.
2. Do not invent facts, concepts, examples, or definitions.
3. Each question must have exactly four options.
4. Only one option must be correct.
5. The correct answer must be supported by the lecture context.
6. The "correct_answer" field must be an EXACT, character-for-character
   copy of one of the four strings in "options" for that question --
   never a paraphrase, a shortened version, or reworded in any way.
7. Provide a short explanation based only on the lecture.
8. Generate exactly the requested number of questions.
9. Questions should test understanding, not only memorization.
""",
            ),
            (
                "human",
                """
Generate exactly {number_of_questions} MCQs from this lecture.

LECTURE CONTEXT:
{lecture_context}
""",
            ),
        ]
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(MCQGame)

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "number_of_questions": number_of_questions,
            "lecture_context": lecture_context,
        }
    )

    return _fix_correct_answers(result)