import json
import streamlit as st

from state import navigate
from api_client import generate_notes


def render_study():

    st.html("""
    <div class="hero">
        <div class="badge">✦ AI STUDY NOTES</div>

        <h1>Understand your lecture.</h1>

        <p>
            Review your AI-generated study notes before starting
            the assessment.
        </p>
    </div>
    """)

    if st.session_state.study_notes is None:

        if st.button("Generate Study Notes", use_container_width=True):

            with st.spinner("Generating study notes..."):

                try:
                    result = generate_notes()

                    notes = result["study_notes"]

                    if isinstance(notes, str):
                        notes = json.loads(notes)

                    st.session_state.study_notes = notes

                    st.rerun()

                except Exception as e:
                    st.error(f"Failed to generate notes: {e}")

        return

    notes = st.session_state.study_notes

    if isinstance(notes, str):
        try:
            notes = json.loads(notes)
        except json.JSONDecodeError:
            st.error("Could not parse study notes.")
            return

    st.html("""
    <div class="section-title">
        Lecture Summary
    </div>
    """)

    st.write(notes.get("lecture_summary", ""))

    sections = [
        ("Key Concepts", "key_concepts"),
        ("Definitions", "definitions"),
        ("Important Points", "important_points"),
        ("Examples", "examples"),
    ]

    for title, key in sections:

        items = notes.get(key, [])

        if not items:
            continue

        st.html(f"""
        <div class="section-title">
            {title}
        </div>
        """)

        for item in items:
            st.markdown(f"- {item}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Download PDF", use_container_width=True):
            st.session_state.download_pdf = True

    with col2:
        if st.button("Start Test →", use_container_width=True):
            navigate("test_selection")

    if st.button("← Back to Upload", use_container_width=True):
        navigate("upload")