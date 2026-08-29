
from pydantic import BaseModel, Field


class ReportAnalysis(BaseModel):
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