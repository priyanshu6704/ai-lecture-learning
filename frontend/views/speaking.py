"""pages/speaking.py

Recording: uses `st.audio_input` (built into Streamlit >= 1.35) when
available for a real in-browser mic recorder with no JS of our own. On
older Streamlit versions it falls back to a plain audio file uploader,
so the page still works either way.
"""

import streamlit as st

import api_client
from components.navigation import render_progress
from state import go_to, render_report_dict, reset_speaking_state

HAS_AUDIO_INPUT = hasattr(st, "audio_input")

def _extract_transcript_text(data: dict) -> str:
   
    value = data.get("transcript") or data.get("text") or ""
    if isinstance(value, dict):
        value = value.get("transcript") or value.get("text") or ""
    return value

def _extract_question_text(data: dict) -> str:            # ← ADD THIS
    """/speaking/question has been observed to return either a flat
    string under "question", or a nested object. Handle both so we
    never display a raw dict in the UI."""

    value = data.get("question") or ""
    if isinstance(value, dict):
        value = value.get("question") or value.get("text") or ""
    return value

def _derive_topic() -> str:
    """Pick a topic automatically from what we already know about the
    uploaded lecture, instead of asking the user to type one."""

    notes = st.session_state.study_notes or {}
    key_concepts = notes.get("key_concepts") or []
    if key_concepts:
        return key_concepts[0]

    summary = notes.get("lecture_summary")
    if summary:
        return summary[:80]

    if st.session_state.filename:
        return st.session_state.filename.rsplit(".", 1)[0]

    return ""


def _topic_screen() -> None:
    st.markdown('<div class="alp-section-title">Speaking Challenge</div>', unsafe_allow_html=True)

    topic = _derive_topic()

    if not topic:
        st.warning("Couldn't determine a topic from the uploaded lecture. Go back and generate study notes first.")
        if st.button("← Back to Study Notes"):
            go_to("study")
        return

    with st.spinner("Generating your question..."):
        try:
            data = api_client.generate_speaking_question(topic)
        except api_client.ApiError as e:
            st.error(f"Could not generate question: {e.message}")
            return

    st.session_state.speaking_topic = topic
    st.session_state.speaking_question = _extract_question_text(data)
    st.rerun()


def _record_screen() -> None:
    st.markdown('<div class="alp-section-title">Speaking Challenge</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="alp-badge accent">Topic: {st.session_state.speaking_topic}</span>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="alp-card">{st.session_state.speaking_question}</div>',
        unsafe_allow_html=True,
    )

    audio_bytes = None
    filename = "answer.wav"
    mime = "audio/wav"

    if HAS_AUDIO_INPUT:
        recording = st.audio_input("Record your answer")
        if recording is not None:
            audio_bytes = recording.getvalue()
            mime = recording.type or mime
    else:
        st.caption("Live mic recording needs Streamlit ≥ 1.35 -- upload an audio file instead.")
        uploaded = st.file_uploader("Upload your answer (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])
        if uploaded is not None:
            audio_bytes = uploaded.getvalue()
            filename = uploaded.name
            mime = uploaded.type or mime

    if audio_bytes and st.session_state.transcript is None:
        if st.button("Transcribe Answer", type="primary"):
            with st.spinner("Transcribing with Whisper..."):
                try:
                    data = api_client.transcribe_audio(audio_bytes, filename=filename, mime=mime)
                except api_client.ApiError as e:
                    st.error(f"Could not transcribe audio: {e.message}")
                    return
            st.session_state.transcript = _extract_transcript_text(data)
            st.rerun()

    if st.session_state.transcript is not None:
        st.markdown('<div class="alp-section-title">Your Answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="alp-card quiet">{st.session_state.transcript}</div>', unsafe_allow_html=True)

        if st.session_state.speaking_evaluation is None:
            if st.button("Evaluate Answer", type="primary"):
                with st.spinner("Evaluating your answer..."):
                    try:
                        result = api_client.evaluate_speaking_answer(st.session_state.transcript)
                    except api_client.ApiError as e:
                        st.error(f"Could not evaluate answer: {e.message}")
                        return
                st.session_state.speaking_evaluation = result
                st.rerun()

    if st.session_state.speaking_evaluation:
        _result_block()


def _result_block() -> None:
    result = st.session_state.speaking_evaluation
    is_correct = result.get("is_correct")
    evaluation_text = result.get("evaluation", "")

    st.markdown('<div class="alp-section-title">Result</div>', unsafe_allow_html=True)
    badge_cls = "success" if is_correct else "danger"
    badge_label = "Correct" if is_correct else "Needs Work"
    st.markdown(f'<span class="alp-badge {badge_cls}">{badge_label}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="alp-card">{evaluation_text}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Speaking Report", type="primary", use_container_width=True):
            with st.spinner("Generating report..."):
                try:
                    st.session_state.speaking_report = api_client.generate_speaking_report()
                except api_client.ApiError as e:
                    st.error(f"Could not generate report: {e.message}")
                    return
    with col2:
        if st.button("Continue →", use_container_width=True):
            go_to("report")

    if st.session_state.speaking_report:
        st.markdown('<div class="alp-section-title">Speaking Report</div>', unsafe_allow_html=True)
        report=(st.session_state.speaking_report)
        render_report_dict(report) if isinstance(report, dict) else st.write(report)


def render() -> None:
    render_progress(active_index=3)

    if st.session_state.speaking_question is None:
        _topic_screen()
    else:
        _record_screen()
