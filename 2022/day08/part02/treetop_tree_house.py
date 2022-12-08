#!/usr/bin/env python

'''
Advent of Code 2022 - Day 8: Treetop Tree House (Part 2)
https://adventofcode.com/2022/day/8
'''

import time
import numpy as np

SCENIC_SCORES = {}


class HeightMap():
    def __init__(self) -> None:
        self._grid = np.array([])

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def _visible_up(self, row=0, col=0, height=0):
        for i in range(row - 1, -1, -1):
            if self._grid[i, col] >= height:
                return False
        return True

    def _visible_down(self, row=0, col=0, height=0):
        for i in range(row + 1, self._grid.shape[0]):
            if self._grid[i, col] >= height:
                return False
        return True

    def _visible_left(self, row=0, col=0, height=0):
        for j in range(col - 1, -1, -1):
            if self._grid[row, j] >= height:
                return False
        return True

    def _visible_right(self, row=0, col=0, height=0):
        for j in range(col + 1, self._grid.shape[1]):
            if self._grid[row, j] >= height:
                return False
        return True

    def check_visibility(self, coordinates=(0, 0)) -> int:
        """ Check the visibility of trees from outside.
            Only checking up, down, left, and right.
        """
        num_visible = 0
        row = coordinates[0]
        column = coordinates[1]
        num_rows, num_cols = self._grid.shape

        # Check only the interior trees
        for j in range(column, num_cols - 1):
            for i in range(row, num_rows - 1):
                height = self._grid[i, j]
                if self._visible_up(i, j, height):
                    num_visible += 1
                    continue
                if self._visible_down(i, j, height):
                    num_visible += 1
                    continue
                if self._visible_left(i, j, height):
                    num_visible += 1
                    continue
                if self._visible_right(i, j, height):
                    num_visible += 1
                    continue

        return num_visible + (self._grid.shape[1] * 2) + (self._grid.shape[0] - 2) * 2

    def _scenic_up(self, row=0, col=0, height=0) -> int:
        num_trees = 0
        for i in range(row - 1, -1, -1):
            num_trees += 1
            if self._grid[i, col] >= height:
                break
        return num_trees

    def _scenic_down(self, row=0, col=0, height=0) -> int:
        num_trees = 0
        for i in range(row + 1, self._grid.shape[0]):
            num_trees += 1
            if self._grid[i, col] >= height:
                break
        return num_trees

    def _scenic_left(self, row=0, col=0, height=0) -> int:
        num_trees = 0
        for j in range(col - 1, -1, -1):
            num_trees += 1
            if self._grid[row, j] >= height:
                break
        return num_trees

    def _scenic_right(self, row=0, col=0, height=0) -> int:
        num_trees = 0
        for j in range(col + 1, self._grid.shape[1]):
            num_trees += 1
            if self._grid[row, j] >= height:
                break
        return num_trees

    def check_scenic_score(self, coordinates=(0, 0)) -> int:
        """ Check the scenic score of interior trees.
            Only checking up, down, left, and right.
        """
        row = coordinates[0]
        column = coordinates[1]
        num_rows, num_cols = self._grid.shape

        # Check only the interior trees
        for j in range(column, num_cols - 1):
            for i in range(row, num_rows - 1):
                height = self._grid[i, j]
                num_scenic_up = self._scenic_up(i, j, height)
                num_scenic_down = self._scenic_down(i, j, height)
                num_scenic_left = self._scenic_left(i, j, height)
                num_scenic_right = self._scenic_right(i, j, height)

                SCENIC_SCORES[(i, j)] = num_scenic_up * \
                    num_scenic_down * num_scenic_left * num_scenic_right

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

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Create a new board
            tree_map = HeightMap()

            # Read the rows and setup the HeightMap
            for line in file:
                line = line.strip()

                input_row = [int(x) for x in str(line)]
                tree_map.add_row(input_row)

            print(f"Size of grid: {tree_map.size}")

            # Get the highest scenic score
            tree_map.check_scenic_score((1, 1))
            print(f"Highest scenic score: {max(SCENIC_SCORES.values())}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
