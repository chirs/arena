
import json
import socket

def start(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2) 
    player1, _ = server.accept()
    player2, _ = server.accept()
    return (player1, player2)

def get_move(player):
    msg = player.recv(1028).decode()
    move = json.loads(msg)
    return move


def send_state(player, state):
    s = json.dumps(state)
    print(s)
    player.sendall(s.encode())

