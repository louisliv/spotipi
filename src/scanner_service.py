from spotipi.os_services.service import OSService
from spotipi.os_services.event_listener import EventListener
from spotipi.events.scanner import scanner_consumer


SCANNER_EVENT_CONSUMER = ["scanner", scanner_consumer]

class Scanner(OSService):
    def __init__(self):
        super().__init__("Scanner Service")
        self.event = SCANNER_EVENT_CONSUMER
        
    def run(self):
        listener = EventListener(self.redis, self.event[0], self.event[1])
        listener.run()


if __name__ == "__main__":
    service = Scanner()
    service.run()
