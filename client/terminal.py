def play_terminal():
    print "Are you ready? let's play."
    board = initialize()
    draw_board(board)

    while True:
        move_s = raw_input("Enter your move as a pair of numbers between 0 and 63.\n")
        move = [int(e) for e in move_s.split(',')]
        if move_legal(move, board):
            board = transition(move, board)
            draw_board(board)
        else:
            print "Please enter a valid move."
            
    
                     

if __name__ == "__main__":
    play_terminal()
