import assemblyai as aai
from pathlib import Path
from dependencies import Dependencies
from logger import get_logger

logger = get_logger(__name__)


def transcribe(filepath: str, deps: Dependencies) -> str:
    transcript_path = _transcript_path(filepath)

    if transcript_path.exists():
        logger.info(f"Transcript already exists, loading from disk: {transcript_path}")
        return transcript_path.read_text(encoding="utf-8")

    logger.info(f"Uploading audio for transcription: {filepath}")
    transcript = deps.assemblyai_transcriber.transcribe(filepath)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription error: {transcript.error}")

    transcript_path.write_text(transcript.text, encoding="utf-8")
    logger.info(f"Transcript saved to disk: {transcript_path}")

    return transcript.text


def _transcript_path(filepath: str) -> Path:
    """Derives transcript path from audio filepath e.g. sermon.mp3 → sermon.txt"""
    return Path(filepath).with_suffix(".txt")