from spotipi.os_services.service import OSService
from spotipi.os_services.event_listener import EventListener
from spotipi.events.player import player_consumer


PLAYER_EVENT_CONSUMER = ["player", player_consumer]

class PlayerService(OSService):
    def __init__(self):
        super().__init__("Player Service")
        self.event = PLAYER_EVENT_CONSUMER

    def run(self):
        listener = EventListener(self.manager, self.event[0], self.event[1])
        listener.run()


def main():
    service = PlayerService()
    service.run()


if __name__ == "__main__":
    main()
