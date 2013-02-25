
import sys
import json
import socket

def setup(host, port):

    # Connect player 1
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((host, port))

    # Connect player 2
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket2.connect((host, port))

    return [socket1, socket2]

def cleanup(sockets):
    [s.close() for s in sockets]

def test_case(host, port, case):

    sockets = setup(host, port)

    # Send play requests, receive acknowledgments
    params = {'game':case['game']}
    for i, socket_ in enumerate(sockets):
        socket_.sendall(json.dumps(params).encode())
        msg = socket_.recv(1000).decode() # receives acknowledgment
        ack = json.loads(msg)

        # Check acknowledgment is correct
        expected = {'name':case['game'], 'player':i+1, 'timelimit':5}
        if ack != expected:
            print("\nIncorrect acknowledgment:\n", ack, "!=", expected, "!!!")
            cleanup(sockets)
            return False

    # Play game
    outcome = None
    for i, move in enumerate(case['history']):

        player = i%2+1 # toggle between 1 and 2

        # Receive game state
        msg = sockets[player-1].recv(1028).decode()
        state = json.loads(msg)

        move_wrapper = {'token':state['token'], 'move':move}

        # Send move
        sockets[player-1].sendall(json.dumps(move_wrapper).encode())

        if state['player'] != player:
            print("\nGame server returned wrong player")
            cleanup(sockets)
            return False

        if (not isinstance(state['board'], str)):
            print("\nGame server returned a board that is not a string")
            cleanup(sockets)
            return False

        outcome = state['result']

    # Receive and discard last board state
    for socket_ in sockets:
        _ = socket_.recv(1028).decode()

    # Receive post morterm
    if case['result']: 
        for socket_ in sockets:
            # Made this very large to accomodate history data.
            msg = socket_.recv(10000).decode()
            postmortem = json.loads(msg)
            outcome = postmortem['result']

            if postmortem['history'] != case['history']:
                print(postmortem)
                print("\nGame server returned wrong game history!")
                cleanup(sockets)
                return False

    # Check correct game outcome
    if outcome != case['result']:
        print("\nGame server returned wrong game results")
        cleanup(sockets)
        return False

    # Close sockets
    cleanup(sockets)

    return True

if __name__ == "__main__":

    _, host, port = sys.argv

    from cases import cases

    results = [test_case(host, int(port), case) for case in cases]

    print("\nPassed", sum(results), "out of", len(results), "tests\n")
    
    def pretty_print(case_id, game):
        print("Failed test: case_id:", case_id, ", game:", game)

    [pretty_print(cases[i]["case_id"], cases[i]["game"]) for i, result in enumerate(results) if not result]

    print()

