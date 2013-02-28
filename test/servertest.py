import socket
import threading
import time

from plumbing.supervisor import Supervisor
from gameplay.tictactoe import TicTacToe

import sys
sys.stderr = open('testerrors.txt', 'w')

ip, port = 'localhost', 8123

def server_alive_after_send(msg):
    server = Supervisor(ip, port, {'tictactoe':TicTacToe})
    stop = False
    def supervise():
        while not stop:
            server.loop(.1)

    t = threading.Thread(target=supervise)
    t.daemon = True
    t.start()
    time.sleep(.2)

    msg = msg.encode()

    s = socket.socket()
    s.connect((ip, port))
    s.send(msg)
    time.sleep(.1)
    result = t.is_alive()
    stop = True
    t.join()
    return result

test_ill_formed_json = lambda: server_alive_after_send('asdf')
test_json_no_game = lambda: server_alive_after_send('{}')
test_wrong_game = lambda: server_alive_after_send('{"game":"nottictactoe"}')
test_right_game = lambda: server_alive_after_send('{"game":"tictactoe"}')

tests = [(f, name) for name, f in locals().items() if callable(f) and 'test_' in name]
for f, name in tests:
    print(name, f())

sys.stderr.close()
