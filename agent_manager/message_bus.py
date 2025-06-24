# agent_manager/message_bus.py

import threading
import heapq
import logging

class Message:
    def __init__(self, content: str, priority: int = 1):
        """
        Message wrapper with priority support.
        Lower `priority` values are more urgent.

        :param content: Message content
        :param priority: Integer priority (lower is higher priority)
        """
        self.content = content
        self.priority = priority

    def __lt__(self, other):
        """Supports priority-based sorting (heapq)."""
        return self.priority < other.priority

class MessageBus:
    def __init__(self):
        """
        Thread-safe priority queue for message handling.
        """
        self.message_queue = []
        self.lock = threading.Lock()
        self.logger = logging.getLogger("MessageBus")

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def send(self, message: Message):
        """
        Send a message to the message bus.

        :param message: Instance of Message
        """
        if not isinstance(message, Message):
            raise TypeError("Only Message instances can be added to the message bus.")

        with self.lock:
            heapq.heappush(self.message_queue, message)
            self.logger.info(f"📨 Message queued: '{message.content}' with priority {message.priority}")

    def read_all(self):
        """
        Read all messages sorted by priority.

        :return: List of message contents sorted by priority.
        """
        with self.lock:
            sorted_messages = sorted(self.message_queue, key=lambda msg: msg.priority)
            self.logger.info(f"📖 Reading {len(sorted_messages)} messages from queue.")
            return [msg.content for msg in sorted_messages]

    def process_message(self):
        """
        Process and remove the highest-priority message.

        :return: Processed message content or None if empty.
        """
        with self.lock:
            if self.message_queue:
                message = heapq.heappop(self.message_queue)
                self.logger.info(f"✅ Processed message: '{message.content}' (Priority: {message.priority})")
                return message.content
            else:
                self.logger.warning("📭 No messages to process.")
                return None

    def clear_messages(self):
        """
        Clears all queued messages.
        """
        with self.lock:
            count = len(self.message_queue)
            self.message_queue.clear()
            self.logger.info(f"🧹 Cleared {count} messages from the message bus.")
