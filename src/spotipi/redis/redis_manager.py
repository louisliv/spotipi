import os, json
import redis.asyncio as aioredis
import redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

class AsyncRedisPubSubManager:
    """
        Initializes the AsyncRedisPubSubManager.
    """

    def __init__(self):
        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        """
        Establishes a connection to Redis.

        Returns:
            aioredis.Redis: Redis connection object.
        """
        return aioredis.Redis(host=self.redis_host,
                              port=self.redis_port,
                              decode_responses=True,
                              auto_close_connection_pool=False)

    async def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub client.
        """
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def publish(self, room_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            room_id (str): Channel or room ID.
            message (str): Message to be published.
        """
        await self.redis_connection.publish(room_id, message)

    async def subscribe(self, room_id: str) -> aioredis.Redis:
        """
        Subscribes to a Redis channel.

        Args:
            room_id (str): Channel or room ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            room_id (str): Channel or room ID to unsubscribe from.
        """
        await self.pubsub.unsubscribe(room_id)


class RedisPubSubManager:
    """
        Initializes the RedisPubSubManager.
    """

    def __init__(self):
        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        self.pubsub = None

    async def _get_redis_connection(self) -> redis.Redis:
        """
        Establishes a connection to Redis.

        Returns:
            redis.Redis: Redis connection object.
        """
        return redis.Redis(host=self.redis_host,
                              port=self.redis_port,
                              decode_responses=True,
                              auto_close_connection_pool=False)

    def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub client.
        """
        self.redis_connection = redis.Redis(
            host=self.redis_host,
            port=self.redis_port
        )
        self.pubsub = self.redis_connection.pubsub()

    def publish(self, room_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            room_id (str): Channel or room ID.
            message (str): Message to be published.
        """
        self.redis_connection.publish(room_id, json.dumps(message))

    def subscribe(self, room_id: str) -> aioredis.Redis:
        """
        Subscribes to a Redis channel.

        Args:
            room_id (str): Channel or room ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        self.pubsub.subscribe(room_id)
        return self.pubsub

    def unsubscribe(self, room_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            room_id (str): Channel or room ID to unsubscribe from.
        """
        self.pubsub.unsubscribe(room_id)