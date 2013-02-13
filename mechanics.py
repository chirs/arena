



def initialize():
    """
    Initial board state.
    """

    rx = ' r r r rr r r r  r r r r'
    bx = 'b b b b  b b b bb b b b'

    return rx + ' ' * 16 + bx

def draw_board(board):
    s = ''
    for i in range(0,64,8):
        s += board[i:i+8]
        s += '\n'
    print s
        

def is_queen(char):
    return not char.islower()

def legal_moves(position, direction):

    if direction == 1:
        if position % 8 == 0:
            return [position + 9]
        elif position % 8 == 7:
            return [position + 7]
        else:
            return [position + 7, position + 9]
        
    elif direction == -1:
        if position % 8 == 0:
            return [position - 7]
        elif position % 8 == 7:
            return [position - 9]
        else:
            return [position - 7, position - 9]


def king_moves(position):
    if position % 8 == 0:
        moves = [position + 9, position - 7]
    elif position % 8 == 7:
        moves = [position + 7, position - 9]
    else:
        moves = [position + 7, position + 9, position - 7, position - 9]

    return [e for e in moves if 0 <= e <= 63]


def king_jump_moves(position):
    if position % 8 in (0,1):
        moves = [position + 18, position - 14]
    elif position % 8 in (6,7):
        moves = [position - 18, position + 14]
    else:
        moves = [position + 14, position + 18, position - 14, position - 18]

    return [e for e in moves if 0 <= e <= 63]


def jump_moves(position, direction):

    if direction == 1:
        if position % 8 in (0, 1):
            return [position + 18]

        elif position % 8 in (6, 7):
            return [position + 14]

        else:
          return [position + 14, position + 18]

    elif direction == -1:
        if position % 8 in (0, 1):
            return [position - 14]

        elif position % 8 in (6, 7):
            return [position - 18]

        else:
          return [position - 14, position - 18]



def opponent(p):
    if p == 'r':
        return 'b'
    elif p == 'b':
        return 'r'
    else:
        raise


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

    if end_position in jump_moves(start_position, direction):
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
        in_between = (start_position + end_position) / 2
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
    board2 = transition((1, 9), board)
    draw_board(board2)
    
