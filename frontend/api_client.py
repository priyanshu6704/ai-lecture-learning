"""
api_client.py

Every HTTP call to the FastAPI backend lives here -- nowhere else in the
app should call `requests` directly. This keeps the API contract in one
place and matches the spec's rule to centralize communication.

IMPORTANT -- a couple of field names had to be assumed because the
`schemas/*.py` files themselves weren't provided, only the API spec doc.
Anywhere that's true is flagged with an "ASSUMPTION" comment. If your
actual FastAPI route expects a different multipart field name or JSON
key, change it here ONLY -- the rest of the app never needs to know.

No endpoints beyond what's in the spec are invented. If a page needs
something the backend doesn't expose yet, it should say so rather than
fabricate a call.
"""

from __future__ import annotations

import requests

import os
BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
TIMEOUT = 60  # seconds; default for fast endpoints
LONG_TIMEOUT = 600  # seconds; for endpoints that chunk + call the LLM
                     # repeatedly (notes generation, reports) and can
                     # legitimately take several minutes on a long lecture


class ApiError(Exception):
    """Raised for any non-2xx response or network failure, with a
    human-readable message the UI can show directly."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _handle(resp: requests.Response) -> dict:
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except ValueError:
            detail = resp.text
        raise ApiError(f"{detail}", status_code=resp.status_code)
    if not resp.content:
        return {}
    try:
        return resp.json()
    except ValueError:
        return {}


def _get(path: str, timeout: int = TIMEOUT, **kwargs) -> dict:
    try:
        resp = requests.get(f"{BASE_URL}{path}", timeout=timeout, **kwargs)
    except requests.exceptions.Timeout:
        raise ApiError(
            f"The server didn't respond within {timeout}s for {path}. "
            "This endpoint can be slow on long lectures -- if it keeps "
            "happening, it may still be worth raising the timeout further."
        )
    except requests.exceptions.RequestException as e:
        raise ApiError(f"Could not reach backend at {BASE_URL}{path} ({e})")
    return _handle(resp)


def _post(path: str, timeout: int = TIMEOUT, **kwargs) -> dict:
    try:
        resp = requests.post(f"{BASE_URL}{path}", timeout=timeout, **kwargs)
    except requests.exceptions.Timeout:
        raise ApiError(
            f"The server didn't respond within {timeout}s for {path}. "
            "This endpoint can be slow on long lectures -- if it keeps "
            "happening, it may still be worth raising the timeout further."
        )
    except requests.exceptions.RequestException as e:
        raise ApiError(f"Could not reach backend at {BASE_URL}{path} ({e})")
    return _handle(resp)


# ---------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------

def check_health() -> bool:
    try:
        data = _get("/health")
        return data.get("status") == "healthy"
    except ApiError:
        return False


# ---------------------------------------------------------------------
# Lecture upload + study notes
# ---------------------------------------------------------------------

def upload_lecture(file) -> dict:
    """file: a Streamlit UploadedFile (.pdf/.docx/.pptx).

    ASSUMPTION: multipart field name is "file". Adjust here if
    backend/main.py's /upload route names it differently.
    """
    files = {"file": (file.name, file.getvalue(), file.type)}
    return _post("/upload", files=files, timeout=LONG_TIMEOUT)


def generate_notes() -> dict:
    """Returns {"study_notes": {...}} per the StudyNotes schema.

    Chunks the lecture and calls the LLM once per chunk plus merge
    batches, so this can legitimately take several minutes on a long
    lecture -- use the long timeout.
    """
    return _post("/generate-notes", timeout=LONG_TIMEOUT)


def generate_notes_pdf() -> dict:
    """Returns {"message": ..., "file": "study_notes.pdf"}.

    NOTE: per spec, the backend currently returns only a filename, not
    file bytes -- so this cannot trigger a real browser download yet.
    The UI surfaces that limitation instead of inventing a download
    endpoint.
    """
    return _post("/generate-notes-pdf", timeout=LONG_TIMEOUT)

def download_notes_pdf() -> bytes:
    resp = requests.get(f"{BASE_URL}/download/notes-pdf", timeout=LONG_TIMEOUT)
    if resp.status_code >= 400:
        raise ApiError("PDF not available yet -- generate it first.", status_code=resp.status_code)
    return resp.content
# ---------------------------------------------------------------------
# MCQ quiz
# ---------------------------------------------------------------------

def start_quiz(number_of_questions: int) -> dict:
    return _post(
        "/quiz/start",
        params={"number_of_questions": number_of_questions},
    )


def get_current_question() -> dict:
    return _get("/quiz/current")


def submit_quiz_answer(selected_answer: str | None, timed_out: bool = False) -> dict:
    return _post(
        "/quiz/answer",
        json={"selected_answer": selected_answer, "timed_out": timed_out},
    )


def get_quiz_result() -> dict:
    return _get("/quiz/result")


def generate_quiz_report() -> dict:
    return _post("/quiz/report", timeout=LONG_TIMEOUT)


# ---------------------------------------------------------------------
# Speaking challenge
# ---------------------------------------------------------------------

def generate_speaking_question(topic: str) -> dict:
    return _post("/speaking/question", json={"topic": topic})


def transcribe_audio(audio_bytes: bytes, filename: str = "answer.wav", mime: str = "audio/wav") -> dict:
    """ASSUMPTION: multipart field name is "file", matching /upload's
    convention. Adjust here if the backend names it e.g. "audio_file"."""
    files = {"file": (filename, audio_bytes, mime)}
    return _post("/speaking/transcribe", files=files)


def evaluate_speaking_answer(transcript: str) -> dict:
    return _post("/speaking/evaluate", json={"transcript": transcript})


def generate_speaking_report() -> dict:
    return _post("/speaking/report", timeout=LONG_TIMEOUT)