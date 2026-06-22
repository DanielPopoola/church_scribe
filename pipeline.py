from dependencies import Dependencies
from transcriber import transcribe
from summarizer import summarize, format_summary
from notifier import send
from logger import get_logger

logger = get_logger(__name__)


def run(filepath: str, deps: Dependencies) -> None:
    logger.info(f"Pipeline started for: {filepath}")

    try:
        transcript = transcribe(filepath, deps)
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return

    try:
        summary = summarize(transcript, deps)
        formatted = format_summary(summary)
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return

    try:
        send(formatted, deps)
    except Exception as e:
        logger.error(f"Notification failed: {e}")
        return

    logger.info("Pipeline completed successfully.")