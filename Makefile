LDLIBS=-lz
CFLAGS=-Iinclude

SRC=$(wildcard *.c)
OBJ=$(SRC:%.c=%.o)
BIN=jffs2extract

all: $(BIN)

$(BIN): $(OBJ)

test: $(BIN)
	python3 test.py

install: $(BIN)
	install -m 0755 jffs2extract /usr/bin

clean:
	$(RM) $(OBJ) $(BIN)

.PHONY: all test install clean
