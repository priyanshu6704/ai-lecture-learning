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

import unicodedata


def _sanitize_text(text: str) -> str:

    if not text:
        return text

    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))

    typographic_map = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
        "\u2018": "'", "\u2019": "'", "\u201a": ",",
        "\u201c": '"', "\u201d": '"', "\u201e": '"',
        "\u2026": "...", "\u00a0": " ", "\u2022": "-",
    }
    for bad, good in typographic_map.items():
        normalized = normalized.replace(bad, good)

    return normalized.encode("cp1252", errors="ignore").decode("cp1252")


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
    story.append(Paragraph(_sanitize_text(notes.lecture_summary), body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Key Concepts", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(_sanitize_text(concept), body_style))
                for concept in notes.key_concepts
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Definitions", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(_sanitize_text(definition), body_style))
                for definition in notes.definitions
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Important Points", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(_sanitize_text(point), body_style))
                for point in notes.important_points
            ],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("Examples", heading_style))
    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(_sanitize_text(example), body_style))
                for example in notes.examples
            ],
            bulletType="bullet",
        )
    )

    document.build(story)

    return str(output_file)