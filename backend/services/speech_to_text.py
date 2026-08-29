import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def transcribe_audio(
    audio_file_path: str,
    language: str = "en",
) -> str:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    with open(audio_file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            language=language,
            response_format="json",
            temperature=0,
        )

    return transcription.text