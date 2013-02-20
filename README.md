# Arena

A game server for staging turn-based, 1-vs-1 match between AI players.

Uses a server/client framework using TCP sockets so players can be written in your language of choice.

## Quick example

In one terminal, launch the server, host and port:

`$ python3 supervise.py some.host.here 12345`

In another terminal, connect player 1:

`$ python3 clients/python/checkers.py some.host.here 12345`

In another terminal, connect player 2:

`$ python3 clients/python/checkers.py some.host.here 12345`

## API

This section covers the API calls a client needs to handle. A game basically consist of three steps:

(i) The AI client connects to the game server (host ??? and port ???)

(ii) The AI client sends a string encapsulating a JSON object (henceforth the "request"). This request must have the field "game" (see [Supported Games section](#games)). E.g.: "{game:checkers}" 

(iii) The server sends a string encapsulating a JSON object (henceforth the "acknowledgment"). This acknowledgment has the following fields:

<table>
  <tr>
    <th>Field name</th><th>Details</th>
  </tr>
  <tr>
    <td>name</td><td>checkers or tictactoe or etc</td>
  </tr>
  <tr>
    <td>player</td><td>1 or 2</td>
  </tr>
  <tr>
    <td>timelimit</td><td>5 seconds</td>
  </tr>
</table>

An example acknowledgement would be "{name:tictactoe, player:2, timelimit:5}".

(iv) The server sends a string encapsulating a JSON object (henceforth the "game state"). This game state has the following fields:
<table>
  <tr>
    <th>Field name</th><th>Details</th>
  </tr>
  <tr>
    <td>player</td><td>1 or 2</td>
  </tr>
  <tr>
    <td>board</td><td>board representation (see [supported games section](#games)</td>
  </tr>
  <tr>
    <td>winner</td><td>-1 is tie, 0 is game ongoing, 1 is player 1 wins, 2 is player 2 wins</td>
  </tr>
  <tr>
    <td>history</td><td>A list holding the sequence of moves done in the game</td>
  </tr>
  <tr>
    <td>log</td><td>A log of miscellaneous relevant info about the game</td>
  </tr>
</table>

An example of game state would be "{player:2, board:"xoxoxo   ", winner:0, history:[0,1,2,3,4,5], log:""}.

(v) The AI player sends the server a move (see [supported games section](#games) for the representation of moves for the different games)

Steps (iv) and (v) are repeated until the game is over.

## Supported Games <a id=games></a>

<table>
  <tr>
    <th>Name</th><th>Board representation</th><th>Move representation</th>
  </tr>
  <tr>
    <td>checkers (i.e. English draughts)</td>
    <td>A 64 char-long string. Char position runs from left to right, top to bottom (e.g. position 10 represents the third square from the left in the second row from the top). Spaces (' ') represent empty squares, 'b' represents a player 1 pawn, 'B' represents a player 1 king. 'r' and 'R' are the same for player 2.</td>
    <td>A string encapsulating a 2 elements-long array with the beginning index and the end index (e.g. "[0,9]").</td>
  </tr>
  <tr>
    <td>tictactoe</td>
    <td>A 9 char-long string. Char position runs from left to right, top to bottom (e.g. position 4 represents the second square from the left in the second row from the top (the middle square)). Spaces (' ') represent empty squares, 'x' represents player 1, 'o' represents player 2.</td>
    <td>A string encapsulating an int with the index of the square the player wants to put its next mark in (e.g. "2").</td>
  </tr>
  <tr>
    <td>connect four</td>
    <td>A 42 char-long string. Char position runs from left to right, top to bottom (e.g. position 0 represents the upper-left square, 18 represents the middle square in the third row (from the top). Spaces (' ') represent empty squares, 'x' represents player 1, 'o' represents player 2.</td>
    <td>A string between 0 and 6 inclusive, encapsulating an integer with the index of the column where the player wants to drop her next piece.</td>
  </tr>
</table>

chess is in the pipeline, let us know if you would like to see it implemented.

## Test Suite

To run the test suite:

(i) Start the game server in one terminal:

`$ python3 supervise.py 34.23.54.34 12345`

(ii) In another terminal, run the test:

`$ python3 test/test.py`

## Wish List
* Handle multiple checkers jumps in one turn 
* Write clients in different languages
* Improve the test suite
* Documentation

