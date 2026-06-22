import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dependencies import Dependencies
from logger import get_logger

logger = get_logger(__name__)


def send_email(summary: str, deps: Dependencies) -> None:
    config = deps.config
    msg = MIMEMultipart()
    msg["From"] = config.email_sender
    msg["To"] = config.email_receiver
    msg["Subject"] = "Sunday Service Summary"
    msg.attach(MIMEText(summary, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config.email_sender, config.email_password)
        server.sendmail(config.email_sender, config.email_receiver, msg.as_string())

    logger.info(f"Email sent to {config.email_receiver}")


def send_telegram(summary: str, deps: Dependencies) -> None:
    pass


def send_whatsapp(summary: str, deps: Dependencies) -> None:
    pass


def send(summary: str, deps: Dependencies) -> None:
    channels = [send_email, send_telegram, send_whatsapp]

    for channel in channels:
        try:
            channel(summary, deps)
        except Exception as e:
            logger.error(f"{channel.__name__} failed: {e}")