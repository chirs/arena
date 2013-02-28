#ifndef CLIENT_H
#define CLIENT_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

#define MAXARGS                      3
#define BUFSIZE                      100
#define GETADDRINFO_SUCCESS          0 
#define CONNECTION_ATTEMPT_FAILURE  -1
#define SOCKET_FAILURE              -1
#define CONNECTION_FAILURE          -1

void print_usage( );
void client_init_hints( struct addrinfo *sa );
void *get_in_addr( struct sockaddr *sa );
int connection_attempt( const char *hostname, const char *port );

#endif

