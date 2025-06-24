from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.auth import verify_token
import logging

# Configure structured logging
logger = logging.getLogger("AI-OS-API")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize FastAPI app
app = FastAPI(title="Autonomous AI OS API", version="1.0")

# CORS configuration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global reference to kernel injected at runtime
kernel_ref = None


@app.get("/api/status", tags=["Health"])
async def get_status():
    """
    Simple health check endpoint.
    """
    logger.info("✅ Status check called.")
    return {"status": "AI OS is active"}


@app.post("/api/command", tags=["Commands"])
async def send_command(payload: dict):
    """
    Receive and execute a command via the AI Kernel.
    Requires valid authentication token.
    """
    token = payload.get("token")
    if not token or not verify_token(token):
        logger.warning("🔒 Unauthorized token access attempt.")
        raise HTTPException(status_code=403, detail="Unauthorized")

    command = payload.get("command")
    if not command:
        logger.error("⚠️ No command found in request.")
        raise HTTPException(status_code=400, detail="Command is required")

    logger.info(f"⚙️ Executing command: {command}")
    try:
        result = await kernel_ref.scheduler.handle_command(command)
        logger.info(f"✅ Command executed: {command}")
        return {"message": f"Command '{command}' executed successfully", "result": result}
    except Exception as e:
        logger.exception(f"❌ Failed to execute command '{command}'")
        raise HTTPException(status_code=500, detail=f"Error executing command: {str(e)}")


@app.get("/api/config", tags=["System"])
async def get_kernel_config():
    """
    Returns basic configuration or capabilities from the kernel.
    """
    try:
        if not kernel_ref:
            raise Exception("Kernel reference not initialized")
        config = kernel_ref.get_config()  # kernel must expose get_config()
        return {"config": config}
    except Exception as e:
        logger.error(f"⚠️ Failed to retrieve config: {e}")
        raise HTTPException(status_code=500, detail="Kernel configuration unavailable")


def start_api_server(kernel):
    """
    Bootstraps and starts the FastAPI service with the injected kernel reference.
    """
    global kernel_ref
    kernel_ref = kernel

    import uvicorn
    logger.info("🚀 Starting API server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=5000)