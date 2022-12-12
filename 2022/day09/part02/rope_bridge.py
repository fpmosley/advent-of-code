#!/usr/bin/env python

'''
Advent of Code 2022 - Day 9: Rope Bridge (Part 2)
https://adventofcode.com/2022/day/9
'''

from enum import Enum
import time
import numpy as np
from typing import Tuple
from collections import OrderedDict


class DIRECTION(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Grid:
    def __init__(self, num_rows, num_cols) -> None:
        self._grid = np.full((num_rows, num_cols), '.')

    def mark_map(self, row, column, symbol):
        self._grid[row, column] = symbol

    def __str__(self) -> str:
        output = ""
        for row in self._grid[::-1]:
            for elem in row:
                output = output + f"{elem:>2}"
            output = output + "\n"
        return output

class Knot:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
    
    @property
    def position(self):
        return self.x, self.y

class Head(Knot):
    def step(self, direction):
        # move 1 step in the direction
        match direction:
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1
            case 'L':
                self.x -= 1
            case 'R':
                self.x += 1

class Tail(Knot):
    def __init__(self):
        super().__init__()
        self.visited = set()
    
    def follow(self, position):
        x, y = position

        dist_x = x - self.x
        dist_y = y - self.y
        if abs(dist_x) == 2 and not dist_y: # horizontal
            xv = 1 if dist_x > 0 else -1
            self.x += xv
        elif abs(dist_y) == 2 and not dist_x: # vertical
            yv = 1 if dist_y > 0 else -1
            self.y += yv
        elif (abs(dist_y) == 2 and abs(dist_x) in (1, 2)) or (abs(dist_x) == 2 and abs(dist_y) in (1, 2)):
            xv = 1 if dist_x > 0 else -1
            self.x += xv
            yv = 1 if dist_y > 0 else -1
            self.y += yv
        self.visited.add((self.x, self.y))


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            head = Head()
            tails = [Tail() for _ in range(9)]
            #knot_map = Grid(100, 100)
            #print(knot_map)

            # Read the motions and move the knots
            for line in file:
                line = line.strip()
                #print('-' * 20)
                #print(line)
                direction, steps = line.split()
                steps = int(steps)

                for _ in range(steps):
                    # col, row = head.position
                    # knot_map.mark_map(row, col, '.')
                    head.step(direction)
                    col, row = head.position
                    # knot_map.mark_map(row, col, 'H')

                    # col, row = tails[0].position 
                    # knot_map.mark_map(row, col, '.')
                    tails[0].follow(head.position)
                    # col, row = tails[0].position 
                    # knot_map.mark_map(row, col, '1')

                    for i in range(1, 9):
                        # col, row = tails[i].position
                        # knot_map.mark_map(row, col, '.')
                        tails[i].follow(tails[i - 1].position)
                        # col, row = tails[i].position
                        # knot_map.mark_map(row, col, i + 1)
                # print(knot_map)

        end = time.time()
        print(f"Number of tail rope positions visited: {len(tails[8].visited)}")
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
