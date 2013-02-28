import socket
import threading
import time

from plumbing.supervisor import Supervisor
from gameplay.tictactoe import TicTacToe

import sys
sys.stderr = open('log/testerrors.txt', 'w')

ip, port = 'localhost', 8123

def server_alive_after_send(message_list):
    global port
    port += 1

    server = Supervisor(ip, port, {'tictactoe':TicTacToe}, silent=True)
    stop = False
    def supervise():
        while not stop:
            server.loop(.1)

    t = threading.Thread(target=supervise)
    t.daemon = True
    t.start()
    time.sleep(.3)

    s1 = socket.socket()
    s1.connect((ip, port))

    s2 = socket.socket()
    s2.connect((ip, port))


    for player, message in message_list:
        sock = {
            1: s1,
            2: s2,
            }[player]

        message = message.encode()
        sock.send(message)


    time.sleep(.3)
    result = t.is_alive()
    stop = True
    t.join()
    return result

test_ill_formed_json = lambda: server_alive_after_send([(1,'asdf')])
test_json_no_game = lambda: server_alive_after_send([(1,'{}')])
test_wrong_game = lambda: server_alive_after_send([(1,'{"game":"nottictactoe"}')])
test_right_game = lambda: server_alive_after_send([(1,'{"game":"tictactoe"}')])
test_two_connections = lambda: server_alive_after_send([(1,'{"game":"tictactoe"}'), (2, '{"game": "tictactoe"}')])
test_badly_formed_move = lambda: server_alive_after_send([(1,'{"game":"tictactoe"}'), (2, '{"game": "tictactoe"}'), (1, '{"fail"')])

tests = [(f, name) for name, f in locals().items() if callable(f) and 'test_' in name]
for f, name in tests:
    sys.stderr.write("Running test %s\n\n" % name)
    print(name, f())

sys.stderr.close()
