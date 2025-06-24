# File: /core/realtime/pubsub/broker.py

from collections import defaultdict
from typing import Callable, Any
import traceback
from core.logging.plugin_logger import PluginLogger

class PubSubBroker:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.logger = PluginLogger()

    def publish(self, topic: str, data: Any) -> None:
        callbacks = self.subscribers.get(topic, [])
        if not callbacks:
            self.logger.log("PubSubBroker", input_code=f"publish:{topic}", output="No subscribers", success=False)
            return

        for callback in callbacks:
            try:
                callback(data)
                self.logger.log("PubSubBroker", input_code=f"publish:{topic}", output="Callback executed", success=True)
            except Exception as e:
                self.logger.log("PubSubBroker", input_code=f"publish:{topic}", output="Callback failed", success=False, error=traceback.format_exc())

    def subscribe(self, topic: str, callback: Callable) -> None:
        if callback not in self.subscribers[topic]:
            self.subscribers[topic].append(callback)
            self.logger.log("PubSubBroker", input_code=f"subscribe:{topic}", output="Subscriber added", success=True)

    def unsubscribe(self, topic: str, callback: Callable) -> None:
        if callback in self.subscribers[topic]:
            self.subscribers[topic].remove(callback)
            self.logger.log("PubSubBroker", input_code=f"unsubscribe:{topic}", output="Subscriber removed", success=True)
