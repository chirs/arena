spartacus is a `node.js` client for [arena][arena-repo].

``` javascript
var spart = require('spartacus');

spart.connect('0.0.0.0','4000','checkers');

spart.on('start', function( ack ){
	// game has started, ack === { name, player, timelimit }
});

spart.on('move', function( gamestate ){
	// your AI makes a move
	var move = 4;
	spart.move( move );
});

spart.on('gameover', function( gamestate ){
	// post-game
	spart.disconnect();
	process.exit();
});

// access the socket connection directly
spart.socket.write('something else');
```

[arena-repo]: https://github.com/chirs/arena