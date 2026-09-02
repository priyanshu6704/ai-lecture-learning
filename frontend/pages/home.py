import streamlit as st
from state import navigate


def render_home():

    # ============================================================
    # Hero
    # ============================================================

    st.html("""
    <div class="hero">
        <div class="badge">✦ AI-POWERED LEARNING</div>

        <h1>Learn smarter from your lectures.</h1>

        <p>
            Upload your lecture and let AI turn it into study notes,
            quizzes, speaking challenges, and actionable learning feedback.
        </p>
    </div>
    """)

    # ============================================================
    # Main Actions
    # ============================================================

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Upload Lecture", use_container_width=True):
            navigate("upload")

    with col2:
        if st.button("Start a Test", use_container_width=True):
            navigate("test_selection")

    # ============================================================
    # Learning Modes
    # ============================================================

    st.html("""
    <div class="section-title">
        Choose how you want to learn
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.html("""
        <div class="card">
            <div class="card-icon">▣</div>

            <h3>Summary Mode</h3>

            <p>
                Generate structured AI study notes from your lecture
                and download them as a PDF.
            </p>
        </div>
        """)

    with col2:
        st.html("""
        <div class="card">
            <div class="card-icon">▣</div>

            <h3>Test Mode</h3>

            <p>
                Test your understanding with MCQs or a speaking challenge
                and receive AI-powered feedback.
            </p>
        </div>
        """)

    # ============================================================
    # How It Works
    # ============================================================

    st.html("""
    <div class="section-title">
        How it works
    </div>
    """)

    cols = st.columns(4)

    steps = [
        ("1", "Upload Lecture", "Upload your lecture."),
        ("2", "AI Understands", "AI processes your content."),
        ("3", "Learn or Test", "Study or test yourself."),
        ("4", "Get Results", "Receive useful feedback."),
    ]

    for col, (number, title, description) in zip(cols, steps):

        with col:

            st.html(f"""
            <div class="card">
                <div class="card-icon">{number}</div>

                <h3>{title}</h3>

                <p>{description}</p>
            </div>
            """)