
import json
import select
import socket

from .match import Match

def supervise(host, port, known_games):

    def handle_new_connection(listen_sock, match_list):
        # Side effects!
        player_sock, _ = listen_sock.accept()

        # Receive play request
        request = player_sock.recv(1028).decode()
        request_json = json.loads(request)
        game_string = request_json['game']

        # Build acknowledgment
        acknowledgment = {'name' : game_string, 'timelimit':5}

        eligible_matches = [e for e in match_list.values() if e.is_waiting() and e.gname == game_string]
        if eligible_matches:
            match = eligible_matches[0]
            acknowledgment['player'] = 2
        else:
            match = Match(game_string, known_games[game_string]())
            acknowledgment['player'] = 1

        # Send acknowledgment
        player_sock.sendall(json.dumps(acknowledgment).encode())

        match_list[player_sock] = match
        match.add_player(player_sock)

        if match.is_ready():
            match.players[0].sendall(json.dumps(match.build_state()).encode())
            match.set_last_move_time()

    def handle_match(match, sock, complete_matches):
        # Side effects!

        move = sock.recv(1028).decode()
        match.make_move(move)
        match.game.draw_board()

        if match.get_result() != 0:
            complete_matches.add(match)
            for i, player in enumerate(match.players, start=1):
                player.sendall(json.dumps(match.build_state(player=i)).encode())
        else:
            match.get_current_socket().sendall(json.dumps(match.build_state()).encode())


    # Set up supervisor.
    active_matches = {} # dict mapping socket => game object
    complete_matches = set()

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind((host, port))
    listen_sock.listen(100) 

    while True:

        # Iterate active matches.
        current_sockets = [e.get_current_socket() for e in set(active_matches.values())]
        readable_sockets, _, _ = select.select(current_sockets + [listen_sock], '', '', 60)

        for socket_ in readable_sockets:
            if socket_ == listen_sock:
                # New connection.
                handle_new_connection(socket_, active_matches)
            else:
                if active_matches[socket_].is_ready():
                    handle_match(active_matches[socket_], socket_, complete_matches)

        # Clean up.
        active_matches = {s:g for (s, g) in active_matches.items() if g not in complete_matches}
        complete_matches = set()

