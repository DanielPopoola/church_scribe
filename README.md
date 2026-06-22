# ChurchScribe

Automated sermon transcription and summary pipeline. Watches a folder for new audio recordings, transcribes them, generates a structured AI summary, and delivers it to your congregation via email, Telegram, and WhatsApp — automatically after every service.

---

## How It Works

```
Audio file saved to folder
    → Folder watcher detects it
        → Waits for file to finish saving
            → Uploads to AssemblyAI for transcription
                → Transcript saved to disk
                    → Gemini generates structured summary
                        → Summary sent via Email / Telegram / WhatsApp
```

---

## Project Structure

```
church_scribe/
├── .env                  # All config and secrets (never commit this)
├── main.py               # Entry point
├── config.py             # Reads and validates environment variables
├── dependencies.py       # Initializes all external clients
├── watcher.py            # Detects new audio files in the watch folder
├── pipeline.py           # Orchestrates transcription → summary → notify
├── transcriber.py        # AssemblyAI transcription logic
├── summarizer.py         # Gemini summarization logic
├── notifier.py           # Email, Telegram, WhatsApp delivery
├── logger.py             # Centralized logging setup
└── church_scribe.log     # Runtime log file (auto-generated)
```

---

## Prerequisites

- Python 3.10+
- An [AssemblyAI](https://assemblyai.com) account (free tier: 5 hours/month)
- A [Google Gemini](https://aistudio.google.com) API key
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) configured
- _(Optional)_ A Telegram bot token from [@BotFather](https://t.me/botfather)
- _(Optional)_ A [Twilio](https://twilio.com) account for WhatsApp

---

## Setup

**1. Clone the project and install dependencies**

```bash
git clone https://github.com/DanielPopoola/church_scribe.git
cd church_scribe
pip install watchdog assemblyai google-genai python-telegram-bot twilio python-dotenv
```

**2. Configure your `.env` file**

Copy the example below and fill in your values:

```bash
# Folder to watch for new audio recordings
WATCH_FOLDER=C:\Users\user\ChurchRecordings

# AssemblyAI
ASSEMBLYAI_API_KEY=your_key_here

# Google Gemini
GEMINI_API_KEY=your_key_here

# Email (Gmail + App Password)
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECEIVER=you@gmail.com

# Church details (used in the summary)
CHURCH_NAME=Your Church Name
PASTOR_NAME=Pastor John Doe

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here

# WhatsApp via Twilio (optional)
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_GROUP_ID=your_group_id_here
```

> **Gmail App Password:** Go to Google Account → Security → 2-Step Verification → App Passwords. Generate one for "Mail" and use that instead of your regular password.

**3. Run the script**

```bash
python main.py
```

You should see:

```
2026-06-22 10:00:00 | INFO | watcher | Watching folder: C:\Users\user\ChurchRecordings
```

Drop any audio file into the watch folder — the pipeline fires automatically.

---

## Supported Audio Formats

`.mp3` `.wav` `.m4a` `.ogg` `.flac`

---

## Summary Output

Each sermon generates a structured summary including:

| Field | Description |
|---|---|
| **Title** | A fitting sermon title inferred from the message |
| **Theme** | One short phrase capturing the spiritual theme |
| **Main Message** | 2-3 sentences capturing the core of the sermon |
| **Key Points** | Distinct arguments made by the pastor |
| **Bible Verses** | Reference, translation used, and context for each verse |
| **Practical Applications** | Concrete actions members can take this week |
| **Call to Action** | The specific charge given at the end of the message |
| **Closing Prayer Focus** | What the congregation was asked to pray about |

---

## Running on Startup (Windows)

To have ChurchScribe start automatically when the PC boots:

1. Open **Task Scheduler** and create a new task
2. **General tab:** Check *"Run whether user is logged in or not"* and *"Run with highest privileges"*
3. **Triggers tab:** New trigger → *At startup*
4. **Actions tab:** New action → *Start a program*
   - Program: `C:\path\to\python.exe` _(run `where python` to find this)_
   - Arguments: `main.py`
   - Start in: `C:\path\to\church_scribe`
5. **Settings tab:** Check *"If the task fails, restart every 1 minute"*

Reboot and verify it's running via Task Manager → Details → look for `python.exe`.

---

## Transcript Caching

Transcripts are saved to disk alongside the audio file immediately after transcription (e.g. `sermon.mp3` → `sermon.txt`). If the pipeline fails at the summarization or notification step, rerunning it will load the transcript from disk — no repeat API calls to AssemblyAI.

---

## Logging

All activity is logged to both the terminal and `church_scribe.log` in the project root:

```
2026-06-22 10:01:00 | INFO | watcher     | New audio file detected: sermon.mp3
2026-06-22 10:01:05 | INFO | watcher     | File ready, starting pipeline: sermon.mp3
2026-06-22 10:01:06 | INFO | transcriber | Uploading audio for transcription: sermon.mp3
2026-06-22 10:03:21 | INFO | transcriber | Transcript saved to disk: sermon.txt
2026-06-22 10:03:22 | INFO | summarizer  | Generating sermon summary with Gemini.
2026-06-22 10:03:25 | INFO | summarizer  | Summary generated successfully.
2026-06-22 10:03:26 | INFO | notifier    | Email sent to you@gmail.com
2026-06-22 10:03:26 | INFO | pipeline    | Pipeline completed successfully.
```

---

## Adding More Notification Channels

Open `notifier.py` and add a new function following the same pattern as `send_email`. Then add it to the `channels` list in `send()`:

```python
def send_slack(summary: str, deps: Dependencies) -> None:
    # your logic here
    pass

def send(summary: str, deps: Dependencies) -> None:
    channels = [send_email, send_telegram, send_whatsapp, send_slack]
    ...
```

No other files need to change.

---

## License

MIT