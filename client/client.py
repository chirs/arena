
import json
import socket
import random

from gameplay.checkers import move_legal

HOST = '127.0.0.1'
PORT = 1060


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock

def play(sock):
    #s.sendall("Hello")

    while True:
        msg = sock.recv(1028).decode()
        state = json.loads(msg)
        
        if state['winner']:
            print("%s wins" % state['winner'])
            sock.close()
            return

        else:
            move = get_move(state)
            move_json = json.dumps(move)
            sock.sendall(move_json.encode())


def get_move(state):
    board = state['board']
    i = 0
    while True:
        i += 1
        p1 = random.randint(0, 63)
        p2 = p1 + random.randint(-19, 19)
        move = (p1, p2)
        if move_legal(move, board):
            return move
        
    
def get_move_stupid(state):
    return (p1, p2)
    
    
if __name__ == "__main__":
    sock = connect()
    play(sock)
    

