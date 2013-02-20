
import sys

from client import play, connect

def play_tictactoe(host, port):
    sock = connect(host, port, 'tictactoe')
    return play(sock, get_move)

def get_move(state):
    board = state['board']
    for i, e in enumerate(board):
        if e == ' ':
            return i

if __name__ == "__main__":
    [_, host, port] = sys.argv
    play_tictactoe(host, int(port))

