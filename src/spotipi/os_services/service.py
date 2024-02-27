import os
import logging
from abc import abstractmethod

from spotipi.redis.redis_manager import RedisPubSubManager

logging.basicConfig(level=logging.INFO)


class OSService:
    def __init__(self, name: str):
        logging.info(f"Starting event listener for {name}")
        self.name = name
        self.manager = RedisPubSubManager()
        self.manager.connect()
        self.redis = self.manager.redis_connection

    @abstractmethod
    def run(self):
        pass
