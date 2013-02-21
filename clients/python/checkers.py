
import sys
import random

from client import play, connect

def play_checkers(host, port):
    sock = connect(host, port, 'checkers')
    return play(sock, get_move)

def get_move(state):

    board = state['board']
    player = 'r' if state['player'] == 1 else 'w'
    direction = 1 if player == 'r' else -1

    positions = [i for i,char in enumerate(board) if char.lower() == player]
    random.shuffle(positions)
    
    for position in positions:
        if direction == 1:
            if position % 8 != 0 and board[position + 7] == ' ':
                return (position, position + 7)
            elif position % 8 != 7 and board[position + 9] == ' ':
                return (position, position + 9)
        else:
            if position % 8 != 7 and board[position - 7] == ' ':
                return (position, position - 7)
            elif position % 8 != 0 and board[position - 9] == ' ':
                return (position, position - 9)

    # Couldnt find one dumb move, return anything
    return  (1,8)

if __name__ == "__main__":
    [_, host, port] = sys.argv
    play_checkers(host, int(port))

