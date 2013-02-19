


from gameplay.game import Game


class Checkers(Game):

    player_mapping = {
        1: 'b',
        2: 'r',
        }

    
    def __init__(self, board=None, current_player=1):
        self.board = board or self.initial_board()
        self.current_player = current_player
        self.moves_without_capture = 0


    @staticmethod
    def initial_board():
        """
        Initial board state.
        
        >>> initialize()[23]
        'r'
        >>> initialize()[28]
        ' '
        >>> initialize()[62]
        'b'
        """
        rx = ' r r r rr r r r  r r r r'
        bx = 'b b b b  b b b bb b b b '
        return rx + ' ' * 16 + bx

    def draw_board(self):
        s = ''
        for i in range(0,64,8):
            s += self.board[i:i+8]
            s += '\n'
        s += '=' * 8
        print(s)


    def is_king(self, char):
        """
        >>> is_king('r')
        False
        >>> is_king('B')
        True
        """
        return not char.islower()

    def get_direction(self, piece):
        """
        >>> get_direction('R')
        
        >>> get_direction('r')
        1
        >>> get_direction('b')
        -1
        """

        if self.is_king(piece):
            return None
        elif piece == 'r':
            return 1
        elif piece == 'b':
            return -1

    def get_opponent(self, p):
        """
        Returns char symbol for opponent.
        
        >>> get_opponent('R')
        'b'
        >>> get_opponent('b')
        'r'
        >>> get_opponent('ew')
        """
    
        if p in 'Rr':
            return 'b'
        elif p in 'Bb':
            return 'r'
        else:
            return None


    def is_tie(self):
        return self.moves_without_capture > 50

    def winner(self):
        """
        >>> winner(64 * 'b')
        'b'
        >>> winner('r' + 64 * ' ')
        'r'
        """
        bl = self.board.lower()

        if 'r' not in bl:
            return 1
        elif 'b' not in bl:
            return 2
        else:
            return 0


    def result(self):
        if self.is_tie():
            return -1
        else:
            return self.winner()



    def transition(self, move, player):
        """
        >>> board = 'r' + 63 * ' '
        >>> transition((0, 9), board)[0]
        ' '
        >>> transition((0, 9), board)[9]
        'r'
        """

        start_p, end_p = move

        distance = abs(start_p - end_p)

        if distance > 9:
            self.moves_without_capture = 0
        else:
            self.moves_without_capture += 1

        board_list = list(self.board)
        board_list[start_p], board_list[end_p] = self.board[end_p], self.board[start_p]    


        if distance > 9:
            jumped_p = int((start_p + end_p) / 2)
            board_list[jumped_p] = ' '

        for position in range(0, 8):
            if board_list[position] == 'b':
                board_list[position] = 'B'

        for position in range(56, 64):
            if board_list[position] == 'r':
                board_list[position] = 'R'

        self.current_player = 3 - self.current_player # Toggle between 1 and 2.
        self.board = ''.join(board_list)


    def move_legal(self, move):
        """
        Verify that a move is legal.
        
        >>> board = 24 * ' ' + 'r ' * 4 + ' b' * 2 + 28 * ' '    
        >>> move_legal((33, 24), board) # Move onto opponent.
        False
        >>> move_legal((0, 9), board) # Move empty cell.
        False
        >>> move_legal((30, 39), board) # Non-capture when capture is forced.
        False
        >>> move_legal((28, 37), board) # Non-capture when capture is forced.
        False
        >>> move_legal((33, 19), board) # Test valid capture.
        True
        
        # Add additional tests for the case where captures are not forced.
        """

        start_position, end_position = move

        if start_position > 63 or end_position > 63:
            return False

        if start_position < 0 or end_position < 0:
            return False

        start_cell = self.board[start_position]
        end_cell = self.board[end_position]

        if  start_cell.lower() != self.player_mapping[self.current_player]:
            return False

        if end_cell != ' ':
            return False

        player = start_cell.lower()
        direction = self.get_direction(start_cell)

        # Check for forced jumps.
        valid_captures = self.valid_capture_moves(player, direction)
        if valid_captures:
            return tuple(move) in valid_captures
        else:
            return end_position in self.moves(start_position, direction)




    def valid_capture_moves(self, player, direction=None):
        """
        Capture moves that will actually result in a capture.
        
        >>> valid_capture_moves('r', 'r' + 8*' ' + 'b' + 54 * ' ', 1)
        [(0, 18)]
        >>> valid_capture_moves('r', 'r' + 8*' ' + 'b' + 54 * ' ', -1)
        []
        >>> valid_capture_moves('b', 'r' + 8*' ' + 'b' + 54 * ' ', -1)
        []
        """

        opponent = self.get_opponent(player)    
        positions = [i for i, char in enumerate(self.board) if char.lower() == player]
        captures = []
    
        for position in positions:
            potential_captures = self.capture_moves(position, direction)
            for end_p in potential_captures:
                jumped_p = int((position + end_p) / 2) # jumped_p should always be an integer
                if self.board[end_p] == ' ' and self.board[jumped_p].lower() == opponent:
                    t = (position, end_p)
                    captures.append(t)
            
        return captures


    def moves(self, position, direction):
        """
        All potential non-capture moves (1 diagonal square away); no collision detection

        >>> sorted(moves(28, None))
        [19, 21, 35, 37]
        >>> sorted(moves(31, None))
        [22, 38]
        >>> sorted(moves(63, 1))
        []
        >>> sorted(moves(63, -1))
        [54]
        """

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
    

    def capture_moves(self, position, direction):
        """
        All potential capture moves (i.e. moves two diagonal squares away; no collision detection
        
        >>> sorted(capture_moves(28, None))
        [10, 14, 42, 46]
        >>> sorted(capture_moves(31, None))
        [13, 45]
        >>> sorted(capture_moves(63, 1))
        []
        >>> sorted(capture_moves(63, -1))
        [45]
        """

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



"""
if __name__ == "__main__":
    import doctest
    doctest.testmod()
"""
