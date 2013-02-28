import socket
import sys
import threading
import time

from gameplay.tictactoe import TicTacToe
from plumbing.supervisor import Supervisor


def server_alive_after_send(host, port, message_list):

    server = Supervisor(host, port, {'tictactoe':TicTacToe}, silent=True)
    stop = False
    def supervise():
        while not stop:
            server.loop(.1)

    t = threading.Thread(target=supervise)    
    t.daemon = True
    t.start()
    time.sleep(.3)

    s1 = socket.socket()
    s1.connect((host, port))

    s2 = socket.socket()
    s2.connect((host, port))


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


def run_tests():

    sys.stderr, old_stderr = open('log/testerrors.txt', 'w'), sys.stderr

    tests = [
        ('test_ill_formed_json', [(1,'asdf')]),
        ('test_json_no_game', [(1,'{}')]),
        ('test_wrong_game', [(1,'{"game":"nottictactoe"}')]),
        ('test_right_game', [(1,'{"game":"tictactoe"}')]),
        ('test_two_connections', [(1,'{"game":"tictactoe"}'), (2, '{"game": "tictactoe"}')]),
        ('test_badly_formed_move', [(1,'{"game":"tictactoe"}'), (2, '{"game": "tictactoe"}'), (1, '{"fail"')]),
        ('test_incorrect_token', [(1,'{"game":"tictactoe"}'), (2, '{"game": "tictactoe"}'), (1, '{"token": "incorrect token", "move": 0}')]),
        ]
    
    results = {}

    port = 8123

    for name, move_list in tests:
        port += 1
        sys.stderr.write("Running test %s\n\n" % name)
        results[name] = server_alive_after_send('localhost', port, move_list)

    sys.stderr.close()
    sys.stderr = old_stderr
    
    return results



