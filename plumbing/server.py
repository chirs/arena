
import json
import socket

def make_listen_sock(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(100) 
    return sock

def get_json(player_socket):
    msg = player_socket.recv(1028).decode()
    try:
        return json.loads(msg)
    except ValueError:
        return None

def send_json(player_socket, json_):
    s = json.dumps(json_)
    player_socket.sendall(s.encode())

