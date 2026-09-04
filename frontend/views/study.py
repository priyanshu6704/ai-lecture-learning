"""pages/study.py

Renders the StudyNotes schema (lecture_summary, key_concepts,
definitions, important_points, examples) as readable sections/cards --
never as raw JSON, per the spec.
"""

import streamlit as st

import api_client
from components.navigation import render_progress
from state import go_to


def _render_list_section(title: str, items: list, accent: bool = False) -> None:
    st.markdown(f'<div class="alp-section-title">{title}</div>', unsafe_allow_html=True)
    if not items:
        st.markdown('<div class="alp-empty">Nothing generated for this section.</div>', unsafe_allow_html=True)
        return
    cls = "alp-card accent" if accent else "alp-card"
    for item in items:
        st.markdown(f'<div class="{cls}">{item}</div>', unsafe_allow_html=True)


def render() -> None:
    render_progress(active_index=2)

    if not st.session_state.lecture_uploaded:
        st.warning("Upload a lecture first.")
        if st.button("Go to Upload"):
            go_to("upload")
        return

    if st.session_state.study_notes is None:
        st.markdown('<div class="alp-section-title">Generate study notes</div>', unsafe_allow_html=True)
        st.write(
            f"Ready to turn **{st.session_state.filename}** into structured notes: "
            "a summary, key concepts, definitions, important points, and examples."
        )
        if st.button("Generate Study Notes", type="primary"):
            with st.spinner("AI is reading your lecture..."):
                try:
                    result = api_client.generate_notes()
                except api_client.ApiError as e:
                    st.error(f"Could not generate notes: {e.message}")
                    return
            st.session_state.study_notes = result.get("study_notes", {})
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Upload"):
            go_to("upload")
        return

    notes = st.session_state.study_notes

    st.markdown('<div class="alp-kicker">AI STUDY NOTES</div>', unsafe_allow_html=True)
    st.markdown('<div class="alp-hero-title" style="font-size:2rem;">Understand your lecture.</div>', unsafe_allow_html=True)

    st.markdown('<div class="alp-section-title">Lecture Summary</div>', unsafe_allow_html=True)
    summary = notes.get("lecture_summary") or "No summary available."
    st.markdown(f'<div class="alp-card accent">{summary}</div>', unsafe_allow_html=True)

    _render_list_section("Key Concepts", notes.get("key_concepts", []))
    _render_list_section("Definitions", notes.get("definitions", []))
    _render_list_section("Important Points", notes.get("important_points", []))
    _render_list_section("Examples", notes.get("examples", []))

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF", use_container_width=True):
            with st.spinner("Generating PDF..."):
                try:
                    result = api_client.generate_notes_pdf()
                except api_client.ApiError as e:
                    st.error(f"Could not generate PDF: {e.message}")
                else:
                    st.session_state.notes_pdf_info = result
    with col2:
        if st.button("Start Test →", type="primary", use_container_width=True):
            go_to("test_selection")

    if st.session_state.notes_pdf_info:
        try:
            pdf_bytes = api_client.download_notes_pdf()
        except api_client.ApiError as e:
            st.error(f"Could not fetch PDF: {e.message}")
        else:
            st.download_button(
                "⬇ Download study_notes.pdf",
                data=pdf_bytes,
                file_name="study_notes.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
