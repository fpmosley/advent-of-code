#!/usr/bin/env python

'''
Advent of Code 2023 - Day 3: Gear Ratios (Part 1)
https://adventofcode.com/2023/day/3
'''


import time
import numpy as np
import re


class EngineSchematic():
    def __init__(self) -> None:
        self._grid = np.array([])
        self._part_nums = []

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def _is_number(self, row, col):
        value = self._grid[(row, col)]
        return value if value.isdigit() else None

    def _search(self, row, col):
        num_string = ''
        value = self._is_number(row=row, col=col)
        if value:
            num_string += value  # add the value to the num string

            # Search left in row
            y = col
            while True:
                y -= 1
                if y < 0:
                    break  # Outside the left boundary

                value = self._is_number(row=row, col=y)
                if value:
                    num_string += value  # add value to the number string
                else:
                    break

            num_string = num_string[::-1]  # reverse the string

            # Search right in row
            y = col
            while True:
                y += 1
                if y >= len(self._grid[0]):
                    break  # Outside the right boundary

                value = self._is_number(row=row, col=y)
                if value:
                    num_string += value  # add the value to the number string
                else:
                    break

        return int(num_string) if num_string else None

    def find_part_numbers(self) -> list:
        part_numbers = []
        coordinates = self._find_symbols()  # Part numbers surround symbols
        for row, col in coordinates:
            # Search left
            if col > 0:
                part_number = self._search(row, col - 1)
                if part_number:
                    part_numbers.append(part_number)

            # Search right
            if col < (len(self._grid[0]) - 1):
                part_number = self._search(row, col + 1)
                if part_number:
                    part_numbers.append(part_number)

            # Search up
            if row > 0:
                part_number = self._search(row - 1, col)
                if part_number:
                    part_numbers.append(part_number)
                else:
                    # Search up and left
                    if col > 0:
                        part_number = self._search(row - 1, col - 1)
                        if part_number:
                            part_numbers.append(part_number)

                    # Search up and right
                    if col < (len(self._grid[0]) - 1):
                        part_number = self._search(row - 1, col + 1)
                        if part_number:
                            part_numbers.append(part_number)

            # Search down
            if row < (len(self._grid) - 1):
                part_number = self._search(row + 1, col)
                if part_number:
                    part_numbers.append(part_number)
                else:
                    # Search down and left
                    if col > 0:
                        part_number = self._search(row + 1, col - 1)
                        if part_number:
                            part_numbers.append(part_number)

                    # Search down and right
                    if col < (len(self._grid[0]) - 1):
                        part_number = self._search(row + 1, col + 1)
                        if part_number:
                            part_numbers.append(part_number)

        return part_numbers

    def _neighbors(self, radius, coordinates=(0, 0)):  # Includes the center coordinates
        neighbors = []
        row = coordinates[0]
        column = coordinates[1]

        for j in range(column - radius, column + radius + 1):
            for i in range(row - radius, row + radius + 1):
                if self._inbounds(row=i, column=j) and (i, j) != coordinates:
                    neighbors.append((i, j))

        # Sort so we can iterate from left to right and top to bottom
        return sorted(neighbors, key=lambda s: (s[0], s[1]))

    def _inbounds(self, row, column):
        return 0 <= row < len(self._grid) and 0 <= column < len(self._grid[0])

    def _find_symbols(self) -> list:
        result = np.where(self._grid == '#')
        return list(zip(result[0], result[1]))

    @property
    def size(self) -> tuple:
        return self._grid.shape

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            for elem in row:
                output = output + f"{elem:>3}"
            output = output + "\n"
        return output


def main():

    filename = input("What is the input file name? ")
    #filename = '/Users/franklin/Documents/GitHub/advent-of-code/2023/day03/part01/test.txt'

    try:
        with open(filename, "r") as file:

            start = time.time()
            engine_schematic = EngineSchematic()

            for line in file:
                line = line.strip()

                # Substitue all symbols to '#' to create an easier search condition
                line = re.sub("[^0-9.]", "#", line)
                engine_schematic.add_row([x for x in line]) # Split each string character into a list

        print(
            f"Sum of part numbers: {sum(engine_schematic.find_part_numbers())}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
