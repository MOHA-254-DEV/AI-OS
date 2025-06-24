from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
import os
from dashboard.backend.agent_monitor import AgentMonitor

app = FastAPI()
agent_monitor = AgentMonitor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = agent_monitor.get_all_agents()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/agents")
def get_agents():
    return agent_monitor.get_all_agents()

@app.post("/agents/{agent_id}/action")
async def agent_action(agent_id: str, request: Request):
    body = await request.json()
    action = body.get("action")
    # Placeholder control actions
    if action == "pause":
        return {"status": "paused", "agent": agent_id}
    elif action == "resume":
        return {"status": "resumed", "agent": agent_id}
    elif action == "scale":
        return {"status": "scaled", "agent": agent_id}
    return {"error": "Unknown action"}
# ... (import existing FastAPI/WS logic)
from task_engine.processor import TaskProcessor
from task_engine.job_model import Job
import uuid

processor = TaskProcessor()
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(processor.worker_loop())

@app.websocket("/ws/jobs")
async def websocket_jobs(websocket: WebSocket):
    await websocket.accept()
    await processor.register_ws(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        await processor.unregister_ws(websocket)

@app.get("/jobs")
async def all_jobs():
    return await processor.get_all_jobs()

@app.post("/jobs")
async def create_job(request: Request):
    body = await request.json()
    job = Job(task_type=body.get("type", "generic"), payload=body.get("payload", {}), priority=body.get("priority", 5))
    await processor.submit_job(job)
    return {"id": job.id, "status": "submitted"}
from plugins.evaluator.monitor import PluginMonitor
plugin_monitor = PluginMonitor()

@app.post("/plugin/track")
async def track_plugin_exec(data: dict):
    plugin_id = data.get("plugin_id")
    success = data.get("success", True)
    plugin_monitor.record_execution(plugin_id, success)
    return {"status": "updated"}

@app.get("/plugin/scorecard")
async def get_scores():
    return plugin_monitor.get_scores()

@app.get("/plugin/blacklist")
async def get_blacklist():
    return plugin_monitor.get_blacklisted()
# dashboard/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import goals

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.include_router(goals.router, prefix="/api")
