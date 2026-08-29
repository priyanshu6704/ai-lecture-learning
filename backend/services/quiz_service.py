from backend.schemas.mcq import MCQ
from backend.schemas.quiz import QuizAnswer, QuizResult


def evaluate_answer(
    mcq: MCQ,
    question_index: int,
    selected_answer: str | None,
    timed_out: bool = False,
) -> QuizAnswer:

    if timed_out or selected_answer is None:
        return QuizAnswer(
            question_index=question_index,
            selected_answer=selected_answer,
            is_correct=False,
            timed_out=True,
        )

    is_correct = selected_answer == mcq.correct_answer

    return QuizAnswer(
        question_index=question_index,
        selected_answer=selected_answer,
        is_correct=is_correct,
        timed_out=False,
    )


def calculate_quiz_result(
    answers: list[QuizAnswer],
) -> QuizResult:

    total_questions = len(answers)

    correct_answers = sum(
        1
        for answer in answers
        if answer.is_correct
    )

    score = correct_answers

    percentage = (
        correct_answers / total_questions
    ) * 100

    return QuizResult(
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
        percentage=percentage,
    )