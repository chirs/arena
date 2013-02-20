
import sys
import random

from gameplay.checkers import Checkers
from client import play, connect

def play_checkers(host, port):
    sock = connect(host, port, 'checkers')
    return play(sock, get_move)

def get_move(state):
    board = state['board']
    while True:
        p1 = random.randint(0, 63)
        p2 = p1 + random.choice([-18, -14, -9, -7, 7, 9, 14, 18])
        move = (p1, p2)
        game = Checkers(board, state['player'])
        if game.move_legal(move):
            return move

if __name__ == "__main__":
    [_, host, port] = sys.argv
    play_checkers(host, int(port))

