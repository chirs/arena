
from arena.plumbing.supervisor import play_wrapper
from arena.gameplay.tictactoe import TicTacToe
from arena.gameplay.checkers import Checkers


if __name__ == "__main__":
    play_wrapper(Checkers)
