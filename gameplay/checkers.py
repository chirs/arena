
from gameplay.game import Game

class Checkers(Game):

    player_mapping = {
        1: 'r',
        2: 'w',
        }

    def __init__(self, board=None, current_player=1):
        self.board = board or self.initial_board()
        self.current_player = current_player
        self.moves_without_capture = 0

    @staticmethod
    def initial_board():
        """
        Initial board state.
        """
        rx = ' r r r rr r r r  r r r r'
        wx = 'w w w w  w w w ww w w w '
        return rx + ' ' * 16 + wx

    def draw_board(self):
        s = ''
        for i in range(0,64,8):
            s += self.board[i:i+8]
            s += '\n'
        s += '=' * 8
        return s

    def is_king(self, char):
        return not char.islower()

    def get_direction(self, piece):

        if self.is_king(piece):
            return None
        elif piece == 'r':
            return 1
        elif piece == 'w':
            return -1

    def get_opponent(self, p):
        """
        Returns char symbol for opponent.
        """
        if p in 'Rr':
            return 'w'
        elif p in 'Ww':
            return 'r'
        else:
            return None

    def result(self):

        bl = self.board.lower()

        if 'w' not in bl:
            return 1
        elif 'r' not in bl:
            return 2
        elif self.moves_without_capture >50:
            return -1
        elif not self.moves(self.player_mapping[self.current_player]):
            # Player is stuck; no more moves, lose
            return 3 - self.current_player
        else:
            return 0

    def apply_move(self, board, move):
        """
        Takes the string representation of the board
        and apply the move to it. Return the resulting
        board. move can be a multiple capture.
        """
        start_pos, *visited_squares = move

        for end_pos in visited_squares:

            distance = abs(end_pos - start_pos)

            board_list = list(board)
            board_list[start_pos], board_list[end_pos] = board[end_pos], board[start_pos]    

            if distance > 9:
                # Keep track of no-capture counter for tie games
                self.moves_without_capture = 0
                jumped_pos = (start_pos + end_pos) // 2
                board_list[jumped_pos] = ' '
            else:
                self.moves_without_capture += 1

            # Make pawn that reached the other end of the board kings
            for position in range(0, 8):
                if board_list[position] == 'w':
                    board_list[position] = 'W'

            for position in range(56, 64):
                if board_list[position] == 'r':
                    board_list[position] = 'R'

            board = ''.join(board_list)
            start_pos = end_pos

        return board
       
    def transition(self, move, _): # No need to use the third argument (player) for checkers

        self.board = self.apply_move(self.board, move)
        self.current_player = 3 - self.current_player # Toggle between 1 and 2.

    def move_legal(self, move):
        """
        Verify that a move is legal.
        """

        # Make sure move is a list of ints
        if not isinstance(move, list) or not all([isinstance(i, int) for i in move]):
            return False

        # Check for out-of-bounds moves
        if any([pos<0 or pos>63 for pos in move]):
            return False

        start_position, *visited_squares = move

        player = self.player_mapping[self.current_player]

        # Check if starting position is correct player
        if self.board[start_position].lower() != player:
            return False

        # Check for forced jumps.
        valid_captures = self.captures(player)
        if valid_captures:
            return move in valid_captures
        else:
            return move in self.moves_(start_position)

    def captures(self, player):
        """
        Returns all potential capture moves
        """
        positions = [i for i, char in enumerate(self.board) if char.lower() == player]
        captures = []
        for position in positions:
            paths = self.captures_([position], self.board)
            [captures.append(capture) for capture in paths if len(capture)>1]

        return captures
            
    def captures_(self, path, board): 
        """
        Returns all potential capture moves for a given start position and board
        """
        start_pos = path[-1]
        player = board[start_pos]
        opponent = self.get_opponent(player)
        direction = self.get_direction(player)

        # Handle left and right borders
        if start_pos % 8 in [0,1]:
            end_positions = [start_pos + 18, start_pos - 14]
        elif start_pos % 8 in [6,7]:
            end_positions = [start_pos + 14, start_pos - 18]
        else:
            end_positions = [start_pos + 18, start_pos + 14, start_pos - 14, start_pos - 18]

        # Handle bottom and top borders
        end_positions = [pos for pos in end_positions if 0 <= pos <= 63]

        # Make sure there is a captured pawn
        end_positions = [pos for pos in end_positions if board[(start_pos+pos)//2].lower() == opponent]
        
        # Make sure the end position is an empty sqare
        end_positions = [pos for pos in end_positions if board[pos].lower() == ' ']
        
        # Handle direction of play
        if direction == 1:
            end_positions = [pos for pos in end_positions if pos > start_pos]
        elif direction == -1:
            end_positions = [pos for pos in end_positions if pos < start_pos]

        paths = []
        for end_pos in end_positions:
            new_path = path + [end_pos]
            return self.captures_(new_path, self.apply_move(self.board, new_path))
        else:
            return [path]

    def moves(self, player):
        """
        All potential non-capture moves (1 diagonal square away)
        """
        positions = [i for i, char in enumerate(self.board) if char.lower() == player]
        moves = []
        for pos in positions:
            moves += self.moves_(pos)
        return moves

    def moves_(self, start_position):
        """
        All potential non-capture moves (1 diagonal square away)
        for a given start position
        """
        player = self.board[start_position]
        direction = self.get_direction(player)

        # Handle left and right borders
        if start_position % 8 == 0:
            end_positions = [start_position + 9, start_position - 7]
        elif start_position % 8 == 7:
            end_positions = [start_position + 7, start_position - 9]
        else:
            end_positions = [start_position + 7, start_position + 9, start_position - 7, start_position - 9]

        # Handle bottom and top borders
        end_positions = [pos for pos in end_positions if 0 <= pos <= 63]

        # Make sure end position is free
        end_positions = [pos for pos in end_positions if self.board[pos] == ' ']

        # Handle direction of play
        if direction == 1:
            end_positions = [pos for pos in end_positions if pos > start_position]
        elif direction == -1:
            end_positions = [pos for pos in end_positions if pos < start_position]
    
        return [[start_position, p] for p in end_positions]

