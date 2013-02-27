
import unittest

from tictactoe import TicTacToe
from connect4 import ConnectFour

class TestSequenceFunctions(unittest.TestCase):

    def test_tictactoe_minimax_score(self):
        # Minimax score assumes you are the next player to move.
        # Don't call it with the wrong player argument - will not give a 
        # trustworthy answer.


        # o can win on next move.
        self.assertTrue(TicTacToe('xx oo xox').minimax_score() == -1)

        
        # Verify minimax works with a complete board.
        self.assertTrue(TicTacToe('xoxxoxoxo').minimax_score() == 0)

        # Build up to a simple example.

        # Game is over, x has won.
        self.assertTrue(TicTacToe('xxxoo xo ').minimax_score() == 1) 

        # Game is over, o has won.
        self.assertTrue(TicTacToe('xx oooxox').minimax_score() == -1)
        

        # x can win on next move.
        self.assertTrue(TicTacToe('xx oo xo ').minimax_score() == 1)

        self.assertTrue(TicTacToe('xxoooxxo ').minimax_score() == 0)
        self.assertTrue(TicTacToe('xx ooxxoo').minimax_score() == 1)

        # Parent.
        self.assertTrue(TicTacToe('xx ooxxo ').minimax_score() == 0)


    def test_tictactoe_minimax_move(self):

        # Make the winning move.
        self.assertTrue(TicTacToe('xxooo x x').minimax_move() == 5)
        self.assertTrue(TicTacToe('xxooox  x').minimax_move() == 6)

        # Doesn't necessarily make the fastest winning move. Just makes 
        # a move that will necessarily win.
        self.assertTrue(TicTacToe('xx oo   x').minimax_move() == 2)

        self.assertTrue(TicTacToe('xx oo    ').minimax_move() == 2)

        # Test some trap cases.
        self.assertTrue(TicTacToe('xox      ').minimax_move() == 4)
        self.assertTrue(TicTacToe('xoxo     ').minimax_move() == 4)


    def _test_connect4(self):
        top_rows = ' ' * 28
        rows = top_rows + 'bbb    rrr    '
        g = ConnectFour(rows)

        import pdb; pdb.set_trace()

        self.assertTrue(g.minimax_score() == 1)
        self.assertTrue(g.minimax_move() == 3)
        
        g2 = g.transition(4)
        self.assertTrue(g2.minimax_move() == 3)

        g3 = g2.transition(3)
        self.assertTrue(g3.minimax_move() == 3)


    def test_connect4_threats(self):
        top_rows = ' ' * 28
        rows = top_rows + '  rrr  ' + '  bbb  '
        g = ConnectFour(rows)

        #import pdb; pdb.set_trace()

        self.assertTrue(g.count_threats(1) == 2)
        self.assertTrue(g.count_threats(2) == 2)

        g2 = g.transition(0)
        self.assertTrue(g2.count_threats(1) == 3)
        self.assertTrue(g2.count_threats(2) == 2)

        g2 = g.transition(0)
        self.assertTrue(g2.count_threats(1) == 3) # Really this is just two threats (two slots) !!Fix this
        self.assertTrue(g2.count_threats(2) == 2)

        g3 = g2.transition(1)
        self.assertTrue(g3.count_threats(1) == 1)
        self.assertTrue(g3.count_threats(2) == 2)


if __name__ == '__main__':
    unittest.main()
