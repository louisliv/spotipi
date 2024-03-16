import argparse
import subprocess

PLAYER_ACTIONS = {
    "play": "playing",
    "pause": "paused",
}


def main():
    parser = argparse.ArgumentParser(description="Play a song")

    parser.add_argument(
        "--hostname",
        type=str,
        required=False,
        default="spotipi.local",
        help="The pi hostname",
    )
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
    hostname = args.hostname

    # Send command to remote pi
    print(f"Sending {action_input} to {hostname}")

    spotipi_cmd = f"spotipi-player-cmd --action {action_input}"

    if rfid_number:
        spotipi_cmd += f" --rfid_number {rfid_number}"

    cmd_list = ["ssh", f"pi@{hostname}", spotipi_cmd]

    executed_cmd = subprocess.run(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True
    )

    print(executed_cmd.stdout)


if __name__ == "__main__":
    main()
