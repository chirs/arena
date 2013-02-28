
import json
import select
import socket

from .match import Match

def send_json(sock, data):
    sock.sendall((json.dumps(data)+'\n').encode())


class Supervisor():



    def __init__(self, host, port, known_games, silent=False):
        # Set up supervisor.
        self.known_games = known_games
        self.active_matches = {} # dict mapping socket => game object
        self.complete_matches = set()

        self.pending_sockets = [] # Sockets not yet connected to a game.

        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((host, port))
        self.listen_sock.listen(100)

        self.silent = silent



    def handle_new_connection(self):
        player_sock, _ = self.listen_sock.accept()
        self.pending_sockets.append(player_sock)

    def handle_game_request(self, player_sock):

        # Receive play request
        request = player_sock.recv(1028).decode()
        request_json = json.loads(request)
        game_string = request_json['game']

        eligible_matches = [e for e in self.active_matches.values() if e.is_waiting_for_player() and e.gname == game_string]
        if eligible_matches:
            match = eligible_matches[0]
        else:
            match = Match(game_string, self.known_games[game_string]())

        self.active_matches[player_sock] = match
        player_number = match.add_player(player_sock)

        self.pending_sockets.remove(player_sock)

        # build and send acknowledgment
        acknowledgment = {
            'name': game_string,
            'timelimit': 5,
            'player': player_number,
            }
        send_json(player_sock, acknowledgment)

        if match.is_ready():
            send_json(match.players[0], match.build_state())
            match.set_last_move_time()


    def handle_match_message(self, sock):
        match = self.active_matches[sock]

        move_msg = sock.recv(1028).decode()

        try:
            move = json.loads(move_msg)
            match.make_move(move)
        except ValueError:
            match.log("Player %s submitted ill-formed json" % match.game.current_player)
            match.result = 3 - match.game.current_player

        if self.silent is False:
            print(match.game.draw_board())

        if match.get_result() != 0:
            self.complete_matches.add(match)
            for i, player in enumerate(match.players, start=1):
                send_json(player, match.build_state(player=i))
        else:
            send_json(match.get_current_socket(), match.build_state())


    def supervise(self):
        while True:
            self.loop(5)

    def loop(self, timeout):

        current_sockets = [e.get_current_socket() for e in set(self.active_matches.values())]

        all_sockets = current_sockets + self.pending_sockets + [self.listen_sock]

        readable_sockets, _, _ = select.select(all_sockets, [], [], timeout)

        for sock in readable_sockets:
            if sock == self.listen_sock:
                self.handle_new_connection()
            elif sock in self.pending_sockets:
                self.handle_game_request(sock)
            else:
                self.handle_match_message(sock)

        # Clean up.
        self.active_matches = {s:g for (s, g) in self.active_matches.items() if g not in self.complete_matches}
        self.complete_matches = set()

