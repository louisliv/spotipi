import uuid, socket, os, json, logging

FAKE_SOCKET_PATH = "/tmp/fake_mfrc"
FAKE_PORT = 12345
FAKE_HOST = "0.0.0.0"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FakeSimpleMFRC:
    def __init__(self):
        self.path = FAKE_SOCKET_PATH
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if os.path.exists(self.path):
            os.unlink(self.path)
        self.socket.bind((FAKE_HOST, FAKE_PORT))

    def read(self):
        logger.info("Fake MFRC is listening")
        self.socket.listen(1)
        self.connection, self.client_address = self.socket.accept()
        data = self.connection.recv(1024)

        if not data:
            return None, None

        data = str(data.decode("utf-8"))

        response = {"message": "accepted"}
        response_string = json.dumps(response)
        self.connection.sendall(response_string.encode())
        self.connection.close()

        return data, "fake_mfrc"

    def close(self):
        self.socket.close()


def send_fake_rfid():
    fake_rfid = str(uuid.uuid4())

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((FAKE_HOST, FAKE_PORT))
    client_socket.sendall(fake_rfid.encode('utf-8'))

    client_socket.recv(1024)
    print(f"Fake RFID sent to port {FAKE_PORT}: {fake_rfid}")
    client_socket.close()


if __name__ == "__main__":
    send_fake_rfid()
