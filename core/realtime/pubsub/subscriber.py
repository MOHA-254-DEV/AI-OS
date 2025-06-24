# File: /core/realtime/pubsub/subscriber.py

from .broker import PubSubBroker
import logging

broker = PubSubBroker()

def subscribe_to_topic(topic: str, callback):
    if not callable(callback):
        raise ValueError("Callback must be a callable function or method")
    broker.subscribe(topic, callback)
    logging.debug(f"Subscribed to topic '{topic}' with handler {callback.__name__}")

def unsubscribe_from_topic(topic: str, callback):
    try:
        broker.unsubscribe(topic, callback)
        logging.debug(f"Unsubscribed from topic '{topic}' for handler {callback.__name__}")
    except ValueError:
        logging.warning(f"Attempted to unsubscribe non-existent handler from topic '{topic}'")

def publish_event(topic: str, data: dict):
    logging.debug(f"Publishing to topic '{topic}' with data: {data}")
    broker.publish(topic, data)
