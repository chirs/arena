
from server import start, get_move, send_state
from gameplay.checkers import move_legal, transition, initialize, winner, draw_board

HOST = '127.0.0.1'
PORT = 1060


def build_state(player, winner, board):

    return {
        'player': player,
        'winner': winner,
        'board': board
        }

def main():
    player1, player2 = start(HOST, PORT)
    board = initialize()
    player1_turn = True
    game_over = False
    winner_ = None

    while not game_over:

        if player1_turn:
            p = player1
            ps = 'b'
        else:
            p = player2
            ps = 'r'

        state = build_state(ps, winner_, board)
        send_state(p, state)
        move = get_move(p)

        if move_legal(move, board):
            draw_board(board)
            player1_turn = not(player1_turn)
            board = transition(move, board)

            winner_ = winner(board)
            if winner_:
                draw_board(board)
                game_over = True
                print("Game over!")
                send_state(player1, build_state('b', winner_, board))
                send_state(player2, build_state('r', winner_, board))

if __name__ == "__main__":
    main()
