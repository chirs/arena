
import sys

from client import play, connect



class TicTacToe(object):

    memo = {}

    def __init__(self, board=None):
        if board is None:
            board = ' ' * 9
        self.board = board


    def current_player(self):
        # Player 1 or player 2.

        unplayed = self.board.count(' ')
        if unplayed %2 == 1:
            return 1
        else:
            return 2

    def get_symbol(self, player):
        return {
            1: 'x',
            2: 'o',
            }[player]


    def get_player(self, symbol):
        return {
            'x': 1,
            'o': 2,
            }[symbol]


    def draw_board(self):
        print(self.board[:3])
        print(self.board[3:6])
        print(self.board[6:9])
        print("===")

    def opponent(self, player):
        if self.current_player() == 1:
            return 2
        else:
            return 1


    def winner(self):
        WINCOMBOS = [[0,1,2], [3,4,5], [6,7,8],
                     [0,3,6], [1,4,7], [2,5,8],
                     [0,4,8], [2,4,6]]
        
        for line in WINCOMBOS:
            s = set([self.board[e] for e in line])
            if len(s) == 1 and ' ' not in s:
                winner = s.pop()
                return self.get_player(winner)
        return None


    def is_tie(self):
        return self.board.count(' ') == 0

    def over(self):
        return self.winner() or self.is_tie()

    def board_score(self, player):
        w = self.winner()
        if w:
            if w == player:
                return 1
            else:
                return -1

        else:
            if self.is_tie():
                return 0
            else:
                return None



    def minimax_score(self):
        #print len(self.memo)

        player = self.current_player()

        if (player, self.board) in self.memo:
            return self.memo[(player, self.board)]

        #import pdb; pdb.set_trace()

        score = self.board_score(player)
        if score is not None:
            self.memo[(player, self.board)] = score

            #self.draw_board()
            #print("Score: %s, player: %s" % (score, player))
            return score

        else:
            potential_moves = self.get_legal_moves()
            potential_states = [self.transition(move) for move in potential_moves]
            scores = [-1 * state.minimax_score() for state in potential_states] # Reverse because this is opponent's minimax score.

            #self.draw_board()
            #print("Score: %s, player: %s" % (max(scores), player))

            return max(scores)

    def minimax_move(self):
        potential_moves = self.get_legal_moves()
        potential_states = [self.transition(move) for move in potential_moves]
        scores = [state.minimax_score() for state in potential_states]
        best_score = min(scores)
        move_index = scores.index(best_score)
        return potential_moves[move_index]



    def get_legal_moves(self):
        return [index for index, value in enumerate(self.board) if value == ' ']

    def transition(self, index):
        symbol = self.get_symbol(self.current_player())
        l = list(self.board)
        if l[index] == ' ':
            l[index] = symbol
            return TicTacToe(''.join(l))
        else:
            raise
        
        


def play_tictactoe(host, port):
    sock = connect(host, port, 'tictactoe')
    return play(sock, get_move)

def get_move(state):
    #import pdb; pdb.set_trace()
    board = state['board']
    t = TicTacToe(board)
    move = t.minimax_move(t.current_player)
    return move
    

if __name__ == "__main__":
    play_tictactoe('', 12345)

    #print(TicTacToe('xxx      ').board_score(1))
    #print(TicTacToe('ooo      ').board_score(1))
    
    #print c.get_legal_moves()
    #print c.minimax_score('x')

    #c = TicTacToe('xx oo ox ')
    #c = TicTacToe('xox      ')
    #c.draw_board()

    #while not c.over():
    #    move = c.minimax_move(c.current_player())
    #    c = c.transition(move)
    #    c.draw_board()        


