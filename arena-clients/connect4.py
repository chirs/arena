
import time

from client import play, connect



def index2coords(num):
    return (num//7, num % 7)

def coords2index(coords):
    return 7*coords[0] + coords[1]

def is_valid(coords):
    return 0 <= coords[0] < 6 and 0 <= coords[1] < 7

class ConnectFour(object):
    """
    An abstract Game object.
    """

    player_mapping = {1: 'b', 2: 'r'}
    color_mapping = {v: k for k, v in player_mapping.items()}

    cached_solutions = None # Runs of 4 that could potentially win.
    board_scores = {}

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
        indexes = [coords2index(e) for e in coords]
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


    def count_threats(self, player):
        threats = []
        solutions = self.get_solutions()
        color = self.player_mapping[player]

        #for cell_list in self.get_solutions():
        for cell_list in reversed(self.get_solutions()):
            values = [self.board[index] for index in cell_list]
            print values
            #import pdb; pdb.set_trace()
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


    def utility(self):  
        # utility is from player #1's perspective (+1 if #1 wins, -1 if #1 loses)
        winner = self.winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1
        else:
            return 0


    def heuristic(self):
        return self.count_threats(1) - self.count_threats(2)

        
    def minimax_score(self):
        """
        Get the minimax score of the current position.
        Minimax is a decision rule that finds the best 
        strategy in a game with an adversary who acts ideally.
        It operates by minimizing the worst case scenario.
        """

        # Retrieve a memoized minimax score.
        if self.board in self.board_scores:
            return self.board_scores[self.board]

        # If the game is over, return the board's utility from
        # the perspective of player 1.
        if self.is_over():
            utility = self.utility()

        # Otherwise, compute the value of the row below you.
        else:
            moves = self.legal_moves() # Generate the next layer of the decision tree.
            states = [self.transition(move) for move in moves] # Create the nodes for this tree.
            values = [e.minimax_score() for e in states] # Calculate minimax values for each of the states.

            if self.current_player() == 1:
                utility = max(values)
            else:
                utility = min(values)

        # Memoize and return the discovered result.
        self.board_scores[self.board] = utility
        return utility


    def minimax_move(self):
        moves = self.legal_moves() # Generate the next layer of the decision tree.
        states = [self.transition(move) for move in moves] # Create the nodes for this tree.
        values = [e.minimax_score() for e in states] # Calculate minimax values for each of the states.

        if self.current_player() == 1:
            v = max(values)
        else:
            v = min(values)

        i = values.index(v)
        return moves[i]

        return 0


    def search_moves(self):
        pass


    def move(self):

        # Best initial move, avoid intense initial recursion.
        if self.board.count(' ') == 42:
            return 3

        # Make this a variable.
        while time.time() - self.start_time < 4.5:
            self.search_moves()

        return self.best_move
            



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
