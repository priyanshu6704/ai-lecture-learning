import requests


# ============================================================
# FastAPI Configuration
# ============================================================

BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# Helper
# ============================================================

def handle_response(response):
    """
    Handle FastAPI response and raise a useful error
    when the request fails.
    """

    if response.ok:
        return response.json()

    try:
        error = response.json().get("detail", "Request failed.")
    except Exception:
        error = "Request failed."

    raise Exception(error)


# ============================================================
# Health
# ============================================================

def check_health():
    response = requests.get(
        f"{BASE_URL}/health"
    )

    return handle_response(response)


# ============================================================
# Lecture Upload
# ============================================================

def upload_lecture(file):
    """
    Upload lecture file to FastAPI.
    """

    files = {
        "file": (
            file.name,
            file.getvalue(),
            file.type,
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files,
    )

    return handle_response(response)


# ============================================================
# Study Notes
# ============================================================

def generate_notes():
    """
    Generate AI study notes.
    """

    response = requests.post(
        f"{BASE_URL}/generate-notes"
    )

    return handle_response(response)


def generate_notes_pdf():
    """
    Generate study notes PDF.
    """

    response = requests.post(
        f"{BASE_URL}/generate-notes-pdf"
    )

    return handle_response(response)


# ============================================================
# MCQ Quiz
# ============================================================

def start_quiz(number_of_questions=10):
    """
    Start a new MCQ quiz.
    """

    response = requests.post(
        f"{BASE_URL}/quiz/start",
        params={
            "number_of_questions": number_of_questions
        },
    )

    return handle_response(response)


def get_current_question():
    """
    Get current quiz question.
    """

    response = requests.get(
        f"{BASE_URL}/quiz/current"
    )

    return handle_response(response)


def submit_quiz_answer(
    selected_answer=None,
    timed_out=False,
):
    """
    Submit answer for current MCQ.
    """

    response = requests.post(
        f"{BASE_URL}/quiz/answer",
        json={
            "selected_answer": selected_answer,
            "timed_out": timed_out,
        },
    )

    return handle_response(response)


def get_quiz_result():
    """
    Get final quiz result.
    """

    response = requests.get(
        f"{BASE_URL}/quiz/result"
    )

    return handle_response(response)


def generate_quiz_report():
    """
    Generate AI report for MCQ performance.
    """

    response = requests.post(
        f"{BASE_URL}/quiz/report"
    )

    return handle_response(response)


# ============================================================
# Speaking Challenge
# ============================================================

def generate_speaking_question(topic):
    """
    Generate speaking question from lecture.
    """

    response = requests.post(
        f"{BASE_URL}/speaking/question",
        json={
            "topic": topic
        },
    )

    return handle_response(response)


def transcribe_audio(audio_file):
    """
    Send recorded/uploaded audio to speech-to-text API.
    """

    files = {
        "file": (
            audio_file.name,
            audio_file.getvalue(),
            audio_file.type,
        )
    }

    response = requests.post(
        f"{BASE_URL}/speaking/transcribe",
        files=files,
    )

    return handle_response(response)


def evaluate_speaking_answer(transcript):
    """
    Evaluate the spoken answer.
    """

    response = requests.post(
        f"{BASE_URL}/speaking/evaluate",
        json={
            "transcript": transcript
        },
    )

    return handle_response(response)


def generate_speaking_report():
    """
    Generate speaking performance report.
    """

    response = requests.post(
        f"{BASE_URL}/speaking/report"
    )

    return handle_response(response)