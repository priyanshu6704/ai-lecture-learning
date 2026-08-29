from pydantic import BaseModel, Field


class StudyNotes(BaseModel):
    lecture_summary: str = Field(
        description="A concise summary of the lecture."
    )

    key_concepts: list[str] = Field(
        description="Important concepts explained in the lecture."
    )

    definitions: list[str] = Field(
        description="Important definitions supported by the lecture."
    )

    important_points: list[str] = Field(
        description="Important facts, principles, formulas, or processes from the lecture."
    )

    examples: list[str] = Field(
        description="Examples explicitly provided in the lecture."
    )