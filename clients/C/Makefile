CFLAGS=-Wall -g -DNDEBUG

all: client

client:	client.o
	gcc json.c client.o -lm -o client
clean:
	rm -f client.o client

