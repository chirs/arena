
import json
import select
import socket

from .match import Match

def send_json(sock, data):
    sock.sendall((json.dumps(data)+'\n').encode())

def supervise(host, port, known_games):

    def handle_new_connection(listen_sock, match_list):

        player_sock, _ = listen_sock.accept()

        # Receive play request
        request = player_sock.recv(1028).decode()
        request_json = json.loads(request)
        game_string = request_json['game']

        eligible_matches = [e for e in match_list.values() if e.is_waiting() and e.gname == game_string]
        if eligible_matches:
            match = eligible_matches[0]
        else:
            match = Match(game_string, known_games[game_string]())

        match_list[player_sock] = match
        player_number = match.add_player(player_sock)

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

    def handle_match_message(match, sock, complete_matches):

        move_msg = sock.recv(1028).decode()

        try:
            move = json.loads(move_msg)
            match.make_move(move)
        except ValueError:
            match.log("Player %s submitted ill-formed json" % match.game.current_player)
            match.result = 3 - match.game.current_player

        match.game.draw_board()

        if match.get_result() != 0:
            complete_matches.add(match)
            for i, player in enumerate(match.players, start=1):
                send_json(player, match.build_state(player=i))
        else:
            send_json(match.get_current_socket(), match.build_state())



    # Set up supervisor.
    active_matches = {} # dict mapping socket => game object
    complete_matches = set()

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((host, port))
    listen_sock.listen(100) 

    while True:

        # Iterate active matches.
        current_sockets = [e.get_current_socket() for e in set(active_matches.values())]
        readable_sockets, _, _ = select.select(current_sockets + [listen_sock], '', '', 60)

        for sock in readable_sockets:
            if sock == listen_sock:
                # New connection.
                handle_new_connection(sock, active_matches)
            else:
                if active_matches[sock].is_ready():
                    handle_match_message(active_matches[sock], sock, complete_matches)

        # Clean up.
        active_matches = {s:g for (s, g) in active_matches.items() if g not in complete_matches}
        complete_matches = set()

