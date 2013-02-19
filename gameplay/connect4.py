
from gameplay.game import Game


def index2coords(num):
    a, b = (num/7, num % 7)
    return (int(a),int(b))


def coords2index(coords):
    a, b = coords
    return int(7*a + b)

def is_valid(coords):
    x, y = coords
    return 0 <= x < 6 and 0 <= y < 7

class ConnectFour(Game):
    """
    An abstract Game object.
    """

    player_mapping = {
        1: 'b',
        2: 'r',
        }

    color_mapping = {
        'b': 1,
        'r': 2,
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
        return self.board[move] == ' ' 


    def transition(self, move, player):
        coords = [(e, move) for e in reversed(range(6))]
        indexes = [coords2index(e) for e in coords]
        for i in indexes:
            if self.board[i] == ' ':
                bl = list(self.board)
                bl[i] = self.player_mapping[player]
                self.board = ''.join(bl)
                self.current_player = 3 - self.current_player
                return

        raise


    def is_tie(self):
        empty_spaces = [e for e in self.board if e == ' ']
        return not empty_spaces



    def check_cells(self, l):
        last = None
        consecutive = 0
        for e in l:
            if e != last:
                last = e
                consecutive = 1
            else:
                consecutive += 1

            if consecutive == 4:
                return True

        return False
            
        
        

    def check_horizontal(self, index):
        value = self.board[index]
        if value.strip() == '':
            return False

        x, y = index2coords(index)
        coord_list = [(x, y+e) for e in range(-3, 4)]
        indexes = [coords2index(e) for e in coord_list if is_valid(e)]

        try:
            return self.check_cells([self.board[i] for i in indexes])
        except:
            import pdb; pdb.set_trace()
        x = 5


    def check_vertical(self, index):

        value = self.board[index]
        if value.strip() == '':
            return False

        x, y = index2coords(index)
        coord_list = [(x+e, y) for e in range(-3, 4)]
        indexes = [coords2index(e) for e in coord_list if is_valid(e)]
        return self.check_cells([self.board[i] for i in indexes])

    def check_diagonal1(self, index):

        value = self.board[index]
        if value.strip() == '':
            return False

        x, y = index2coords(index)
        coord_list = [(x+e, y+e) for e in range(-3, 4)]
        indexes = [coords2index(e) for e in coord_list if is_valid(e)]
        return self.check_cells([self.board[i] for i in indexes])

    def check_diagonal2(self, index):

        value = self.board[index]
        if value.strip() == '':
            return False

        x, y = index2coords(index)
        coord_list = [(x-e, y+e) for e in range(-3, 4)]
        indexes = [coords2index(e) for e in coord_list if is_valid(e)]
        return self.check_cells([self.board[i] for i in indexes])


    def result_for_cell(self, index):
        return self.check_horizontal(index) or\
            self.check_vertical(index) or\
            self.check_diagonal1(index) or \
            self.check_diagonal2(index)
            
        


    def result(self):
        if self.is_tie():
            return -1
        else:
            for index in range(0, 42):
                result = self.result_for_cell(index)
                if result:
                    color = self.board[index]
                    return self.color_mapping[color]

            return 0



