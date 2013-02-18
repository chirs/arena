
import json
import socket

def start(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("Accepting connection on host", socket.gethostname(), ", port ", port)
    sock.listen(2) 
    player1_sock, _ = sock.accept()
    print("Player 1 connected")
    player2_sock, _ = sock.accept()
    print("Player 2 connected")
    return (sock, player1_sock, player2_sock)

def stop(socket_list):
    for sock in socket_list:
        sock.close()

def get_json(player_socket):
    msg = player_socket.recv(1028).decode()
    json_ = json.loads(msg)
    return json_

def send_json(player_socket, json_):
    s = json.dumps(json_)
    player_socket.sendall(s.encode())

