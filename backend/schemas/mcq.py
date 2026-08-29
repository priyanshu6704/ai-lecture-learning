from pydantic import BaseModel, Field


class MCQ(BaseModel):
    question: str = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)


class MCQGame(BaseModel):
    questions: list[MCQ] = Field(..., min_length=1)
    time_per_question: int = Field(default=30, ge=1)