
import json
import socket

def make_listen_sock(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100) 
    return sock

def get_json(player_socket):
    msg = player_socket.recv(1028).decode()
    
    if msg:
        return json.loads(msg)
    else:
        return None

def send_json(player_socket, json_):
    s = json.dumps(json_)
    player_socket.sendall(s.encode())

