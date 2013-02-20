
import json
import socket
import pickle

from gencases import cases

def test_case(host, port, case):

    # Connect player 1
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((host, port))

    # Connect player 2
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket2.connect((host, port))

    sockets = [socket1, socket2]

    # Send play requests, receive acknowledgments
    params = {'game':case['name']}
    for i, socket_ in enumerate(sockets):
        socket_.sendall(json.dumps(params).encode())
        msg = socket_.recv(10000).decode()
        ack = json.loads(msg)

        # Check acknowledgment is correct
        expected = {'name':case['name'], 'player':i+1, 'timelimit':5}
        try:
            assert(ack == expected)
        except AssertionError:
            print("Incorrect acknowledgment:", ack, "!=", expected, "!!!")
            return False

    # Play game
    for i, move in enumerate(case['history']):

        player = i%2+1 # toggle between 1 and 2

        # Send move
        sockets[player-1].sendall(json.dumps(move).encode())

        # Receive game state
        msg = sockets[player-1].recv(10000).decode() # Made this very large to accomodate history data.
        state = json.loads(msg)

        try:
            assert(state['player'] == player)
            assert(state['history'] == case['history'][:i])
        except AssertionError:
            print("Game server returned incorrect player or history")
            return False

    # Receive game result
    outcome = 0
    for socket_ in sockets:
        msg = socket_.recv(10000).decode() # Made this very large to accomodate history data.
        state = json.loads(msg)
        outcome = state['winner']

    # Check correct game outcome
    try:
        assert(outcome==case['result'])
    except AssertionError:
        print("Incorrect game outcome; expected", case['result'], ", got",outcome)
        return False

    # Close sockets
    for socket_ in sockets:
        socket_.close()

    return True

if __name__ == "__main__":

    HOST = ''
    PORT = 12345

    #cases = pickle.load(open("test_cases.p", "rb"))

    results = [test_case(HOST, PORT, case) for case in cases]

    print("\nPassed", sum(results), "out of", len(results), "tests\n")

