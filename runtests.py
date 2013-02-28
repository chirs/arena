
import sys

from plumbing.supervisor import Supervisor
from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers
from gameplay.connect4 import ConnectFour

from test import protocoltests, servertests

GAMES = {
    'tictactoe': TicTacToe,
    'checkers': Checkers,
    'connectfour':ConnectFour,
}

if __name__ == '__main__':
    results = {}
    results.update(protocoltests.run_tests(GAMES))
    results.update(servertests.run_tests())

    print("\nPassed", len([e for e in results.values() if e]), "out of", len(results), "tests")

    """
    def pretty_print(case_id, game):
        print("Failed test: case_id:", case_id, ", game:", game)

    [pretty_print(cases[i]["case_id"], cases[i]["game"]) for i, result in enumerate(results) if not result]

    print()
    """

