
import json
import select
import sys

from .match import Match
from .server import make_listen_sock, get_json, send_json

def supervise(host, port):

    def handle_new_connection(listen_sock, match_list):
        # Side effects!
        pending_connection, _, _ = select.select([listen_sock], '', '', 0)
        if pending_connection:
            player_sock, _ = listen_sock.accept()

            # Receive play request
            request = player_sock.recv(1028).decode()
            request_json = json.loads(request)
            game_string = request_json['game']

            # Build acknowledgment
            acknowledgment = {'name' : game_string, 'timelimit':5}

            eligible_matches = [e for e in match_list if e.is_waiting() and e.gname == game_string]
            if eligible_matches:
                match = eligible_matches[0]
                acknowledgment['player'] = 2
            else:
                match = Match(game_string)
                match_list.append(match)
                acknowledgment['player'] = 1

            # Send acknowledgment
            send_json(player_sock, acknowledgment)

            match.add_player(player_sock)

            if match.is_ready():
                send_json(match.players[0], match.build_state())
                match.set_last_move_time()


    def handle_match(match, readable_sockets, complete_matches):
        # Side effects!
        sock = match.get_current_socket()
        result = None
        moved = False

        # A move has been made.
        if sock in readable_sockets:
            move = get_json(sock)

            if match.game.move_legal(move):
                match.make_move(move)
                moved = True

            else:
                print("Game over. Player %s forfeits because of illegal move." % match.game.current_player)
                result = 3 - match.game.current_player

        # No move has been made.
        else:
            if match.time_expired():
                print("Game over. Player %s forfeits because of time." % match.game.current_player)
                result = 3 - match.game.current_player

        if result is None:
            result = match.game.result()

        if result != 0:
            match.game.draw_board()
            complete_matches.append(match)
            for i, player in enumerate(match.players, start=1):
                send_json(player, match.build_state(player=i, result=result))

        elif moved is True:
            match.game.draw_board()
            send_json(match.get_current_socket(), match.build_state())
                        

    active_matches = []
    complete_matches = []

    listen_sock = make_listen_sock(host, port)
    
    while True:
        # Check for new connection.
        handle_new_connection(listen_sock, active_matches)

        # Iterate active matches.
        current_sockets = [e.get_current_socket() for e in active_matches]
        readable_sockets, _, _ = select.select(current_sockets, '', '', 0)

        for match in active_matches:
            handle_match(match, readable_sockets, complete_matches)

        # Clean up.
        active_matches = [e for e in active_matches if e not in complete_matches]
        complete_matches = []
