# File: /core/realtime/websocket/manager.py

import logging

class WebSocketManager:
    def __init__(self):
        self.clients = set()

    async def register(self, ws):
        self.clients.add(ws)
        logging.info(f"[WebSocketManager] Client registered: {ws.remote_address}")

    async def unregister(self, ws):
        if ws in self.clients:
            self.clients.remove(ws)
            logging.info(f"[WebSocketManager] Client unregistered: {ws.remote_address}")

    async def broadcast(self, msg: str):
        dead_clients = set()
        for client in self.clients:
            try:
                await client.send(msg)
            except Exception as e:
                logging.warning(f"[WebSocketManager] Failed to send message: {e}")
                dead_clients.add(client)

        for client in dead_clients:
            await self.unregister(client)
