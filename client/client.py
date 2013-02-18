
import json
import socket

HOST = 'alexandre-1225B'
PORT = 1060

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock

def play(sock, move_function):

    while True:
        msg = sock.recv(1028).decode()
        state = json.loads(msg)
        
        if state['winner']:
            print("%s wins" % state['winner'])
            sock.close()
            return

        else:
            move = move_function(state)
            move_json = json.dumps(move)
            sock.sendall(move_json.encode())

