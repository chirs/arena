// Spartacus: node.js socket client for arena: https://github.com/chirs/arena
// By Daniel Mendel Espeset http://github.com/danielmendel
// Never Graduate

/**
 * Utilities
 */

// logger
function log(){ console.log.apply( console, arguments ); };
// convert obj to JSON and wrap in a string
function stringify(obj){ return JSON.stringify(obj); };

log('booting spartacus');

/**
 * Modules
 */

var net    = require('net')
  , util   = require('util')
  , events = require('events')
  , socket = new net.Socket()
  , spart  = new events.EventEmitter()
  ;

// handle arena events
socket.on('data', function route( data ){
    // every so often the socket gives us double data, this should handle that gracefully.
    var jsonStr = data.toString();
    var multipleMessages = jsonStr.match(/}\n?{/);
    if( multipleMessages ){
      route( jsonStr.substr(0,multipleMessages.index+1) );
      jsonStr = jsonStr.substr(multipleMessages.index+1, jsonStr.length);
    }
    var gamestate = JSON.parse( jsonStr );
    if( gamestate.hasOwnProperty('timelimit') )
        return spart.emit('start', gamestate);
    if( gamestate.hasOwnProperty('result') && gamestate.result !== 0 )
        return spart.emit('gameover', gamestate);
    return spart.emit('move', gamestate);
});

// connect to arena server & start game
spart.connect = function( HOST, PORT, game ){
    log('connecting to '+HOST+':'+PORT);
    socket.connect(PORT, HOST, function(){
        log('connected to arena server '+HOST+':'+PORT);
        log('requesting game of '+game);
        socket.write( stringify({ game: game }) );
    });
};

// disconnect from arena server
spart.disconnect = socket.end;

// handle move tokens behind the scenes
var move_token;
spart.on('move', function( gamestate ){
    move_token = gamestate.token;
});
// make a move
spart.move = function( move ){
    socket.write( stringify({ token: move_token, move: move }) );
}

// expose the socket connection
spart.socket = socket;

// export spartacus
module.exports = spart;
