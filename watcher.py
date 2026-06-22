# watcher.py
import time
from pathlib import Path
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from dependencies import Dependencies
from logger import get_logger
import pipeline

logger = get_logger(__name__)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}


def wait_for_file_ready(filepath: str, stable_seconds: int = 5) -> None:
    path = Path(filepath)
    last_size = -1

    while True:
        current_size = path.stat().st_size
        if current_size == last_size:
            break
        last_size = current_size
        time.sleep(stable_seconds)


class AudioHandler(FileSystemEventHandler):
    def __init__(self, deps: Dependencies):
        self.deps = deps

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        if Path(filepath).suffix.lower() not in AUDIO_EXTENSIONS:
            return

        logger.info(f"New audio file detected: {filepath}")
        wait_for_file_ready(filepath)
        logger.info(f"File ready, starting pipeline: {filepath}")
        pipeline.run(filepath, self.deps)


def start(deps: Dependencies) -> None:
    observer = PollingObserver()  # ← changed
    observer.schedule(AudioHandler(deps), path=deps.config.watch_folder, recursive=False)
    observer.start()
    logger.info(f"Watching folder: {deps.config.watch_folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watcher stopped.")

    observer.join()