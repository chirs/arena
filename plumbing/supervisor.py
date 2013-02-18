#!/usr/bin/python3

import sys

from server import start, stop, get_json, send_json

from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers
from gameplay.connect4 import ConnectFour



def build_state(player, board, winner, history):
    return {
        'player': player,
        'board': board,
        'winner': winner,
        'history': history,
        }


GAMES = {
        'tictactoe': TicTacToe, 
        'checkers': Checkers, 
        'connectfour':ConnectFour,
        }


def supervise(host, port):

    active_games = {}

    sock.bind((host, port))
    print("Accepting connection on host", socket.gethostname(), ", port ", port)
    sock.listen(200) 

    def end_game(gid, result):
        d = active_games[gid]
        send_json(d['players'][1], build_state(1, d.game.board, result, d.game.history))
        send_json(d['players'][2], build_state(2, d.game.board, result, d.game.history))
        active_games.pop(gid)


    while True:

        # New client logic.
        player_socket, _ = sock.accept() # This breaks the code since accept is blocking. (pretend it is non-blocking.)
        handshake = player_socket.recv(1028).decode()
        handshake_json = json.loads(handshake)
        game_string = handshake_json['game']
        game_class = game_classes[game_string]

        valid_games = [gid for gid, v in active_games.items() if v['players'][2] == None and v['name'] == game_string]

        if valid_games:
            # Player 2 logic
            g = valid_games[0]
            g['players'][2] = player_socket
            send_json(g['player1'], {'gid':gid, 'player':1})

        else:
            gid = datetime.datetime.now().isoformat()
            d = {
                'game': game_class(),
                'name': game_string,
                'players' {
                    1: player_socket,
                    2: None,
                    },
                'history': [],
                }
            active_games[gid] = d

        for gid, values in active_games.items():
            g = values['game']
            sock = values['players'][g.current_player]
            move = get_json(sock)
            if game.move_legal(move):
                g['history'].append(move)
                game.transition(move, player)

                result = game.result()
                if result:
                    print("Game over!")
                    end_game(gid, result)

            else:
                print("Game over. Player %s forfeits because of illegal move." % g.current_player)
                winner = 3 - g.current_player
                end_game(gid, winner)


if __name__ == "__main__":
    [_, host, port] = sys.argv
    supervise(host, port)
 
