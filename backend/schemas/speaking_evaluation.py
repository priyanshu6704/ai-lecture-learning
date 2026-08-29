
from pydantic import BaseModel, Field


class SpeakingEvaluation(BaseModel):
    accuracy: float = Field(
        ...,
        ge=0,
        le=100,
        description="Accuracy of the student's answer compared with the lecture content."
    )

    feedback: str = Field(
        ...,
        min_length=1,
        description="Concise feedback explaining the accuracy of the student's answer."
    )

    @property
    def is_correct(self)->bool:
        return self.accuracy >=65