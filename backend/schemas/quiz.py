from pydantic import BaseModel, Field
from backend.schemas.mcq import MCQGame

class QuizAnswer(BaseModel):
    question_index: int = Field(..., ge=0)
    selected_answer: str | None = None
    is_correct: bool = False
    timed_out: bool = False


class QuizResult(BaseModel):
    total_questions: int = Field(..., ge=1)
    correct_answers: int = Field(..., ge=0)
    score: int = Field(..., ge=0)
    percentage: float = Field(..., ge=0, le=100)


class QuizSession(BaseModel):
    game: MCQGame
    current_question_index: int = Field(default=0, ge=0)
    answers: list[QuizAnswer] = Field(default_factory=list)
    completed: bool = False