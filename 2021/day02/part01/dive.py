#!/usr/bin/env python

'''
Advent of Code 2021 - Day 2: Dive!
https://adventofcode.com/2021/day/2
'''


class Submarine():
    def __init__(self) -> None:
        self._depth = 0
        self._position = 0

    def forward(self, units):
        self._position += units

    def down(self, units):
        self._depth += units

    def up(self, units):
        self._depth -= units

    @property
    def depth(self):
        return self._depth

    @property
    def position(self):
        return self._position

    def __str__(self) -> str:
        return f"Submarine has position '{self._position}' and depth '{self._depth}'"


filename = input("What is the input file name? ")


sub = Submarine()

try:
    with open(filename, "r") as file:
        for line in file:
            instruction = line.strip()
            print(instruction)
            command, units = instruction.split(" ")
            if command == 'forward':
                sub.forward(int(units))
            elif command == 'down':
                sub.down(int(units))
            elif command == 'up':
                sub.up(int(units))
            else:
                print(f"Invalid command entered: {command}")
    print(sub)
    print(f"Multiplication answer: {sub.position * sub.depth}")
except FileNotFoundError:
    print(f"No such file or directory: '{filename}'")
