
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
        return isinstance(column, int) and 0 <= column < 7 and self.board[column] == ' '

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
        # This method could use a better name.        
        """
        Cache and return a list of all possible winning runs  (e.g. [[(0,0), (1,0), (2,0), (3,0)], [(0,0), (0,1)...]
        """

        if cls.cached_solutions is not None:
            return cls.cached_solutions

        def generate_run(coords, x_direction, y_direction):
            # Generate a list of coordinates in a specified pair of directions.
            a, b = coords
            l = [(a + i * x_direction , b + i * y_direction) for i in range(4)]
            valid = all([is_valid(e) for e in l])
            if valid:
                return l
            else:
                return []
            
        def generate_runs_for_cell(coords):
            runs = [generate_run(coords, 1, 0), generate_run(coords, 0, 1), generate_run(coords, 1, 1), generate_run(coords, 1, -1)]
            return [e for e in runs if e]
            
        solutions = []
        for i in range(0, 42):
            coords = index2coords(i)
            runs = generate_runs_for_cell(coords)
            solutions.extend(runs)

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

            return 0
