
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

    def move_legal(self, column):
        """Check that the top field for the column is open."""
        return self.board[column] == ' '

    def transition(self, move, player):
        assert player == self.current_player
        coords = [(e, move) for e in reversed(range(6))]
        indexes = [coords2index(e) for e in coords]
        for i in indexes:
            if self.board[i] == ' ':
                self.board = self.board[:i] + self.player_mapping[player] + self.board[i+1:]
                self.current_player = 3 - self.current_player
                return
        raise ValueError('column %d is full' % column)


    def is_tie(self):
        return self.board.count(' ') == 0

    @classmethod
    def get_solutions(cls):
        """
        Cache and eturn a list of all possible winning runs  (e.g. [[(0,0), (1,0), (2,0), (3,0)], [(0,0), (0,1)...]
        """
        # This method could use a better name.
        
        if cls.cached_solutions is not None:
            return cls.cached_solutions


        seq = lambda start, end: range(start, end+1)
        rows = 6
        columns = 7
        run = 4

        #solutions = []
        #for cell in range(0, 42):
        #    cell_solutions = generate_cell_solutions(cell)
        #    solutions.extend(cell_solutions)

        # Rework the logic for generating these.
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
            for cell_list in self.get_solutions():
                values = set([self.board[index] for index in cell_list])
                if len(values) == 1:
                    color = values.pop()
                    if color != ' ':
                        return self.color_mapping[color]
                
                """
                Pretty sure this logic is wrong.
                if all(self.board[index] for index in solution):
                    color = self.board[solution[0]]
                    return self.color_mapping[color]
                """
            return 0
