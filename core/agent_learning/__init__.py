# /core/agent_learning/__init__.py

import logging

# Setup logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: Attach a default handler if none is set (for standalone scripts)
if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("Initializing Agent Learning Module...")

# Import version metadata
try:
    from ._version import __version__
    logger.info(f"Agent Learning Module version: {__version__}")
except ImportError:
    __version__ = "0.0.1-dev"
    logger.warning("No version file found. Using fallback version.")

# Import components
__all__ = []
failed_imports = []

try:
    from .feedback_collector import feedback_collector
    __all__.append("feedback_collector")
except ImportError as e:
    logger.error(f"Failed to import 'feedback_collector': {e}")
    failed_imports.append("feedback_collector")

try:
    from .skill_adaptive_engine import skill_adaptive_engine
    __all__.append("skill_adaptive_engine")
except ImportError as e:
    logger.error(f"Failed to import 'skill_adaptive_engine': {e}")
    failed_imports.append("skill_adaptive_engine")

try:
    from .models.feedback_model import feedback_db
    __all__.append("feedback_db")
except ImportError as e:
    logger.error(f"Failed to import 'feedback_db': {e}")
    failed_imports.append("feedback_db")

# Always expose __version__
__all__.append("__version__")

# Final status log
if failed_imports:
    logger.warning(f"Agent Learning Module initialized with missing components: {failed_imports}")
else:
    logger.info("Agent Learning Module initialized successfully with all components.")
