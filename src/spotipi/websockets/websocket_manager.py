from typing import Dict, List
import asyncio

from fastapi import WebSocket

from spotipi.pubsub.pubsub_manager import AsyncPubSubManager
from spotipi.redis.redis_manager import AsyncRedisPubSubManager


class WebSocketManager:

    def __init__(self):
        """
        Initializes the WebSocketManager.

        Attributes:
            rooms (dict): A dictionary to store WebSocket connections in different rooms.
            pubsub_client (AsyncPubSubManager): An instance of the AsyncPubSubManager class for pub-sub functionality.
        """
        self.rooms: Dict[str, List] = {}
        self.pubsub_client = AsyncPubSubManager()

    async def add_user_to_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Adds a user's WebSocket connection to a room.

        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        await websocket.accept()

        if room_id in self.rooms:
            self.rooms[room_id].append(websocket)
        else:
            self.rooms[room_id] = [websocket]

            await self.pubsub_client.connect()
            pubsub_subscriber = await self.pubsub_client.subscribe(room_id)
            asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        """
        Broadcasts a message to all connected WebSockets in a room.

        Args:
            room_id (str): Room ID or channel name.
            message (str): Message to be broadcasted.
        """
        await self.pubsub_client.publish(room_id, message)

    async def remove_user_from_room(self, room_id: str, websocket: WebSocket) -> None:
        """
        Removes a user's WebSocket connection from a room.

        Args:
            room_id (str): Room ID or channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        self.rooms[room_id].remove(websocket)

        if len(self.rooms[room_id]) == 0:
            del self.rooms[room_id]
            await self.pubsub_client.unsubscribe(room_id)

    async def _pubsub_data_reader(self, pubsub_subscriber):
        """
        Reads and broadcasts messages received from Redis PubSub.

        Args:
            pubsub_subscriber (aioredis.ChannelSubscribe): PubSub object for the subscribed channel.
        """
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                channel = message['channel']

                if channel is isinstance(channel, bytes):
                    channel = channel.decode('utf-8')

                data = message['data']

                if data is isinstance(data, bytes):
                    data = data.decode('utf-8')

                room_id = channel
                all_sockets = self.rooms[room_id]
                for socket in all_sockets:
                    await socket.send_text(data)
