
import random

from gameplay.checkers import move_legal

from client import play, connect


def play_checkers():
    sock = connect()
    return play(sock, get_move)


def get_move(state):
    board = state['board']
    while True:
        p1 = random.randint(0, 63)
        p2 = p1 + random.randint(-19, 19)
        move = (p1, p2)
        if move_legal(move, board):
            return move
        


if __name__ == "__main__":
    play_checkers()
