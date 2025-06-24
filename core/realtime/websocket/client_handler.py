# File: /core/realtime/websocket/client_handler.py

import asyncio
import json
from core.realtime.pubsub.subscriber import publish_event
from core.realtime.pubsub.topics import Topics
from core.realtime.websocket.manager import WebSocketManager

ws_manager = WebSocketManager()

async def handle_client(ws, path):
    """
    Handles lifecycle of a single WebSocket client connection.
    - Registers client.
    - Listens for messages.
    - Publishes to internal event system.
    - Unregisters on disconnect.
    """
    await ws_manager.register(ws)
    try:
        async for msg in ws:
            try:
                data = json.loads(msg)
                topic = data.get("topic", Topics.TASK_UPDATE)
                payload = data.get("payload", {})

                # Forward the message into the PubSub system
                publish_event(topic, payload)

                # Optional: Echo back confirmation
                await ws.send(json.dumps({
                    "status": "received",
                    "topic": topic,
                    "payload": payload
                }))

            except json.JSONDecodeError:
                await ws.send(json.dumps({
                    "status": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                await ws.send(json.dumps({
                    "status": "error",
                    "message": f"Handler exception: {str(e)}"
                }))

    finally:
        await ws_manager.unregister(ws)
