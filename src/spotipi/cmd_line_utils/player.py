import argparse

from spotipi.player import PlayerResponses
from spotipi.redis.redis_manager import RedisPubSubManager


def main():
    parser = argparse.ArgumentParser(description="Play a song")
    parser.add_argument(
        "--action",
        type=PlayerResponses,
        choices=list(PlayerResponses),
        required=True,
        help="The action to perform",
    )

    parser.add_argument("--rfid_number", type=str, help="The RFID number to play")

    args = parser.parse_args()

    if args.action == PlayerResponses.playing and not args.rfid_number:
        parser.error("The 'playing' action requires an RFID number")

    action = args.action
    rfid_number = args.rfid_number

    pubsub = RedisPubSubManager()
    pubsub.connect()

    message = {"type": action}

    if rfid_number:
        message["rfid_number"] = rfid_number

    pubsub.publish("player", message)


if __name__ == "__main__":
    main()
