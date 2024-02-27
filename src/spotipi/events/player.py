import os

if os.getenv('ENV') == 'development':
    from spotipi.player import FakePlayer as Player
else:
    from spotipi.player import SpotifyPlayer as Player


def player_consumer(message: dict):
    player = Player()
    
    player.handle_message(message)
