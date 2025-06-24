# /core/realtime/websocket/server.py

import asyncio
import websockets
from .client_handler import handle_client  # Uses topic-aware handler

def run_server(host='0.0.0.0', port=8765):
    """
    Starts the WebSocket server using the custom client handler.
    """
    print(f"[WebSocket] Server running on ws://{host}:{port}")
    start_server = websockets.serve(handle_client, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
