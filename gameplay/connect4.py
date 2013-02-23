
from gameplay.game import Game


def index2coords(num):
    return (num//7, num % 7)

def coords2index(coords):
    return 7*coords[0] + coords[1]

def is_valid(coords):
    return 0 <= coords[0] < 6 and 0 <= coords[1] < 7

class ConnectFour(Game):
    """
    An abstract Game object.
    """

    player_mapping = {1: 'b', 2: 'r'}
    color_mapping = {v: k for k, v in player_mapping.items()}
    cached_solutions = None

    def __init__(self, board=' '*42, current_player=1):
        self.board = board
        self.current_player = current_player

    def draw_board(self):
        s = '\n'.join([self.board[i:i+7] for i in range(0, 42, 7)] + ['='*7])
        print(s)

    def move_is_legal(self, column):
        """Check that the top field for the column is open."""
        return self.board[column] == ' '

    def transition(self, column, player):
        assert player == self.current_player
        coords = [(row, column) for row in reversed(range(6))]
        indexes = [coords2index(row_coord) for row_coord in coords]
        for i in indexes:
            if self.board[i] == ' ':
                self.board = self.board[:i] + self.player_mapping[player] + self.board[i:]
                self.current_player = 3 - player
                return
        raise ValueError('column %d is full' % column)

    def is_tie(self):
        return not [e for e in self.board if e == ' ']

    @classmethod
    def get_solutions(cls):
        if cls.cached_solutions is not None:
            return cls.cached_solutions
        seq = lambda start, end: range(start, end+1)
        rows = 6
        columns = 7
        run = 4
        horizontal_solutions = [[(start_r, c) for c in range(start_c, start_c+run)]
                                   for start_r in range(rows)
                                   for start_c in seq(0, columns-run)]
        vertical_solutions = [[(r, start_c) for r in range(start_r, start_r+run)]
                                   for start_r in seq(0, rows-run)
                                   for start_c in range(columns)]
        diagonal_solutions_down_right = [[(r, c) for r,c in zip(range(start_r, start_r+run), range(start_c, start_c+run))]
                                   for start_r in seq(0, rows-run)
                                   for start_c in seq(0, columns-run)]
        diagonal_solutions_down_left = [[(r, c) for r,c in zip(range(start_r, start_r+run), reversed(range(start_c, start_c+run)))]
                                   for start_r in seq(0, rows-run)
                                   for start_c in seq(0, columns-run)]
        solutions = sum([horizontal_solutions, vertical_solutions, diagonal_solutions_down_right, diagonal_solutions_down_left], [])
        cls.cached_solutions = [[coords2index(pos) for pos in solution] for solution in solutions]
        return cls.cached_solutions

    def result(self):
        if self.is_tie():
            return -1
        else:
            for solution in self.get_solutions():
                if all(self.board[index] for index in solution):
                    color = self.board[solution[0]]
                    return self.color_mapping[color]
            return 0
