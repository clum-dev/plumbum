CFLAGS=-Wall -Werror -pedantic -std=gnu99 -g
.PHONY=all clean
.DEFAULT_GOAL:=all

OBJS_parser=parser.c clum-lib/file.o clum-lib/strings.o clum-lib/arr.o clum-lib/node.o clum-lib/list.o clum-lib/sha1.o clum-lib/dict.o clum-lib/pipe.o clum-lib/util.o token.o

all: parser

parser: $(OBJS_parser)
	gcc $(CFLAGS) $(OBJS_parser) -o parser

clum-lib/file.o: clum-lib/file.c clum-lib/file.h
	gcc $(CFLAGS) -o clum-lib/file.o -c clum-lib/file.c

clum-lib/strings.o: clum-lib/strings.c clum-lib/strings.h
	gcc $(CFLAGS) -o clum-lib/strings.o -c clum-lib/strings.c

clum-lib/arr.o: clum-lib/arr.c clum-lib/arr.h
	gcc $(CFLAGS) -o clum-lib/arr.o -c clum-lib/arr.c

clum-lib/node.o: clum-lib/node.c clum-lib/node.h
	gcc $(CFLAGS) -o clum-lib/node.o -c clum-lib/node.c

clum-lib/list.o: clum-lib/list.c clum-lib/list.h
	gcc $(CFLAGS) -o clum-lib/list.o -c clum-lib/list.c

clum-lib/sha1.o: clum-lib/sha1.c clum-lib/sha1.h
	gcc $(CFLAGS) -o clum-lib/sha1.o -c clum-lib/sha1.c

clum-lib/dict.o: clum-lib/dict.c clum-lib/dict.h
	gcc $(CFLAGS) -o clum-lib/dict.o -c clum-lib/dict.c

clum-lib/pipe.o: clum-lib/pipe.c clum-lib/pipe.h
	gcc $(CFLAGS) -o clum-lib/pipe.o -c clum-lib/pipe.c

clum-lib/util.o: clum-lib/util.c clum-lib/util.h
	gcc $(CFLAGS) -o clum-lib/util.o -c clum-lib/util.c

token.o: token.c token.h
	gcc $(CFLAGS) -o token.o -c token.c


clean:
	rm -f parser
	rm -f clum-lib/file.o
	rm -f clum-lib/strings.o
	rm -f clum-lib/arr.o
	rm -f clum-lib/node.o
	rm -f clum-lib/list.o
	rm -f clum-lib/sha1.o
	rm -f clum-lib/dict.o
	rm -f clum-lib/pipe.o
	rm -f clum-lib/util.o
	rm -f token.o
