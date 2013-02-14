
import json
import socket

def start(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(2) 
    player1_sock, _ = sock.accept()
    player2_sock, _ = sock.accept()
    return (sock, player1_sock, player2_sock)


def stop(socket_list):
    for sock in socket_list:
        sock.close()
    

def get_move(player):
    msg = player.recv(1028).decode()
    move = json.loads(msg)
    return move


def send_state(player, state):
    s = json.dumps(state)
    print(s)
    player.sendall(s.encode())

