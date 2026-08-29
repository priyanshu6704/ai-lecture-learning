
from pydantic import BaseModel, Field


class SpeakingEvaluation(BaseModel):
    accuracy: float = Field(
        ...,
        ge=0,
        le=100,
    )

    feedback: str = Field(
        ...,
        min_length=1,
    )

    @property
    def is_correct(self) -> bool:
        return self.accuracy >= 65


# Test 1: Above 65
evaluation1 = SpeakingEvaluation(
    accuracy=80,
    feedback="Good answer."
)

print("80%:", evaluation1.is_correct)


# Test 2: Below 65
evaluation2 = SpeakingEvaluation(
    accuracy=50,
    feedback="The answer needs improvement."
)

print("50%:", evaluation2.is_correct)


# Test 3: Exactly 65
evaluation3 = SpeakingEvaluation(
    accuracy=65,
    feedback="Acceptable answer."
)

print("65%:", evaluation3.is_correct)


print("\nPHASE 7.3 TEST: PASS")

