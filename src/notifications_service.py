from spotipi.os_services.service import OSService
from spotipi.os_services.event_listener import EventListener
from spotipi.events.notifications import notification_consumer


NOTIFICATIONS_EVENT_CONSUMER = ["notifications", notification_consumer]

class NotificationsService(OSService):
    def __init__(self):
        super().__init__("Notifications Service")
        self.event = NOTIFICATIONS_EVENT_CONSUMER

    def run(self):
        listener = EventListener(self.manager, self.event[0], self.event[1])
        listener.run()


def main():
    service = NotificationsService()
    service.run()


if __name__ == "__main__":
    main()
