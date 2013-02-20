
import sys

from plumbing.supervisor import supervise
from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers
from gameplay.connect4 import ConnectFour

GAMES = {
    'tictactoe': TicTacToe,
    'checkers': Checkers,
    'connectfour':ConnectFour,
}

if __name__ == '__main__':
    _, host, port = sys.argv
    supervise(host, int(port), GAMES)

