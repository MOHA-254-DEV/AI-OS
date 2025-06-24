from fastapi import APIRouter, WebSocket
from visualizer.agent_tracker import AgentTracker
from visualizer.behavior_cache import BehaviorCache

router = APIRouter()
tracker = AgentTracker()
cache = BehaviorCache()

@router.post("/track-agent")
async def track_agent(data: dict):
    agent_id = data.get("agent_id")
    task_type = data.get("task_type")
    plugin = data.get("plugin")
    outcome = data.get("outcome", "success")
    tracker.log_activity(agent_id, task_type, plugin, outcome)
    return {"status": "logged"}

@router.get("/logs")
async def get_logs():
    logs = tracker.get_all_logs()
    cache.update_from_log(logs)
    return {"logs": logs}

@router.get("/snapshot")
async def get_snapshot():
    return cache.get_snapshot()

@router.websocket("/ws/heatmap")
async def heatmap_socket(ws: WebSocket):
    await ws.accept()
    while True:
        logs = tracker.get_all_logs()
        cache.update_from_log(logs)
        await ws.send_json(cache.get_snapshot())
