from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path

from backend.document_loader import load_document

from backend.services.lecture_rag import (
    build_lecture_knowledge_base,
    generate_study_notes,
    search_lecture,
)

from backend.services.pdf_generator import generate_notes_pdf

from backend.services.mcq_generator import generate_mcq_game

from backend.services.quiz_session_service import (
    start_quiz,
    get_current_question,
    submit_answer,
    get_quiz_result,
)

from backend.services.speaking_question_generator import (
    generate_speaking_question,
)

from backend.services.speech_to_text import (
    transcribe_audio,
)

from backend.services.transcript_service import (
    create_transcript,
)

from backend.services.speaking_evaluator import (
    evaluate_spoken_answer,
)

from backend.services.test_report_generator import (
    generate_mcq_report,
    generate_speaking_report,
)


app = FastAPI()


# Temporary application state
documents = None
vector_store = None
quiz_session = None
speaking_question = None
speaking_context = None
speaking_evaluation = None


class QuizAnswerRequest(BaseModel):
    selected_answer: str | None = None
    timed_out: bool = False


class SpeakingQuestionRequest(BaseModel):
    topic: str


class SpeakingEvaluationRequest(BaseModel):
    transcript: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_lecture(
    file: UploadFile = File(...)
):
    global documents
    global vector_store

    try:
        suffix = Path(file.filename).suffix

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            contents = await file.read()
            temp_file.write(contents)

            file_path = temp_file.name

        documents = load_document(file_path)

        vector_store = build_lecture_knowledge_base(
            documents
        )

        return {
            "message": "Lecture uploaded successfully",
            "filename": file.filename,
            "document_count": len(documents),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


study_notes_cache = None


@app.post("/generate-notes")
async def generate_notes():

    global documents, study_notes_cache

    if documents is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    try:

        notes = generate_study_notes(
            documents
        )

        study_notes_cache = notes

        return {
            "study_notes": notes
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/generate-notes-pdf")
async def generate_notes_pdf_endpoint():

    global documents, study_notes_cache

    if documents is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    try:

        notes = study_notes_cache if study_notes_cache is not None else generate_study_notes(documents)

        output_path = "study_notes.pdf"

        generate_notes_pdf(
            notes,
            output_path
        )

        return {
            "message": "PDF generated successfully",
            "file": output_path,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/download/notes-pdf")
async def download_notes_pdf():

    file_path = Path("study_notes.pdf")

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="No PDF found. Generate the notes PDF first."
        )

    return FileResponse(
        path=str(file_path),
        filename="study_notes.pdf",
        media_type="application/pdf",
    )

@app.post("/quiz/start")
async def start_mcq_quiz(
    number_of_questions: int = 10,
):

    global vector_store
    global quiz_session

    if vector_store is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    try:

        game = generate_mcq_game(
            vector_store,
            number_of_questions
        )

        quiz_session = start_quiz(
            game
        )

        question = get_current_question(
            quiz_session
        )

        return {
            "question": question,
            "total_questions": len(game.questions),
            "time_per_question": game.time_per_question,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/quiz/answer")
async def answer_quiz_question(
    request: QuizAnswerRequest
):

    global quiz_session

    if quiz_session is None:

        raise HTTPException(
            status_code=400,
            detail="Quiz has not been started."
        )

    try:

        answer = submit_answer(
            session=quiz_session,
            selected_answer=request.selected_answer,
            timed_out=request.timed_out,
        )

        return {
            "answer": answer,
            "completed": quiz_session.completed,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/quiz/current")
async def current_quiz_question():

    global quiz_session

    if quiz_session is None:

        raise HTTPException(
            status_code=400,
            detail="Quiz has not been started."
        )

    question = get_current_question(
        quiz_session
    )

    return {
        "question": question
    }


@app.get("/quiz/result")
async def quiz_result():

    global quiz_session

    if quiz_session is None:

        raise HTTPException(
            status_code=400,
            detail="Quiz has not been started."
        )

    try:

        result = get_quiz_result(
            quiz_session
        )

        return {
            "result": result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/quiz/report")
async def quiz_report():

    global quiz_session
    global documents

    if quiz_session is None:

        raise HTTPException(
            status_code=400,
            detail="Quiz has not been started."
        )

    if documents is None:

        raise HTTPException(
            status_code=400,
            detail="Lecture has not been uploaded."
        )

    try:

        result = get_quiz_result(
            quiz_session
        )

        lecture_context = "\n\n".join(
            document.page_content
            for document in documents
        )

        report = generate_mcq_report(
            quiz_result=result,
            lecture_context=lecture_context,
        )

        return {
            "report": report
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/speaking/question")
async def create_speaking_question(
    request: SpeakingQuestionRequest
):

    global vector_store
    global speaking_question
    global speaking_context

    if vector_store is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    try:

        question = generate_speaking_question(
            vector_store=vector_store,
            topic=request.topic,
        )

        documents = search_lecture(
            vector_store=vector_store,
            query=request.topic,
            k=3,
        )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        speaking_question = question
        speaking_context = context

        return {
            "question": question
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/speaking/transcribe")
async def transcribe_speaking_audio(
    file: UploadFile = File(...)
):

    try:

        suffix = Path(file.filename).suffix

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            contents = await file.read()
            temp_file.write(contents)

            audio_path = temp_file.name

        transcript_text = transcribe_audio(
            audio_file_path=audio_path
        )

        transcript = create_transcript(
            transcript_text=transcript_text
        )

        return {
            "transcript": transcript
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/speaking/evaluate")
async def evaluate_speaking_answer(
    request: SpeakingEvaluationRequest
):

    global speaking_question
    global speaking_context
    global speaking_evaluation

    if speaking_question is None:

        raise HTTPException(
            status_code=400,
            detail="Speaking question has not been generated."
        )

    if speaking_context is None:

        raise HTTPException(
            status_code=400,
            detail="Lecture context is not available."
        )

    try:

        evaluation = evaluate_spoken_answer(
            question=speaking_question.question,
            transcript=request.transcript,
            lecture_context=speaking_context,
        )

        speaking_evaluation = evaluation

        return {
            "evaluation": evaluation,
            "is_correct": evaluation.is_correct,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/speaking/report")
async def speaking_report():

    global speaking_evaluation
    global speaking_context

    if speaking_evaluation is None:

        raise HTTPException(
            status_code=400,
            detail="Speaking evaluation has not been completed."
        )

    if speaking_context is None:

        raise HTTPException(
            status_code=400,
            detail="Lecture context is not available."
        )

    try:

        report = generate_speaking_report(
            evaluation=speaking_evaluation,
            lecture_context=speaking_context,
        )

        return {
            "report": report
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )