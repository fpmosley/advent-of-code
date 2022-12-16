#!/usr/bin/env python

'''
Advent of Code 2022 - Day 14: Regolith Reservoir (Part 2)
https://adventofcode.com/2022/day/14

Solution makes use of recursion to drop the sand.
'''

import time
import numpy as np
import re


class PathMap():
    def __init__(self) -> None:
        self._grid = np.full((400, 800), '.')  # 200 x 600 grid with air ('.')
        self._position = (0, 0)
        self._sand_units = 0
        self._floor = 0

    def _draw_horizontal(self, a: tuple, b: tuple) -> None:
        horizontal_pos = a[1]
        assert horizontal_pos == b[1]

        # Check if drawing line right or left. Cols increase going right on the grid.
        horiz_range = range(
            a[0], b[0] - 1, -1) if a[0] > b[0] else range(a[0], b[0] + 1)
        for col in horiz_range:
            self._grid[horizontal_pos, col] = '#'

    def _draw_vertical(self, a: tuple, b: tuple) -> None:
        vertical_pos = a[0]
        assert vertical_pos == b[0]

        # Check if drawing line down or up. Rows increase going down the grid.
        vert_range = range(
            a[1], b[1] - 1, -1) if a[1] > b[1] else range(a[1], b[1] + 1)
        for row in vert_range:
            self._floor = row + 2 if row + 2 > self._floor else self._floor
            self._grid[row, vertical_pos] = '#'

    def draw_floor(self) -> None:
        rows, cols = self._grid.shape
        for i in range(cols):
            self._grid[self._floor, i] = '#'

    def draw(self, a: tuple, b: tuple) -> None:
        """Draw a horizontal or vertical line from point a to b"""
        if a[0] == b[0]:
            self._draw_vertical(a=a, b=b)
        else:
            self._draw_horizontal(a=a, b=b)

    def in_abyss(self, coordinate: tuple) -> bool:
        y, x = coordinate
        values = self._grid[x:, y]
        if 'o' in values or '#' in values:
            return False
        return True

    def drop_sand(self, start: tuple) -> bool:
        "Drop sand from starting location. Return False when flowing into abyss."
        y, x = start

        if self._grid[x, y] == 'o':  # Check if we have sand at the starting point
            return False

        # Drop the sand
        if self._grid[x + 1, y] == '.':  # Check down one step
            x = x + 1
            if self.in_abyss(coordinate=(y, x)):
                return False
            return self.drop_sand((y, x))
        elif self._grid[x + 1, y - 1] == '.':  # Check down and to the left
            x = x + 1
            y = y - 1
            if self.in_abyss(coordinate=(y, x)):
                return False
            return self.drop_sand((y, x))
        elif self._grid[x + 1, y + 1] == '.':  # Check down and to the right
            x = x + 1
            y = y + 1
            if self.in_abyss(coordinate=(y, x)):
                return False
            return self.drop_sand((y, x))
        else:
            self._grid[x, y] = 'o'
            self._sand_units += 1
            return True

    @property
    def sand(self) -> int:
        return self._sand_units

    @property
    def floor(self) -> int:
        return self._floor

    @floor.setter
    def floor(self, floor):
        self._floor = floor

    def __str__(self) -> str:
        output = ""
        for row in self._grid[:150]:
            for elem in row[450:550]:
                output = output + f"{elem}"
            output = output + "\n"
        return output


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Create a new board
            path_map = PathMap()

            # Read the rows and setup the HeightMap
            for line in file:
                line = line.strip()

                # Find all the points in the input line
                result = re.findall(r"(\d+,\d+)", line)
                if result:
                    # Create a list of points (tuples)
                    path = [eval(x) for x in result]
                    for i in range(1, len(path)):
                        path_map.draw(a=path[i - 1], b=path[i])

            # Draw the floor
            path_map.draw_floor()

            while True:
                if not path_map.drop_sand(start=(500, 0)):
                    break

            print(path_map)

        end = time.time()
        print(f"Units of sand at rest: {path_map.sand}")
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
