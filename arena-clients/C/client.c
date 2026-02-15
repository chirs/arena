#include "json.h"
#include "inc/client.h"

void print_usage( ) {
    fprintf( stderr, "usage: client hostname portnumber\n" );
}

// get sockaddr, IPv4 or IPv6
void *get_in_addr( struct sockaddr *sa ) {
    if ( sa->sa_family == AF_INET ) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int connection_attempt(  const char *hostname, const char *port ) {
    struct addrinfo hints;
    struct addrinfo *p         = NULL;
    struct addrinfo *pservinfo = NULL;
    int             sockfd;
    int             result;
    char            dst[INET6_ADDRSTRLEN] = { '\0' };
     
    memset( &hints, 0, sizeof( hints ) );
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    result = getaddrinfo( hostname, port, &hints, &pservinfo );
    if ( result != GETADDRINFO_SUCCESS ) {
        fprintf( stderr, "getaddrinfo: %s\n", gai_strerror( result ) );
        return CONNECTION_ATTEMPT_FAILURE;
     }

    for ( p = pservinfo; p != NULL; p = p->ai_next ) {
        sockfd = socket( p->ai_family, p->ai_socktype, p->ai_protocol );
        if ( sockfd == SOCKET_FAILURE ) {
            perror( "client: socket" );
            continue;
        }

        result = connect( sockfd, p->ai_addr, p->ai_addrlen );
        if ( result == CONNECTION_FAILURE ) {
            close( sockfd );
            perror( "client: connect" );
            continue;
        }

        break;
    }

    if ( p == NULL ) {
        return CONNECTION_ATTEMPT_FAILURE; 
    } 

    inet_ntop(p->ai_family,
              get_in_addr( (struct sockaddr *)p->ai_addr ), 
              dst, 
              sizeof( dst ) );

    printf( "client: connecting to host %s, port %s\n", dst, port);
    freeaddrinfo( pservinfo );

     return sockfd;
}

int main( int argc, char *argv[] ) {
    char const      *hostname  = NULL;
    char const      *port      = NULL;
    int             sockfd     = -1;
    char            *buf       = NULL;
    char            ttt[BUFSIZE] = "{\"game\":\"tictactoe\"}";

    if ( argc < MAXARGS ) {
        print_usage( );
        exit( EXIT_FAILURE );
    }
    
    hostname = argv[1];
    port = argv[2];

    buf = (char *)malloc( sizeof( char ) * BUFSIZE );
    memset( buf, 0, sizeof( char ) * BUFSIZE );

    sockfd = connection_attempt( hostname, port );
    if ( sockfd == CONNECTION_ATTEMPT_FAILURE ) {
        fprintf( stderr, "client: failed to connect\n" );
        exit( EXIT_FAILURE );
    }

    send( sockfd, ttt, strlen( ttt ), 0 );
    
    recv( sockfd, buf, BUFSIZE, 0 );
    
    printf( "Received: %s\n", buf );

    close( sockfd );
    free( buf );

    return 0;
}

