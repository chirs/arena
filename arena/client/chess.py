
import random

from arena.client.client import play, connect
from arena.gameplay.chess import Chess



def play_chess()
    sock = connect()
    return play(sock, get_move)


def get_move(state):
    board = state['board']
    while True:
        game = Chess(board, state['player'])
        moves = game.all_legal_moves()
        return random.choice(moves)
        


if __name__ == "__main__":
    play_chess()
