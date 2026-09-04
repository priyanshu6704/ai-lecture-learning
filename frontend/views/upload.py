"""pages/upload.py"""

import streamlit as st

import api_client
from components.navigation import render_progress
from state import go_to

ACCEPTED_TYPES = ["pdf", "docx", "pptx"]


def render() -> None:
    render_progress(active_index=1)

    st.markdown('<div class="alp-section-title">Upload your lecture</div>', unsafe_allow_html=True)
    st.write("Accepted formats: PDF, DOCX, PPTX.")

    uploaded_file = st.file_uploader(
        "Choose a lecture file",
        type=ACCEPTED_TYPES,
        label_visibility="collapsed",
    )

    if uploaded_file is not None and not st.session_state.lecture_uploaded:
        st.markdown(
            f"""
            <div class="alp-card">
                <span class="alp-badge">Selected</span><br><br>
                <strong>{uploaded_file.name}</strong><br>
                <span style="color:#5B6478">{uploaded_file.size / 1024:.1f} KB</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Process Lecture", type="primary"):
            with st.spinner("Uploading and processing lecture..."):
                try:
                    result = api_client.upload_lecture(uploaded_file)
                except api_client.ApiError as e:
                    st.error(f"Upload failed: {e.message}")
                    return

            st.session_state.lecture_uploaded = True
            st.session_state.filename = result.get("filename", uploaded_file.name)
            st.session_state.document_count = result.get("document_count")
            st.rerun()

    if st.session_state.lecture_uploaded:
        st.success(
            f"**{st.session_state.filename}** processed successfully "
            f"({st.session_state.document_count} sections)."
        )
        if st.button("Continue to Study Notes", type="primary"):
            go_to("study")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        go_to("home")
