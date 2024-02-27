from typing import Callable
import json

from redis import Redis

class EventListener:
    def __init__(self, redis: Redis, topic: str, consumer: Callable[[dict], None]):
        self.redis = redis
        self.topic = topic
        self.consumer = consumer

    def run(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.topic)

        for message in pubsub.listen():
            msg_dict = None

            try:
                msg_data = message.get("data")
                msg_dict = json.loads(msg_data)
            except:
                pass
            
            if isinstance(msg_dict, dict):
                self.consumer(msg_dict)