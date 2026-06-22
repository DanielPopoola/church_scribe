import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    watch_folder: str
    assemblyai_api_key: str
    gemini_api_key: str
    email_sender: str
    email_password: str
    email_receiver: str
    church_name: str
    pastor_name: str


def load_config() -> Config:
    missing = []
    required = [
        "WATCH_FOLDER",
        "ASSEMBLYAI_API_KEY",
        "GEMINI_API_KEY",
        "EMAIL_SENDER",
        "EMAIL_PASSWORD",
        "EMAIL_RECEIVER",
        "CHURCH_NAME",
        "PASTOR_NAME",
    ]

    for key in required:
        if not os.getenv(key):
            missing.append(key)

    if missing:
        raise RuntimeError(f"Missing required environment variables: {missing}")

    return Config(
        watch_folder=os.getenv("WATCH_FOLDER"),
        assemblyai_api_key=os.getenv("ASSEMBLYAI_API_KEY"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        email_sender=os.getenv("EMAIL_SENDER"),
        email_password=os.getenv("EMAIL_PASSWORD"),
        email_receiver=os.getenv("EMAIL_RECEIVER"),
        church_name=os.getenv("CHURCH_NAME"),
        pastor_name=os.getenv("PASTOR_NAME"),
    )