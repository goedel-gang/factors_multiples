TARGET = crack
LIBS = -lm
CC = gcc
CFLAGS = -Wall -pedantic

debug: CFLAGS += -DDEBUG -g
deboptimise: CFLAGS += -DDEBUG -g -O3
optimise: CFLAGS += -O3

.PHONY: default all clean debug optimise deboptimise

default: $(TARGET)
all: default
debug: all
optimise: all
deboptimise: all

OBJECTS = $(patsubst %.c, %.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TARGET) $(OBJECTS)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $@

clean:
	rm -f *.o
	rm -f $(TARGET)
