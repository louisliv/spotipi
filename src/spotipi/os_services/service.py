import os
import logging
from abc import abstractmethod

from spotipi.pubsub.pubsub_manager import PubSubManager
from spotipi.redis.redis_manager import RedisPubSubManager, AsyncRedisPubSubManager

logging.basicConfig(level=logging.INFO)


class OSService:
    def __init__(self, name: str):
        logging.info(f"Starting event listener for {name}")
        self.name = name
        self.manager = PubSubManager()
        self.manager.connect()

    @abstractmethod
    def run(self):
        pass
