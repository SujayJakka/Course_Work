# COMP 3500: Project 5 Scheduling
# Sujay Jakka
# Version 1.0  11/28/2023

CC = gcc
CFLAGS = -std=c99 -g
OBJ = open.o read.o print.o

scheduler: $(OBJ) scheduler.c
	@echo "Creating the scheduler ..."
	$(CC) -o $@ $^ $(CFLAGS)

%.o: %.c %.h
	@echo "Creating object files ..."
	$(CC) -c $< -o $@

clean:
	@echo "Deleting object and binary files ..."
	rm -rvf *.o scheduler
