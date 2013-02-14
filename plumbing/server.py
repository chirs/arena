

import socket

def start(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2) 
    player1, _ = sock.accept()
    player2, _ = sock.accept()
    return (player1, player2)

def get_move(player):
    return player.recv(1028)  


def send_board(player, board):
    player.sendall(board)


