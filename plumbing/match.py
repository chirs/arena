
import datetime
import hashlib

class Match(object):
    """
    Represents a game currently being played between two networked players.
    """

    def __init__(self, gname, gobj):
        self.game_id = self.create_game_id()
        self.move_id = self.create_move_id()
        self.gname = gname
        self.game = gobj
        self.players = []
        self.history = []
        self.log = ""
        self.timeout_limit = 5
        self.last_move_time = None

    def create_game_id(self):
        s = datetime.datetime.now().isoformat().encode()
        return hashlib.sha1(s).hexdigest()

    def create_move_id(self):
        s = datetime.datetime.now().isoformat()
        s2 = ("%s %s" % (self.game_id, s)).encode()
        return hashlib.sha1(s2).hexdigest()

    def add_player(self, socket):
        self.players.append(socket)

    def is_waiting(self):
        return len(self.players) < 2

    def is_ready(self):
        return not self.is_waiting()

    def get_current_socket(self):
        current_player = self.game.current_player
        return self.players[current_player-1]

    def move_legal(self, move):
        if move['token'] != self.move_id:
            self.log += "Player %s submitted incorrect token" % self.game.current_player
            return False

        legal = self.game.move_legal(move['move'])

        if not legal:
            self.log += "Player %s submitted illegal move %s" % \
                                        (self.game.current_player, move['move'])

        return legal

    def make_move(self, move):
        self.game.transition(move['move'], self.game.current_player)
        self.history.append(move['move'])
        self.set_last_move_time()
        self.move_id = self.create_move_id()

    def set_last_move_time(self, t=None):
        if t is None:
            t = datetime.datetime.now()
        self.last_move_time = datetime.datetime.now()

    def time_expired(self):
        if self.last_move_time is None:
            return False

        seconds = (datetime.datetime.now() - self.last_move_time).seconds

        timeout = seconds > self.timeout_limit

        if timeout:
            self.log += "Player %s took too long to submit move" % self.game.current_player

        return timeout 

    def build_state(self, player=None, result=None):

        player = player or self.game.current_player
        result = result or self.game.result()

        return {
            'player': player,
            'board': self.game.board,
            'result': result,
            'token': self.move_id,
            #'score': score,
            }

    def post_mortem(self):
        return {
            'history' : self.history,
            'log' : self.log,
            'result': self.game.result(),
            }

