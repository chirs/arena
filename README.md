# Arena

A network framework for staging turn-based, 1-vs-1 against human or AI players.

### Getting started

In one terminal, launch the server:

`$ python3 plumbing/supervisor.py`

In another terminal, connect player I:

`$ python3 client/checkers.py`

In another terminal, connect player II:

`$ python3 client/checkers.py`

### Wish List
* Add history and logs to state so that clients can do postmortem of games
* Fix doctests in checkers.py
* Figure out how to run clients on different machines
* Write clients in different languages
* Documentation
