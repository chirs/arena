
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
        if move['token'] != self.move_id:
            self.log += "Player %s submitted incorrect token\n" % \
                    self.game.current_player
            return False

        return self.game.move_legal(move['move'])

    def make_move(self, move):

        self.history.append(move['move'])

        if self.move_legal(move):
            self.move_id = self.create_move_id()
            self.set_last_move_time()
            self.game.transition(move['move'], self.game.current_player)
        else:
            self.log += "Player %s submitted illegal move %s\n" % \
                                (self.game.current_player, move['move'])
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

        result = seconds > self.timeout_limit

    def build_state(self, player=None):

        player = player or self.game.current_player

        state = {'player': player}
        state['board'] = self.game.board
        state['result'] = self.get_result()
        state['token'] = self.move_id

        if self.get_result():
            state['history'] = self.history
            state['log'] = self.log

        return state

