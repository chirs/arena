
# Should be moved to surpervisor.py
def draw_board(board):
    s = ''
    for i in range(0,64,8):
        s += board[i:i+8]
        s += '\n'
    print s



def get_opponent(p):
    if p in 'Rr':
        return 'b'
    elif p in 'Bb':
        return 'r'
    else:
        raise

def is_king(char):
    return not char.islower()


def initialize():
    """
    Initial board state.
    """

    rx = ' r r r rr r r r  r r r r'
    bx = 'b b b b  b b b bb b b b'

    return rx + ' ' * 16 + bx


def moves(position, direction):
    if position % 8 == 0:
        moves = [position + 9, position - 7]
    elif position % 8 == 7:
        moves = [position + 7, position - 9]
    else:
        moves = [position + 7, position + 9, position - 7, position - 9]

    moves = [e for e in moves if 0 <= e <= 63]

    if direction == 1:
        return [e for e in moves if e > position]
    elif direction == -1:
        return [e for e in moves if e < position]
    else:
        return moves
    


def capture_moves(position, direction):
    if position % 8 in (0,1):
        moves = [position + 18, position - 14]
    elif position % 8 in (6,7):
        moves = [position - 18, position + 14]
    else:
        moves = [position + 14, position + 18, position - 14, position - 18]

    moves = [e for e in moves if 0 <= e <= 63]

    if direction == 1:
        return [e for e in moves if e > position]
    elif direction == -1:
        return [e for e in moves if e < position]
    else:
        return moves



def valid_capture_moves(player, board, direction=None):
    """
    Capture moves that will actually result in a capture.
    """
    
    positions = [i for i, char in enumerate(board) if char == player]
    opponent = get_opponent(player)


    captures = []
    
    for position in positions:
        potential_captures = capture_moves(position, direction)
        if position == 280:
            import pdb; pdb.set_trace()

        for end_p in potential_captures:
            jumped_p = (position + end_p) / 2
            if board[end_p] == ' ' and board[jumped_p] == opponent:
                captures.append(end_p)
            
    return captures


def move_legal(move, board):
    start_position, end_position = move
    start_cell = board[start_position]
    end_cell = board[end_position]

    if start_cell == ' ':
        return False

    if end_cell != ' ':
        return False

    if start_cell == 'r':
        direction = 1
    else:
        direction = -1

    # Check for forced jumps.

    if end_position in legal_moves(start_position, direction):
        return True

    if end_position in capture_moves(start_position, direction):
        in_between_cell = (end_position + start_position) / 2
        between_cell = board[in_between_cell]
        if between_cell == opponent(start_cell):
            return True
        
    return False

def transition(move, board):
    start_p, end_p = move
    distance = abs(start_p - end_p)

    board_list = list(board)
    board_list[start_p], board_list[end_p] = board[end_p], board[start_p]    


    if distance > 9:
        in_between = (start_p + end_p) / 2
        board_list[in_between] = ' '

    return ''.join(board_list)
        
    return board


def winner(board):
    if 'r' not in board:
        return 'b'
    elif 'b' not in board:
        return 'r'
    else:
        return None


if __name__ == "__main__":
    #print initialize()
    board = initialize()
    draw_board(board)
    print valid_capture_moves('r', board)
    board2 = transition((21, 28), board)
    board3 = transition((46, 37), board2)
    print valid_capture_moves('r', board3)

    #board3 = transition((46, 53), board2)
    draw_board(board3)
    
