# Arena

A game server for staging turn-based, 1-vs-1 match between AI players.

Uses a server/client framework using TCP sockets so AI players can be written in any language.

## Quick start

In one terminal, launch the server, host and port:

`$ python3 supervise.py some.host.here 12345`

In another terminal, connect with player 1:

`$ python3 clients/python/checkers.py some.host.here 12345`

In another terminal, connect with player 2:

`$ python3 clients/python/checkers.py some.host.here 12345`

After both clients connect, a game will be played without further human interference.


## API

This section covers the API calls a client needs to handle. Here's a sketch of the communications
between the client (a.k.a. AI player) and the server:

<pre>
                              CONNECTION
  Client                                                       Server
    |                                                             |
    |                                                             |
    |                     {game:"tictactoe"}                      |
    |  ------------------------------------------------------&gt;&gt;&gt;  |
    |                                                             |
    |                                                             |
    |            {game:"tictactoe", player:2, timelimit:5}        |
    |  &lt;&lt;&lt;------------------------------------------------------  |
    |                                                             |
    |                                                             |
    |       {token:"a8bdT%d#", board:"  x      ", result: 0}      |
    |  &lt;&lt;&lt;------------------------------------------------------  |
    |                                                             |
    |                                                             |
    |                {token:"ae8bdT%kd#", move:4}                 |
    |  ------------------------------------------------------&gt;&gt;&gt;  |
    |                                                             |
    |                                                             |
    |       {token:"45&d$X3f", board:" xx o    ", result:0}       |
    |  &lt;&lt;&lt;------------------------------------------------------  |
    |                                                             |
    |                                                             |
    |                {token:"45&d$X3f", move:3}                   |
    |  ------------------------------------------------------&gt;&gt;&gt;  |
    |                                                             |
    |                                                             |
    |       {token:"$asDF@7G", board:"xxxoo    ", result:1,       |
    |      history:"24130", log:"Player 1 made an illegal move."} |
    |  &lt;&lt;&lt;------------------------------------------------------  |
    |                                                             |
    |                                                             |
                            DISCONNECTION

</pre>

A game consists of five steps:

(i) The AI client connects to a game server at a given host and port.

(ii) The AI client sends a string encapsulating a JSON object (henceforth the "request"). This request specify a game type with the field "game" (see [Supported Games section](#games)). E.g.: `{game:"checkers"}`

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

An example acknowledgement would be `{name:"tictactoe", player:2, timelimit:5}`.

(iv) The server sends a string encapsulating a JSON object (henceforth the "game state"). This game state has the following fields:
<table>
  <tr>
    <th>Field name</th><th>Details</th>
  </tr>
  <tr>
    <td>token</td><td>A cryptic token needed to return a valid move</td>
  </tr>
  <tr>
    <td>board</td><td>board representation (see [supported games section](#games)</td>
  </tr>
  <tr>
    <td>result</td><td>-1 is tie, 0 is game ongoing, 1 is player 1 wins, 2 is player 2 wins</td>
  </tr>
  <tr>
    <td>history*</td><td>A list holding the sequence of moves done in the game</td>
  </tr>
  <tr>
    <td>log*</td><td>A log of miscellaneous relevant info about the game</td>
  </tr>
</table>

* The `history` and `log` fields are only send when the game is over (i.e. result != 0). An example of game state would be `{token: "g$jhe%j&", player:2, board:"xoxoxo   ", result:0}`.

(v) The AI player sends the server a move inside a json. Refer to [supported games section](#games) for the representation of moves key-value for the different games. A move json has the following elements:
<table>
  <tr>
    <th>Field name</th><th>Details</th>
  </tr>
  <tr>
    <td>token</td><td>The cryptic token receive previously</td>
  </tr>
  <tr>
    <td>move</td><td>see [supported games section](#games)</td>
  </tr>
</table>
An example of move json would be `{token: "g$jhe%j&", move:[1,9]}`

Steps (iv) and (v) are repeated until the game is over.

## Supported Games <a id=games></a>

<table>
  <tr>
    <th>Name</th><th>Board representation</th><th>Move representation</th>
  </tr>
  <tr>
    <td>checkers (English draughts)</td>
    <td>A 64 char-long string. Char position runs from left to right, top to bottom (e.g. position 10 represents the third square from the left in the second row from the top). Spaces (' ') represent empty squares, 'b' represents a player 1 pawn, 'B' represents a player 1 king. 'r' and 'R' are the same for player 2.</td>
    <td>A list of integers holding a piece's starting position and the visited squares (e.g. [1,10] or [24, 42, 60, 45] (multiple captures)).</td>
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

## Test Suite

To run the test suite:

(i) Start the game server on a host and port in one terminal:

`$ python3 supervise.py localhost 12345`

(ii) In another terminal, start the test suite on the same host and port:

`$ python3 test/test.py localhost 12345`

## Wish List
* Fix commented out connect four tests cases in test suite

