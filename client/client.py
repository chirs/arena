
import json
import socket

def connect(host, port, game):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    params = {'game':game}
    sock.sendall(json.dumps(params).encode())
    return sock


def play(sock, move_function):

    print("playing")

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

