from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)

from backend.schemas.study_notes import StudyNotes


def generate_notes_pdf(notes: StudyNotes, output_path: str) -> str:
    output_file = Path(output_path)

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "NotesTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "NotesHeading",
        parent=styles["Heading2"],
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = styles["BodyText"]

    story = []

    story.append(Paragraph("AI Lecture Study Notes", title_style))

    story.append(Paragraph("Lecture Summary", heading_style))
    story.append(Paragraph(notes.lecture_summary, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Key Concepts", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(concept, body_style))
                for concept in notes.key_concepts
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Definitions", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(definition, body_style))
                for definition in notes.definitions
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Important Points", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(point, body_style))
                for point in notes.important_points
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Examples", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(example, body_style))
                for example in notes.examples
            ],
            bulletType="bullet",
        )
    )

    document.build(story)

    return str(output_file)