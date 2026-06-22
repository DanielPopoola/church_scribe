from datetime import date
from typing import Optional
from pydantic import BaseModel
from google.genai import types
from dependencies import Dependencies
from logger import get_logger

logger = get_logger(__name__)


class BibleVerse(BaseModel):
    reference: str        # e.g. John 3:16
    translation: str      # e.g. KJV, NIV, ESV
    context: str          # why the pastor referenced it


class SermonSummary(BaseModel):
    title: str
    theme: str                        # one word or short phrase e.g. "Faith", "Prayer"
    main_message: str
    key_points: list[str]
    bible_verses: list[BibleVerse]
    practical_applications: list[str] # concrete things members can do this week
    call_to_action: Optional[str] = None
    closing_prayer_focus: Optional[str] = None  # what to pray about after service


def summarize(transcript: str, deps: Dependencies) -> SermonSummary:
    logger.info("Generating sermon summary with Gemini.")

    config = deps.config
    today = date.today().strftime("%A, %B %d, %Y")

    prompt = f"""
    You are summarizing a church sermon for members who could not attend in person.
    Be warm, spiritually sensitive, and thorough. Do not be generic.

    Service Details:
    - Church: {config.church_name}
    - Pastor: {config.pastor_name}
    - Date: {today}

    Your task is to extract the following from the transcript:

    1. **Title** - A fitting, specific sermon title. Not generic like "Sunday Service".
    2. **Theme** - One short phrase capturing the spiritual theme e.g. "Intercessory Prayer", "Walking in Faith".
    3. **Main Message** - 2-3 sentences capturing the core of what {config.pastor_name} preached. Be specific, not vague.
    4. **Key Points** - The distinct points or arguments made. Each point should be a full sentence that stands alone and captures the idea completely.
    5. **Bible Verses** - For each verse referenced:
        - The exact reference (book, chapter, verse)
        - The Bible translation used if mentioned (KJV, NIV, ESV, NLT etc). If not explicitly stated, write "Not specified".
        - A brief note on why the pastor used that verse in context of the message.
    6. **Practical Applications** - Specific, actionable things a church member can do this week based on the sermon. Not vague spiritual advice — concrete steps.
    7. **Call to Action** - The specific charge or appeal {config.pastor_name} gave at the end of the message.
    8. **Closing Prayer Focus** - The main thing the congregation was asked to pray about or believe God for.

    Transcript:
    {transcript}
    """

    response = deps.gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SermonSummary,
        ),
    )

    logger.info("Summary generated successfully.")
    return response.parsed


def format_summary(summary: SermonSummary) -> str:
    today = date.today().strftime("%A, %B %d, %Y")

    verses = "\n".join(
        f"  - {v.reference} ({v.translation}) — {v.context}"
        for v in summary.bible_verses
    ) or "None identified"

    points = "\n".join(f"  • {p}" for p in summary.key_points)
    applications = "\n".join(f"  • {a}" for a in summary.practical_applications)

    return f"""
📖 {summary.title}
🗓 {today} | Theme: {summary.theme}

MAIN MESSAGE
{summary.main_message}

KEY POINTS
{points}

BIBLE VERSES REFERENCED
{verses}

PRACTICAL APPLICATIONS THIS WEEK
{applications}

CALL TO ACTION
{summary.call_to_action or "Not specified"}

CLOSING PRAYER FOCUS
{summary.closing_prayer_focus or "Not specified"}
""".strip()