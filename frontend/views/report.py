"""pages/report.py

NOTE: the spec's API contract (section 6-15) never lists a dedicated
"combine everything" endpoint, even though `schemas/test_report.py` and
`schemas/report_analysis.py` exist in the backend -- which strongly
suggests one exists (e.g. something like POST /report or
/test-report/generate) but wasn't included in the doc you gave me.

Rather than invent that route, this page renders the final report from
the two results the app already has in session state -- the MCQ report
(`/quiz/report`) and the speaking report (`/speaking/report`) -- exactly
as returned by the backend, with no scoring done in the frontend. If you
do have a combined-report endpoint, tell me its path/method and I'll
wire it in here as a single source of truth instead.
"""

import streamlit as st

from components.navigation import render_progress
from state import go_to, reset_session_for_new_lecture, render_report_dict


def render() -> None:
    render_progress(active_index=4)

    st.markdown('<div class="alp-kicker">FINAL REPORT CARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="alp-hero-title" style="font-size:2rem;">Your learning results.</div>', unsafe_allow_html=True)

    quiz_report = st.session_state.quiz_report
    speaking_report = st.session_state.speaking_report

    if not quiz_report and not speaking_report:
        st.markdown(
            '<div class="alp-empty">No results yet -- complete the MCQ and/or Speaking '
            "challenge to see your report here.</div>",
            unsafe_allow_html=True,
        )
    else:
        if quiz_report:
            st.markdown('<div class="alp-section-title">MCQ Score</div>', unsafe_allow_html=True)
            render_report_dict(quiz_report) if isinstance(quiz_report, dict) else st.write(quiz_report)
    

        if speaking_report:
            st.markdown('<div class="alp-section-title">Speaking Score</div>', unsafe_allow_html=True)
            render_report_dict(speaking_report) if isinstance(speaking_report, dict) else st.write(speaking_report)


    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again", use_container_width=True):
            reset_session_for_new_lecture()
            go_to("home")
    with col2:
        if st.button("Back to Study Notes", use_container_width=True):
            go_to("study")
