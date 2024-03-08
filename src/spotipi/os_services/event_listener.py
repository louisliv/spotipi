from typing import Callable
import json

from spotipi.pubsub.pubsub_manager import PubSubManager

class EventListener:

    def __init__(
        self, manager: PubSubManager, topic: str, consumer: Callable[[dict], None]
    ):
        self.manager = manager
        self.topic = topic
        self.consumer = consumer

    def run(self):
        pubsub = self.manager.subscribe(self.topic)

        for message in pubsub.listen():
            msg_dict = None

            try:
                msg_data = message.get("data")
                msg_dict = json.loads(msg_data)
            except:
                pass

            if isinstance(msg_dict, dict):
                self.consumer(msg_dict)
