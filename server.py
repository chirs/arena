
from arena.plumbing.supervisor import play_wrapper
from arena.gameplay.tictactoe import TicTacToe
from arena.gameplay.checkers import Checkers
from arena.gameplay.connect4 import ConnectFour


if __name__ == "__main__":
    play_wrapper(Checkers)
    #play_wrapper(ConnectFour)
