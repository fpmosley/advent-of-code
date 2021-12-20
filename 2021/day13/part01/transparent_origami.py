#!/usr/bin/env python

'''
Advent of Code 2021 - Day 13: Transparent Origami (Part 1)
https://adventofcode.com/2021/day/13
'''

import re
import numpy as np


class Grid():
    def __init__(self, num_rows, num_cols) -> None:
        self._grid = np.full((num_rows, num_cols), '.')

    def add_dot(self, row, column):
        self._grid[row, column] = '#'

    def fold_up(self, unit):
        # Slice the grid to search below the fold
        search_area = self._grid[unit:, ]
        result = np.where(search_area == "#")

        coordinates = self.get_coordinates(result)
        new_coordinates = [(unit - row, col)
                           for row, col in coordinates]  # Translate the coordinates
        for row, col in new_coordinates:
            self._grid[row, col] = "#"

        # Delete below the fold
        self._grid = np.delete(self._grid, np.s_[unit:], 0)

    def fold_left(self, unit):
        # Slice the grid to search to the right of the fold
        search_area = self._grid[:, unit:]
        result = np.where(search_area == "#")

        coordinates = self.get_coordinates(result)
        new_coordinates = [(row, unit - col)
                           for row, col in coordinates]  # Translate the coordinates
        for row, col in new_coordinates:
            self._grid[row, col] = "#"

        # Delete to the right of the fold
        self._grid = np.delete(self._grid, np.s_[unit:], 1)

    def search_grid(self, value):
        result = np.where(self._grid == value)
        coordinates = self.get_coordinates(result)
        return coordinates

    @staticmethod
    def get_coordinates(result):
        return list(zip(result[0], result[1]))

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            for elem in row:
                output = output + f"{elem:>2}"
            output = output + "\n"
        return output


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:
            rows = []
            columns = []
            instructions = []
            read_instructions = False

            # Create match pattern
            pattern = r'^fold along (?P<direction>[xy])=(?P<unit>\d+)'

            # Read the coordinates and instructions
            for line in file:
                line = line.strip()
                if not line:
                    read_instructions = True
                    continue

                if read_instructions:
                    matches = re.match(pattern, line)
                    if matches:
                        direction = matches.group('direction')
                        unit = int(matches.group('unit'))
                        instructions.append((direction, unit))
                        continue

                col, row = line.split(',')
                columns.append(int(col))
                rows.append(int(row))

        # Initialize the grid
        num_rows = max(rows) + 1  # Zero-based index
        num_cols = max(columns) + 1  # Zero-based index
        transparency_paper = Grid(num_rows=num_rows, num_cols=num_cols)
        coordinates = list(zip(rows, columns))
        for row, column in coordinates:
            transparency_paper.add_dot(row=row, column=column)

        print()
        print(transparency_paper)

        # Process the first instruction
        direction, unit = instructions.pop(0)
        if direction == 'y':
            transparency_paper.fold_up(unit)
        else:
            transparency_paper.fold_left(unit)

        print(
            f"After folding {'up' if direction == 'y' else 'left'} at {direction}={unit}")
        print(transparency_paper)

        result = transparency_paper.search_grid('#')
        print(f"Number of visible dots: {len(result)}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
