
import datetime
import json
import hashlib

class Match(object):
    """
    Represents a game currently being played between two networked players.
    """

    def __init__(self, gname, gobj):
        self.game_id = self.create_game_id()
        self.move_id = self.create_move_id()
        self.gname = gname # Name of the game, e.g. checkers
        self.game = gobj # Game objects, e.g. ConnectFour(' ' * 42)
        self.players = []
        self.history = []
        self.log = ""
        self.timeout_limit = 5
        self.last_move_time = None
        self.result = 0

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
        return self.players[self.game.current_player-1]

    def move_legal(self, move):
        if not isinstance(move, dict):
            return False
        if 'move' not in move:
            self.log += "Key \'move\' not in move json\n" 
            return False
        if 'token' not in move:
            self.log += "Move json does not contain \'token\'\n" 
            return False
        if move['token'] != self.move_id:
            self.log += "Player %s submitted incorrect token\n" % \
                    self.game.current_player
            return False

        return self.game.move_legal(move['move'])

    def make_move(self, msg):

        try:
            move = json.loads(msg)
        except ValueError:
            self.log += "Player %s submitted ill-formed json\n" % self.game.current_player
            self.result = 3 - self.game.current_player
            return

        if self.move_legal(move):
            self.move_id = self.create_move_id()
            self.history.append(move['move'])
            self.game.transition(move['move'], self.game.current_player)
            self.set_last_move_time()
        else:
            self.log += "Player %s submitted illegal move\n" % self.game.current_player
            self.result = 3 - self.game.current_player

    def set_last_move_time(self):
        self.last_move_time = datetime.datetime.now()

    def get_result(self):
        if not self.result:
            if self.time_expired():
                self.log += "Player %s took too long to submit move\n" % \
                        self.game.current_player
                self.result = 3 - self.game.current_player

            self.result = self.game.result()

        return self.result
 
    def time_expired(self):
        if self.last_move_time is None:
            return False

        seconds = (datetime.datetime.now() - self.last_move_time).seconds
        return seconds > self.timeout_limit

    def build_state(self, player=None):

        player = player or self.game.current_player

        state = {
            'player': player,
            'board': self.game.board,
            'result': self.get_result(),
            'token': self.move_id,
                 }

        if self.get_result():
            state.update({
                    'history': self.history,
                    'log': self.log,
                    })

        return state

