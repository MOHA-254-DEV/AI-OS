import asyncio
from core.task_scheduler import TaskScheduler
from core.voice_handler import VoiceHandler
from utils.logger import logger

class AIKernel:
    def __init__(self):
        self.scheduler = TaskScheduler()
        self.voice = VoiceHandler()
        self.booted = False
        self.shutdown_requested = False

    async def boot(self):
        try:
            logger.info("🚀 Booting AI OS Kernel...")
            await self.scheduler.initialize()
            await self.voice.initialize()
            self.booted = True
            logger.info("✅ Kernel booted successfully.")
            await self.run()
        except Exception as e:
            logger.error(f"❌ Kernel boot failed: {e}")
            self.booted = False

    async def run(self):
        logger.info("🔁 Kernel main loop started.")
        try:
            while not self.shutdown_requested:
                command = await self.voice.listen_for_command()
                if command:
                    logger.info(f"🎙️ Received voice/prompt command: {command}")
                    await self.scheduler.handle_command(command)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.warning("⛔ Kernel loop cancelled.")
        except Exception as e:
            logger.error(f"⚠️ Error in main loop: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("🛑 Shutting down Kernel components...")
        await self.scheduler.shutdown()
        await self.voice.shutdown()
        logger.info("💤 Kernel shutdown complete.")
