#!/usr/bin/env python3
"""
AI Operating System - Main Entry Point
Multi-platform compatible autonomous AI system
"""

import os
import sys
import logging
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

try:
    from core.kernel import AIKernel
    from core.task_scheduler import TaskScheduler
    from utils.logger import setup_logger
    from utils.config import load_config
    from api.server import create_app  # <-- Import your Flask app factory here
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    sys.exit(1)

logger = setup_logger(__name__)

class AIOperatingSystem:
    def __init__(self):
        self.kernel = None
        self.scheduler = None
        self.web_app = None
        self.running = False
        
    def setup_signal_handlers(self):
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            self.shutdown()
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
    def initialize(self):
        try:
            logger.info("🚀 Initializing AI Operating System...")
            config = load_config()
            self.kernel = AIKernel()
            self.scheduler = TaskScheduler()
            self.web_app = create_app()  # <-- Get your Flask app with blueprints and frontend registered
            self.setup_signal_handlers()
            logger.info("✅ AI Operating System initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize system: {e}")
            return False
    
    def start(self):
        if not self.initialize():
            return False
            
        try:
            logger.info("🎯 Starting AI Operating System...")
            self.running = True
            port = int(os.getenv('PORT', 5000))
            host = "0.0.0.0"
            logger.info(f"🌐 Starting web interface on {host}:{port}")
            self.web_app.run(
                host=host,
                port=port,
                debug=os.getenv('DEBUG', 'false').lower() == 'true',
                threaded=True
            )
        except Exception as e:
            logger.error(f"❌ Error starting system: {e}")
            self.shutdown()
            return False
            
    def shutdown(self):
        if self.running:
            logger.info("🛑 Shutting down AI Operating System...")
            self.running = False
            logger.info("✅ AI Operating System shutdown complete")

def main():
    try:
        ai_os = AIOperatingSystem()
        success = ai_os.start()
        return 0 if success else 1
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
