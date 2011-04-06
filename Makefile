CC = gcc
CFLAGS = -Wall
LDFLAGS = -ltdb

all: popcorn-server popcorn-dump

popcorn-server: popcorn-server.o
	$(CC) $(LDFLAGS) $< -o $@

popcorn-dump: popcorn-dump.o
	$(CC) $(LDFLAGS) $< -o $@

example:
	./popcorn-client > example.txt

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o popcorn-server popcorn-dump example.txt popcorn.tar.bz2
	rm -rf dist

dist:
	mkdir dist
	tar --transform 's:^:popcorn/:' -j -c -f dist/popcorn.tar.bz2 [^d]*
	cp -a *spec dist