# /core/agent_messaging/handlers/error_handler.py

import logging
from typing import Dict, Any, Optional

# Configure logger for error handling
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def handle(message_dict: Dict[str, Any], error_msg: str, context: Optional[str] = None) -> None:
    """
    Handles and logs an error that occurred during message processing.

    Parameters:
    - message_dict (dict): The raw message that caused the error.
    - error_msg (str): A string describing the error.
    - context (str, optional): Additional context (e.g., handler name or task type).
    """
    try:
        logger.error("[ErrorHandler] Message processing failed.")
        logger.error(f"Context     : {context if context else 'N/A'}")
        logger.error(f"Message     : {message_dict}")
        logger.error(f"Error Reason: {error_msg}")
    except Exception as e:
        print(f"[ErrorHandler] Logging failed with error: {e}")
        print(f"[Fallback] Message: {message_dict}")
        print(f"[Fallback] Reason : {error_msg}")
