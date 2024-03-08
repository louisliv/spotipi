import os
import typing as t
import abc


class PubSubManagerBase(abc.ABC):
    PUBSUB_PROVIDER_PRECEDENCE = 99
    PUBSUB_PROVIDER_KEY = "BASE"

    _provider_types: t.Dict[str, t.Type["PubSubManagerBase"]] = {}

    def __new__(cls):
        provider = os.getenv("PUBSUB_PROVIDER") or "AUTO"

        if provider == "AUTO":
            registered_types = sorted(
                (provider.PUBSUB_PROVIDER_PRECEDENCE, provider)
                for provider in cls._provider_types.values()
            )

            type_to_use = next((provider for _, provider in registered_types), None)

            if not type_to_use:
                raise ValueError("No PubSubManager available")
        else:
            type_to_use = cls._provider_types.get(provider)
            if not type_to_use is None:
                raise ValueError(f"Unknown PubSubManager: {provider}")

        instance = super().__new__(type_to_use)

        if type_to_use != cls:
            instance.__init__()

        return instance

    def __init_subclass__(cls, **kwargs):
        cls._provider_types[cls.PUBSUB_PROVIDER_KEY] = cls

    @abc.abstractmethod
    def publish(self, topic: str, message: str):
        pass

    @abc.abstractmethod
    def subscribe(self, topic: str):
        pass

    @abc.abstractmethod
    def unsubscribe(self, topic: str):
        pass


class AsyncPubSubManagerBase(abc.ABC):
    PUBSUB_MANGER_PRECEDENCE = 99
    PUBSUB_PROVIDER_KEY = "BASE"

    _provider_types: t.Dict[str, t.Type["AsyncPubSubManagerBase"]] = {}

    def __new__(cls):
        provider = os.getenv("PUBSUB_PROVIDER") or "AUTO"

        if provider == "AUTO":
            registered_types = sorted(
                (provider.PUBSUB_PROVIDER_PRECEDENCE, provider)
                for provider in cls._provider_types.values()
            )

            type_to_use = next((provider for _, provider in registered_types), None)

            if not type_to_use:
                raise ValueError("No PubSubManager available")
        else:
            type_to_use = cls._provider_types.get(provider)
            if not type_to_use is None:
                raise ValueError(f"Unknown PubSubManager: {provider}")

        instance = super().__new__(type_to_use)

        if type_to_use != cls:
            instance.__init__()

        return instance

    def __init_subclass__(cls, **kwargs):
        cls._provider_types[cls.PUBSUB_PROVIDER_KEY] = cls

    @abc.abstractmethod
    async def publish(self, topic: str, message: str):
        pass

    @abc.abstractmethod
    async def subscribe(self, topic: str):
        pass

    @abc.abstractmethod
    async def unsubscribe(self, topic: str):
        pass


class PubSubManager(PubSubManagerBase):
    """
    Initializes the PubSubManager.
    """

    PUBSUB_PROVIDER_PRECEDENCE = 98
    PUBSUB_PROVIDER_KEY = "PUBSUB"

    def __init__(self):
        self.pubsub = None

    def connect(self):
        """
        Connects to the PubSub server.
        """
        raise NotImplementedError

    def publish(self, topic: str, message: str):
        """
        Publishes a message to a specific channel or topic.

        Args:
            topic (str): Channel or topic to publish the message to.
            message (str): Message to be published.
        """
        raise NotImplementedError

    def subscribe(self, topic: str):
        """
        Subscribes to a channel or topic.

        Args:
            topic (str): Channel or topic to subscribe to.
        """
        raise NotImplementedError

    def unsubscribe(self, topic: str):
        """
        Unsubscribes from a channel or topic.

        Args:
            topic (str): Channel or topic to unsubscribe from.
        """
        raise NotImplementedError


class AsyncPubSubManager(AsyncPubSubManagerBase):
    """
    Initializes the AsyncPubSubManager.
    """

    PUBSUB_PROVIDER_PRECEDENCE = 98
    PUBSUB_PROVIDER_KEY = "PUBSUB"

    def __init__(self):
        self.pubsub = None

    def connect(self):
        """
        Connects to the PubSub server.
        """
        raise NotImplementedError

    async def publish(self, topic: str, message: str):
        """
        Publishes a message to a specific channel or topic.

        Args:
            topic (str): Channel or topic to publish the message to.
            message (str): Message to be published.
        """
        raise NotImplementedError

    async def subscribe(self, topic: str):
        """
        Subscribes to a channel or topic.

        Args:
            topic (str): Channel or topic to subscribe to.
        """
        raise NotImplementedError

    async def unsubscribe(self, topic: str):
        """
        Unsubscribes from a channel or topic.

        Args:
            topic (str): Channel or topic to unsubscribe from.
        """
        raise NotImplementedError
