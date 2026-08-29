from backend.schemas.speaking import SpeechTranscript

def create_transcript(
        transcript_text:str,
        language:str|None=None,
)->SpeechTranscript:
    return SpeechTranscript(
        transcript=transcript_text.strip(),
        language=language,
    )