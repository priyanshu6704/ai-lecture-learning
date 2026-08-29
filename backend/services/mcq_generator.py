from langchain_core.prompts import ChatPromptTemplate

from backend.schemas.mcq import MCQGame
from backend.services.lecture_retriever import retrieve_lecture_context
from backend.services.llm_service import get_llm


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
6. Provide a short explanation based only on the lecture.
7. Generate exactly the requested number of questions.
8. Questions should test understanding, not only memorization.
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

    return result