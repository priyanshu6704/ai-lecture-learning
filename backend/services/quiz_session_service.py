from backend.schemas.mcq import MCQGame
from backend.schemas.quiz import QuizAnswer, QuizResult, QuizSession
from backend.services.quiz_service import (
    calculate_quiz_result,
    evaluate_answer,
)


def start_quiz(game: MCQGame) -> QuizSession:
    return QuizSession(
        game=game,
        current_question_index=0,
        answers=[],
        completed=False,
    )


def get_current_question(session: QuizSession):
    if session.completed:
        return None

    return session.game.questions[
        session.current_question_index
    ]


def submit_answer(
    session: QuizSession,
    selected_answer: str | None,
    timed_out: bool = False,
) -> QuizAnswer:

    if session.completed:
        raise ValueError("Quiz is already completed.")

    question_index = session.current_question_index

    mcq = session.game.questions[question_index]

    answer = evaluate_answer(
        mcq=mcq,
        question_index=question_index,
        selected_answer=selected_answer,
        timed_out=timed_out,
    )

    session.answers.append(answer)

    if question_index == len(session.game.questions) - 1:
        session.completed = True
    else:
        session.current_question_index += 1

    return answer


def get_quiz_result(session: QuizSession) -> QuizResult:

    if not session.completed:
        raise ValueError("Quiz is not completed yet.")

    return calculate_quiz_result(session.answers)