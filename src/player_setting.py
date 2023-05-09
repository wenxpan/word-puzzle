import json
from player import Player


player = Player()


def setting():
    player.load_data()
    print(f'Welcome, {player.name}!')
    pass


if __name__ == '__main__':
    setting()
