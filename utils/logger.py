import logging
import sys
from pathlib import Path

def setup_logger(name="AIOS", level=logging.INFO):
    """Setup logger with console and file output (singleton pattern)."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(logs_dir / "ai_os.log", encoding="utf-8")
        file_handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()
