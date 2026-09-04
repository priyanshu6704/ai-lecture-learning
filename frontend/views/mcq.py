

import time

import streamlit as st

import api_client
from components.navigation import render_progress
from state import go_to, render_report_dict, reset_quiz_state

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False

OPTION_LETTERS = ["A", "B", "C", "D", "E", "F"]


def _extract_question(data: dict) -> dict:
    """Normalize whatever the backend returned into:
    {text, options: [str,...], total_questions, time_per_question}
    """
    q_source = data.get("question")
    if isinstance(q_source, dict):
        text = q_source.get("text") or q_source.get("question") or ""
        options = q_source.get("options") or q_source.get("choices") or []
    else:
        text = q_source or ""
        options = data.get("options") or data.get("choices") or []

    return {
        "text": text,
        "options": options,
        "total_questions": data.get("total_questions", st.session_state.quiz_total_questions),
        "time_per_question": data.get("time_per_question", st.session_state.quiz_time_per_question),
    }


def _load_question(data: dict) -> None:
    parsed = _extract_question(data)
    st.session_state.quiz_question = parsed
    if parsed["total_questions"] is not None:
        st.session_state.quiz_total_questions = parsed["total_questions"]
    if parsed["time_per_question"] is not None:
        st.session_state.quiz_time_per_question = parsed["time_per_question"]
    st.session_state["_quiz_question_start_ts"] = time.time()


def _start_screen() -> None:
    st.markdown('<div class="alp-section-title">MCQ Challenge</div>', unsafe_allow_html=True)
    st.write("Choose how many questions you'd like to answer.")

    num_questions = st.slider("Number of questions", min_value=3, max_value=20, value=10)

    if st.button("Begin Quiz", type="primary"):
        with st.spinner("Preparing your quiz..."):
            try:
                data = api_client.start_quiz(num_questions)
            except api_client.ApiError as e:
                st.error(f"Could not start quiz: {e.message}")
                return
        st.session_state.quiz_started = True
        st.session_state.quiz_question_index = 1
        _load_question(data)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Test Selection"):
        reset_quiz_state()
        go_to("test_selection")


def _submit(selected_letter: str | None, timed_out: bool) -> None:
    try:
        result = api_client.submit_quiz_answer(selected_letter, timed_out)
    except api_client.ApiError as e:
        st.error(f"Could not submit answer: {e.message}")
        return

    st.session_state.quiz_last_answer_feedback = result
    completed = result.get("completed", False)

    if completed:
        st.session_state.quiz_completed = True
    else:
        st.session_state.quiz_question_index += 1
        try:
            next_q = api_client.get_current_question()
            _load_question(next_q)
        except api_client.ApiError as e:
            st.error(f"Could not load next question: {e.message}")
            return
    st.rerun()


def _question_screen() -> None:
    q = st.session_state.quiz_question or {}
    idx = st.session_state.quiz_question_index
    total = st.session_state.quiz_total_questions or "?"

    st.markdown('<div class="alp-section-title">MCQ Challenge</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="alp-badge">Question {idx} / {total}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="alp-card"><strong>{q.get("text", "")}</strong></div>', unsafe_allow_html=True)

    time_per_q = st.session_state.quiz_time_per_question
    timed_out_now = False
    if time_per_q:
        start_ts = st.session_state.get("_quiz_question_start_ts", time.time())
        elapsed = time.time() - start_ts
        remaining = max(0, time_per_q - elapsed)
        st.progress(min(1.0, remaining / time_per_q), text=f"Time remaining: {int(remaining)}s")
        if remaining <= 0:
            timed_out_now = True
        elif HAS_AUTOREFRESH:
            st_autorefresh(interval=1000, key=f"timer_{idx}")

    options = q.get("options") or []
    selected = None
    if options:
        labeled = [f"{OPTION_LETTERS[i]}. {opt}" for i, opt in enumerate(options[:len(OPTION_LETTERS)])]
        choice = st.radio("Choose one:", labeled, index=None, label_visibility="collapsed")
        if choice:
            letter_prefix_len=choice.index(".")+2
            selected = choice[letter_prefix_len:]
    else:
        st.warning(
            "No 'options' field was found in the backend response for this question -- "
            "showing the raw payload below so you can update `_extract_question()` in "
            "pages/mcq.py to match your actual schema."
        )
        st.json(q)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit Answer", type="primary", disabled=timed_out_now and not options):
            if selected is None and not timed_out_now:
                st.warning("Select an answer before submitting.")
            else:
                _submit(selected, timed_out=timed_out_now)
    with col2:
        if timed_out_now:
            if st.button("Continue (time's up)"):
                _submit(None, timed_out=True)

    if st.session_state.quiz_last_answer_feedback and not st.session_state.quiz_completed:
        fb = st.session_state.quiz_last_answer_feedback
        if fb.get("answer"):
            st.caption(f"Previous answer: {fb.get('answer')}")


def _result_screen() -> None:
    st.markdown('<div class="alp-section-title">MCQ Results</div>', unsafe_allow_html=True)

    if st.session_state.quiz_result is None:
        with st.spinner("Fetching your results..."):
            try:
                st.session_state.quiz_result = api_client.get_quiz_result()
            except api_client.ApiError as e:
                st.error(f"Could not fetch result: {e.message}")
                return

    result = st.session_state.quiz_result
    render_report_dict(result) if isinstance(result, dict) else st.write(result)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Quiz Report", type="primary", use_container_width=True):
            with st.spinner("Generating report..."):
                try:
                    st.session_state.quiz_report = api_client.generate_quiz_report()
                except api_client.ApiError as e:
                    st.error(f"Could not generate report: {e.message}")
                    return
    with col2:
        if st.button("Continue to Speaking Challenge →", use_container_width=True):
            go_to("speaking")

    if st.session_state.quiz_report:
        st.markdown('<div class="alp-section-title">Quiz Report</div>', unsafe_allow_html=True)
        report=(st.session_state.quiz_report)
        render_report_dict(report) if isinstance(report, dict) else st.write(report)
        if st.button("Go to Final Report →", type="primary"):
            go_to("report")


def render() -> None:
    render_progress(active_index=3)

    if not st.session_state.quiz_started:
        _start_screen()
    elif st.session_state.quiz_completed:
        _result_screen()
    else:
        _question_screen()
