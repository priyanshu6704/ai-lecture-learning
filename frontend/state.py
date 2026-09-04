"""
state.py

Single place that defines and initializes st.session_state.
No database, no auth -- everything here is per-browser-session only,
exactly as the spec requires.
"""

import streamlit as st

DEFAULT_STATE = {
    # navigation
    "page": "home",
    # upload
    "lecture_uploaded": False,
    "filename": None,
    "document_count": None,
    # study notes
    "study_notes": None,
    "notes_pdf_info": None,
    # mcq
    "quiz_started": False,
    "quiz_question": None,        # current question payload from backend
    "quiz_total_questions": None,
    "quiz_time_per_question": None,
    "quiz_question_index": 0,
    "quiz_completed": False,
    "quiz_last_answer_feedback": None,
    "quiz_result": None,
    "quiz_report": None,
    # speaking
    "speaking_topic": None,
    "speaking_question": None,
    "transcript": None,
    "speaking_evaluation": None,
    "speaking_report": None,
    # final report
    "final_report": None,
}


def init_state() -> None:
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page: str) -> None:
    """Navigate to another page and rerun immediately."""
    st.session_state.page = page
    st.rerun()


def reset_quiz_state() -> None:
    for key in (
        "quiz_started",
        "quiz_question",
        "quiz_total_questions",
        "quiz_time_per_question",
        "quiz_question_index",
        "quiz_completed",
        "quiz_last_answer_feedback",
        "quiz_result",
        "quiz_report",
    ):
        st.session_state[key] = DEFAULT_STATE[key]


def reset_speaking_state() -> None:
    for key in (
        "speaking_topic",
        "speaking_question",
        "transcript",
        "speaking_evaluation",
        "speaking_report",
    ):
        st.session_state[key] = DEFAULT_STATE[key]


def reset_session_for_new_lecture() -> None:
    """Used by 'Try Again' on the report page -- keeps nothing but the page."""
    current_page = st.session_state.get("page", "home")
    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value
    st.session_state.page = current_page

def render_report_dict(data: dict) -> None:
    for key, value in data.items():
        label = key.replace("_", " ").title()
        if isinstance(value, list):
            st.markdown(f'<div class="alp-section-title">{label}</div>', unsafe_allow_html=True)
            for item in value:
                if isinstance(item, dict):
                    render_report_dict(item)
                else:
                    st.markdown(f'<div class="alp-card quiet">{item}</div>', unsafe_allow_html=True)
        elif isinstance(value, dict):
            st.markdown(f'<div class="alp-section-title">{label}</div>', unsafe_allow_html=True)
            render_report_dict(value)
        else:
            st.markdown(
                f'<div class="alp-card"><strong>{label}</strong>: {value}</div>',
                unsafe_allow_html=True,
            )
