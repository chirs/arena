var client = require('spartacus')
  , player = 0
  , timeout = 0
;

client.connect('0.0.0.0','4000','tictactoe');

client.on('start', function( acknowledgement ){
    player  = acknowledgement.player;
    timeout = acknowledgement.timeout;
});

client.on('move', function( gamestate ){
    do var move = Math.round(Math.random() * 8)
    while( gamestate.board[move] !== ' ')
    client.move( move );
});

client.on('gameover', function( gamestate ){
    client.disconnect();
    process.exit();
});

