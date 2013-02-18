
import json
import socket

HOST = '127.0.0.1'
PORT = 1060


def connect():
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

    
    
#if __name__ == "__main__":
#    sock = connect()
#    play(sock)
    

