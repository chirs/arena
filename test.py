
import unittest

from tictactoe import TicTacToe

class TestSequenceFunctions(unittest.TestCase):


    def test_board_score(self):
        self.assertTrue(TicTacToe('         ').board_score(1) == None)

        # Tie games.
        self.assertTrue(TicTacToe('xoxxoxoxo').board_score(1) == 0)
        self.assertTrue(TicTacToe('xoxxoxoxo').board_score(2) == 0)

        # Detect win for player 1.
        self.assertTrue(TicTacToe('xxxoo o  ').board_score(1) == 1)
        self.assertTrue(TicTacToe('xxxoo o  ').board_score(2) == -1)

        # Detect win for player 2
        self.assertTrue(TicTacToe('xx ooo  x').board_score(1) == -1)
        self.assertTrue(TicTacToe('xx ooo  x').board_score(2) == 1)


    def test_minimax_score(self):

        # Verify minimax works with a complete board.
        self.assertTrue(TicTacToe('xoxxoxoxo').minimax_score(1) == 0)
        self.assertTrue(TicTacToe('xoxxoxoxo').minimax_score(2) == 0)

        # Here there be errors.
        self.assertTrue(TicTacToe('xx oo    ').minimax_score(1) == 1)
        self.assertTrue(TicTacToe('xx oo    ').minimax_score(2) == -1)

        #self.assertTrue(TicTacToe('xx oo   x').minimax_score(1) == -1)
        #self.assertTrue(TicTacToe('xx oo   x').minimax_score(2) == 1)


if __name__ == '__main__':
    unittest.main()
