import streamlit as st

from state import navigate
from api_client import upload_lecture


def render_upload():

    st.html("""
    <div class="hero">
        <div class="badge">✦ LECTURE INPUT</div>

        <h1>Upload your lecture.</h1>

        <p>
            Upload a PDF, DOCX, or PPTX file and let AI
            understand the lecture content.
        </p>
    </div>
    """)

    uploaded_file = st.file_uploader(
        "Choose your lecture file",
        type=["pdf", "docx", "pptx"],
    )

    if uploaded_file:

        st.success(f"Selected: {uploaded_file.name}")

        if st.button("Process Lecture", use_container_width=True):

            with st.spinner("Processing your lecture..."):

                try:
                    result = upload_lecture(uploaded_file)

                    st.session_state.lecture_uploaded = True
                    st.session_state.filename = uploaded_file.name
                    st.session_state.page = "study"

                    st.success("Lecture uploaded successfully!")
                    st.info(
                        f"Processed {result['document_count']} sections."
                    )

                    st.rerun()

                except Exception as e:
                    st.error(f"Upload failed: {e}")

    if st.button("← Back to Home", use_container_width=True):
        navigate("home")