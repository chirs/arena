#!/usr/bin/python3

import sys

from server import start, stop, get_json, send_json

from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers
from gameplay.connect4 import ConnectFour

GAMES = {'tictactoe':TicTacToe, 'checkers':Checkers, 'connectfour':ConnectFour}

def build_state(player, board, winner, history):
    return {
        'player': player,
        'board': board,
        'winner': winner,
        'history': history,
        }

def play(sockets, game_class):

    player = 1
    game = game_class()
    history = []

    while True:
        player_sock = sockets[player]
        state = build_state(player, game.board, 0, history)
        send_json(player_sock, state)

        move = get_json(player_sock)

        if game.move_legal(move):

            player = 3 - player # Toggle between 1 and 2...
            history.append(move)
            game.draw_board()
            game.transition(move, player)

            result = game.result()
            if result:
                game.draw_board()
                print("Game over!")
                send_json(sockets[1], build_state(1, game.board, result, history))
                send_json(sockets[2], build_state(2, game.board, result, history))
                return

def play_wrapper(host, port, game):
    sockets = start(host, port)
    params1 = get_json(sockets[1])
    params2 = get_json(sockets[2])
    send_json(sockets[1], {'game':game, 'player':1})
    send_json(sockets[2], {'game':game, 'player':2})
    print("Game starts!\n")
    play(sockets, GAMES[game.lower()])
    stop(sockets)

if __name__ == "__main__":
    [_, game, host, port] = sys.argv
    play_wrapper(host, int(port), game)

