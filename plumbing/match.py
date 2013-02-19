
import datetime

from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers
from gameplay.connect4 import ConnectFour

class Match(object):
    # Represents a game currently being played between two networked players.

    GAMES = {
        'tictactoe': TicTacToe, 
        'checkers': Checkers, 
        'connectfour':ConnectFour,
        }

    def __init__(self, gname):
        self.gname = gname
        self.game = self.GAMES[gname]()
        self.players = []
        self.history = []
        self.last_move_time = None

    def add_player(self, socket):
        self.players.append(socket)

    def is_waiting(self):
        return len(self.players) < 2

    def is_ready(self):
        return not self.is_waiting()

    def get_current_socket(self):
        current_player = self.game.current_player
        return self.players[current_player-1]

    def make_move(self, move):
        print("Moving")
        print("CP: %s" % self.game.current_player)
        self.game.transition(move, self.game.current_player)
        self.history.append(move)
        self.set_last_move_time()



    def set_last_move_time(self, t=None):
        if t is None:
            t = datetime.datetime.now()
        self.last_move_time = datetime.datetime.now()

    def time_expired(self):
        if self.last_move_time is None:
            return False

        seconds = (datetime.datetime.now() - self.last_move_time).seconds
        return seconds > 5

    def build_state(self, player=None, result=None):

        if player is None:
            player = self.game.current_player

        if result is None:
            result = self.game.result()

        return {
            'player': player,
            'board': self.game.board,
            'winner': result,
            'history': self.history
            }

