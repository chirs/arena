
from arena.client.client import play, connect


def play_tictactoe():
    sock = connect()
    return play(sock, get_move)


def get_move(state):
    board = state['board']
    for i, e in enumerate(board):
        if e == ' ':
            return i

if __name__ == "__main__":
    play_tictactoe()
