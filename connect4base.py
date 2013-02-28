
from client import play, connect


class ConnectFourBase(object):
    """
    An abstract Game object.
    """

    player_mapping = {1: 'b', 2: 'r'}
    color_mapping = {v: k for k, v in player_mapping.items()}

    cached_solutions = None # Runs of 4 that could potentially win.
    board_scores = {}


    @staticmethod
    def index2coords(num):
        return (num//7, num % 7)

    @staticmethod
    def coords2index(coords):
        return 7*coords[0] + coords[1]

    @staticmethod
    def is_valid(coords):
        return 0 <= coords[0] < 6 and 0 <= coords[1] < 7



    def __init__(self, board=None):
        self.board = board or ' ' * 42

        self.best_move = None

        self.start_time = time.time()

        #self.time_limit = 5

    def current_player(self):
        x_plays = self.board.count('x') 
        if x_plays % 2 == 0:
            return 1
        else:
            return 2


    def opponent(self):
        return self.current_player() - 2

    def draw_board(self):
        s = '\n'.join([self.board[i:i+7] for i in range(0, 42, 7)] + ['='*7])
        print(s)

    def move_legal(self, column):
        """Check that the top field for the column is open."""
        return self.board[column] == ' '

    def legal_moves(self):
        return [e for e in range(7) if self.move_legal(e)]

    def transition(self, move):
        coords = [(e, move) for e in reversed(range(6))]
        indexes = [self.coords2index(e) for e in coords]
        for i in indexes:
            if self.board[i] == ' ':
                board = self.board[:i] + self.player_mapping[self.current_player()] + self.board[i+1:]
                return ConnectFour(board)

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
            valid = all([self.is_valid(e) for e in l])
            if valid:
                return l
            else:
                return []
            
        def generate_runs_for_cell(coords):
            runs = [generate_run(coords, 1, 0), generate_run(coords, 0, 1), generate_run(coords, 1, 1), generate_run(coords, 1, -1)]
            return [e for e in runs if e]
            
        solutions = []
        for i in range(0, 42):
            coords = self.index2coords(i)
            runs = generate_runs_for_cell(coords)
            solutions.extend(runs)

        cls.cached_solutions = [[self.coords2index(pos) for pos in solution] for solution in solutions]            
        return cls.cached_solutions


    def count_threats(self, player):
        threats = []
        solutions = self.get_solutions()
        color = self.player_mapping[player]

        #for cell_list in self.get_solutions():
        for cell_list in reversed(self.get_solutions()):
            values = [self.board[index] for index in cell_list]
            print values
            if ' ' in values and values.count(color) == 3:
                threats.append(cell_list)
                
        return len(threats)


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

    def is_over(self):
        return self.result() != 0



def play_connect4(host, port):
    sock = connect(host, port, 'connectfour')
    return play(sock, get_move)

def get_move(state):
    board = state['board']
    g = ConnectFour(board)
    move = g.minimax_move()
    return move
    

if __name__ == "__main__":
    play_connect4('', 12345)
