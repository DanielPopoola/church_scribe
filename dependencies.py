# dependencies.py
import assemblyai as aai
from google import genai
from dataclasses import dataclass
from config import Config


@dataclass(frozen=True)
class Dependencies:
    assemblyai_transcriber: aai.Transcriber
    gemini_client: genai.Client
    config: Config


def build_dependencies(config: Config) -> Dependencies:
    aai.settings.api_key = config.assemblyai_api_key

    gemini_client = genai.Client(api_key=config.gemini_api_key)

    return Dependencies(
        assemblyai_transcriber=aai.Transcriber(),
        gemini_client=gemini_client,
        config=config,
    )