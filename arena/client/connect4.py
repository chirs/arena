

import random

from arena.client.client import play, connect


def play_connect_four():
    sock = connect()
    return play(sock, get_move)


def get_move(state):
    board = state['board']
    choices = [i for i,e in enumerate(board[:7]) if e == ' ']

    try:
        return random.choice(choices)
    except:
        import pdb; pdb.set_trace()
    5



if __name__ == "__main__":
    play_connect_four()
