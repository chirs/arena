#!/usr/bin/python3

import json
import datetime
import select
import sys

from match import Match
from server import make_listen_sock, get_json, send_json

def pending_connection(listen_sock):
    pending_connection, _, _ = select.select([listen_sock], '', '', 0)
    return pending_connection

def get_new_connection(listen_sock):
    game_sock, address = listen_sock.accept()
    return game_sock

def supervise(host, port):

    listen_sock = make_listen_sock(host, port)

    active_matches = []
    complete_matches = []
    
    while True:

        # Handle a new connection.
        if pending_connection(listen_sock):
            player_sock = get_new_connection(listen_sock)
            handshake = player_sock.recv(1028).decode()
            handshake_json = json.loads(handshake)
            game_string = handshake_json['game']

            eligible_matches = [e for e in active_matches if e.is_waiting() and e.gname == game_string]
            if eligible_matches:
                match = eligible_matches[0]
            else:
                match = Match(game_string)
                active_matches.append(match)

            match.add_player(player_sock)

            if match.is_ready():
                send_json(match.players[0], match.build_state())
                match.set_last_move_time()

        # Handle current games.

        current_sockets = [e.get_current_socket() for e in active_matches]
        readable_sockets, _, _ = select.select(current_sockets, '', '', 0)

        for match in active_matches:
            sock = match.get_current_socket()
            if sock in readable_sockets:
                move = get_json(sock)

                result = None

                if move:
                    if match.game.move_legal(move):
                        match.make_move(move)
                    else:
                        print("Game over. Player %s forfeits because of illegal move." % match.game.current_player)
                        result = 3 - match.game.current_player

                else:
                    if match.time_expired():
                        print("Game over. Player %s forfeits because of time." % match.game.current_player)
                        result = 3 - match.game.current_player
                        



                if result is None:
                    result = match.game.result()

                match.game.draw_board()

                if result != 0:
                    complete_matches.append(match)
                    for i, player in enumerate(match.players, start=1):
                        send_json(player, match.build_state(player=i, result=result))
                else:
                    send_json(match.get_current_socket(), match.build_state())
                        

        # Clean up.
        active_matches = [e for e in active_matches if e not in complete_matches]
        complete_matches = []
                
if __name__ == "__main__":
    [_, host, port] = sys.argv
    supervise(host, int(port))
 
