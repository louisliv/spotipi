import argparse

from spotipi.player import PlayerResponses
from spotipi.redis.redis_manager import RedisPubSubManager


PLAYER_ACTIONS = {
    "play": PlayerResponses.playing.value,
    "pause": PlayerResponses.paused.value,
}


def main():
    parser = argparse.ArgumentParser(description="Play a song")
    parser.add_argument(
        "--action",
        type=str,
        choices=list(PLAYER_ACTIONS.keys()),
        required=True,
        help="The action to perform",
    )

    parser.add_argument(
        "--rfid_number", type=str, help="The RFID number to play", required=False
    )

    args = parser.parse_args()

    action_input = args.action
    rfid_number = args.rfid_number

    if action_input not in PLAYER_ACTIONS:
        parser.error("The action specified is not valid")

    pubsub = RedisPubSubManager()
    pubsub.connect()

    message = {"type": PLAYER_ACTIONS.get(action_input)}

    if rfid_number:
        message["rfid_number"] = rfid_number

    pubsub.publish("player", message)


if __name__ == "__main__":
    main()
