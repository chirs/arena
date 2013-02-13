
from mechanics import move_legal, transition, initialize, winner


def draw_board(board):
    s = ''
    for i in range(0,64,8):
        s += board[i:i+8]
        s += '\n'
    print(s)



def main():
    pass


def start_game():
    pass

def end_game():
    pass


def dispatch_move(move, board):
    if move_legal(move, board):
        return transition(move_board)
    else:
        return 'invalid'


