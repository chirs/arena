# Arena

A network framework for staging turn-based, 1-vs-1 games against human or AI players.

### Getting started

In one terminal, launch the server with game (Checkers, TicTacToe or ConnectFour case-sensitive), host '' and port:

`$ plumbing/supervisor.py Checkers '' 1060`

In another terminal, connect player 1:

`$ client/checkers.py alexandre-1225B 1060`

In another terminal, connect player 2:

`$ client/checkers.py alexandre-1225B 1060`

### Wish List
* Add history and logs to state so that clients can do postmortem of games
* Improve initial "handshake" with client, specifying the game played, player number, time limit for move, etc...
* Fix doctests in checkers.py
* Add time periods players have to submit their move within
* Write clients in different languages
* Documentation
