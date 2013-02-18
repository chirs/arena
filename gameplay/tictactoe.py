
from arena.gameplay.game import Game


class TicTacToe(Game):

    player_mapping = {
        1: 'x',
        2: 'o',
        }

    def __init__(self, board=None):
        self.board = board or self.initial_board()


    @staticmethod
    def initial_board():
        return ' ' * 9  


    def draw_board(self):
        print(self.board[:3])
        print(self.board[3:6])
        print(self.board[6:9])
        print("===")

    def transition(self, move, player):
        mark = self.player_mapping[player]
        l = list(self.board)
        l[move] = mark
        self.board = ''.join(l)
        #new_state = TicTacToe(''.join(l))
        #return new_game
        
    def move_legal(self, move):
        return self.board[move] == ' '


    def is_tie(self):
        return ' ' not in self.board
    
    def winner(self):
        WINCOMBOS = [[0,1,2], [3,4,5], [6,7,8],
                     [0,3,6], [1,4,7], [2,5,8],
                     [0,4,8], [2,4,6]]
        
        for line in WINCOMBOS:
            s = set([self.board[e] for e in line])
            if len(s) == 1 and ' ' not in s:
                winner = s.pop()
                return winner
        return None

    def result(self):
        if self.is_tie():
            return -1
        else:
            w = self.winner()
            if w is None:
                return 0
            else:
                # return w
                return 1


