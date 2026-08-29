from pydantic import BaseModel, Field


class SpeakingQuestion(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Lecture-grounded question for the learner to answer verbally."
    )

    topic: str = Field(
        ...,
        min_length=1,
        description="Main lecture topic being tested."
    )


class SpeechTranscript(BaseModel):
    transcript: str = Field(
        ...,
        min_length=1,
        description="Text generated from the learner's spoken response."
    )

    language: str | None = Field(
        default=None,
        description="Detected language of the spoken response."
    )