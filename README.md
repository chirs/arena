# Arena

A game server for staging turn-based, 1-vs-1 match between AI players.

Uses a server/client framework using TCP sockets so players can be written in your language of choice.

## Quick example

In one terminal, launch the server, host and port:

`$ plumbing/supervisor.py some.host.here 12345`

In another terminal, connect player 1:

`$ client/python/checkers.py some.host.here 12345`

In another terminal, connect player 2:

`$ client/python/checkers.py some.host.here 12345`

## Wish List
* Improve initial "handshake" with client, specifying the game played, player number, time limit for move, etc...
* Fix doctests in checkers.py
* Add time periods players have to submit their move within
* Write clients in different languages
* Documentation
