class InvalidDataException(Exception):
    def __init__(self, message: str = "Invalid data") -> None:
        self.message = message
        super().__init__(self.message)