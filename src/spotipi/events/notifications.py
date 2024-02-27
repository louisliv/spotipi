from spotipi.notification import NotificationSound


def notification_consumer(message: dict):
    message_to_play = message.get("message")

    if message_to_play:
        NotificationSound(message_to_play)
