
from server import start, get_move, send_board 
from mechanics import move_legal, transition, initialize, winner

HOST = '127.0.0.1'
PORT = 1060

def draw_board(board):
    s = ''
    for i in range(0,64,8):
        s += board[i:i+8]
        s += '\n'
    print(s)

def main():
    player1, player2 = start(HOST, PORT)
    board = initialize()
    player1s_turn = True
    game_over = False

    while not game_over:
        if player1s_turn:
            send_board(player1, board)
            move = get_move(player1)
        else
            send_board(player2, board)
            move = get_move(player2)

        if move_legal(move):
            board = transition(move, board)
            winner_ = winner(board)
            if winner_:
                game_over = True

