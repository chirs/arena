# Arena

A game server for staging turn-based, 1-vs-1 match between AI players.

Uses a server/client framework using TCP sockets so players can be written in your language of choice.

## Quick example

In one terminal, launch the server, host and port:

`$ plumbing/supervisor.py some.host.here 12345`

In another terminal, connect player 1:

`$ clients/python/checkers.py some.host.here 12345`

In another terminal, connect player 2:

`$ clients/python/checkers.py some.host.here 12345`

## API

This section covers the API calls a client needs to handle. A game basically consist of three steps:

1. The AI client connects to the game server (host ??? and port ???)
2. The AI client sends a string encapsulating a JSON object (a.k.a. the "handshake"). This handshake must have the field "game" (see section Supported Games section). E.g.: "{game:checkers}" 

## Supported Games

<table>
  <tr>
    <th>Name</th><th>Board representation</th><th>Move representation</th>
  </tr>
  <tr>
    <td>checkers</td>
    <td>A 64 char-long string. Char position runs from left to right, top to bottom (e.g. position 10 represents the third square from the left in the second row from the top). Spaces (' ') represent empty squares, 'b' represents a player 1 pawn, 'B' represents a player 1 king. 'r' and 'R' are the same for player 2.</td>
    <td>A string encapsulating a 2 elements-long array with the beginning index and the end index (e.g. "[0,9]").</td>
  </tr>
  <tr>
    <td>tictactoe</td>
    <td>A 9 char-long string. Char position runs from left to right, top to bottom (e.g. position 4 represents the second square from the left in the second row from the top (the middle square)). Spaces (' ') represent empty squares, 'x' represents player 1, 'o' represents player 2.</td>
    <td>A string encapsulating an int with the index of the square the player wants to put its next mark in (e.g. "2").</td>
  </tr>
</table>

connectfour and chess are in the pipeline, let us know if you would like to see them implemented.

## Wish List
* Improve initial "handshake" with client, specifying the game played, player number, time limit for move, etc...
* Fix doctests in checkers.py
* Add time periods players have to submit their move within
* Write clients in different languages
* Get a test script together
* Documentation
