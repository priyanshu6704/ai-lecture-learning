
from typing import Literal

from pydantic import BaseModel, Field


class TestReport(BaseModel):
    test_type: Literal["mcq", "speaking"]

    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Final test score from 0 to 100."
    )

    strengths: list[str] = Field(
        ...,
        min_length=1,
        description="Things the learner performed well on."
    )

    recommendations: list[str] = Field(
        ...,
        min_length=1,
        description="Actionable recommendations for improvement."
    )
