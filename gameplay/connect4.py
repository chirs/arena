
from arena.gameplay.game import Game


def index2coords(num):
    a, b = (num/7, num % 7)
    return (a,b)


def coords2index(coords):
    a, b = coords
    return 7*a + b

class ConnectFour(Game):
    """
    An abstract Game object.
    """

    player_mapping = {
        1: 'b',
        2: 'r',
        }

    def __init__(self, board=None, current_player=1):
        self.board = board or self.initial_board()
        self.current_player = current_player

    @staticmethod
    def initial_board():
        return ' ' * 42

    def draw_board(self):
        s = ''
        for i in range(0,42,7):
            s += self.board[i:i+7]
            s += '\n'
        s += '=' * 7
        print(s)

    def move_legal(self, move):
        """Check that the top field for the move column is open."""
        try:
            return self.board[move] == ' ' 
        except:
            import pdb; pdb.set_trace()
        5

    def transition(self, move, player):
        coords = [(e, move) for e in reversed(range(6))]
        indexes = [coords2index(e) for e in coords]
        for i in indexes:
            if self.board[i] == ' ':
                bl = list(self.board)
                bl[i] = self.player_mapping[player]
                self.board = ''.join(bl)
                return

        raise


    def is_tie(self):
        empty_spaces = [e for e in self.board if e == ' ']
        return not empty_spaces


    def result(self):
        if self.is_tie():
            return -1
        else:
            return 0



