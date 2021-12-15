#!/usr/bin/env python

'''
Advent of Code 2021 - Day 9: Smoke Basin (Part 2)
https://adventofcode.com/2021/day/9
'''

import numpy as np


class HeightMap():
    def __init__(self) -> None:
        self._grid = np.array([])

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def find_low_points(self, radius=1):
        low_points = {}
        for coordinates, point in np.ndenumerate(self._grid):
            neighbor_points = self._neighbors(radius, coordinates=coordinates)

            if point < min(neighbor_points.values()):
                low_points[coordinates] = point

        return low_points

    def find_basins(self, radius=1, low_points=None):
        basins = []

        if not low_points:
            return basins

        for coordinates, value in low_points.items():
            basin = {
                coordinates: value
            }
            basin = self._basin(radius, coordinates=coordinates,
                                basin=basin, checked=[(coordinates)])
            basins.append(basin)

        return basins

    def _basin(self, radius, coordinates=(0, 0), basin=None, checked=None):

        neighbors = self._neighbors(radius, coordinates=coordinates)
        for neighbor_coordinates, _ in neighbors.items():
            row = neighbor_coordinates[0]
            col = neighbor_coordinates[1]
            if neighbor_coordinates in checked:
                continue

            if not checked:
                checked = []

            checked.append(neighbor_coordinates)
            if self._grid[row, col] != 9:
                basin[row, col] = self._grid[row, col]
                self._basin(1, coordinates=(row, col),
                            basin=basin, checked=checked)

        return basin

    # Searches for horizontal and vertical adjacent neighors
    def _neighbors(self, radius, coordinates=(0, 0)):
        neighbors = {}
        row = coordinates[0]
        column = coordinates[1]

        # Get UP neighbor value
        if row >= 1:
            neighbors[(row - radius, column)] = self._grid[row - radius, column]

        # Get LEFT neighbor value
        if column >= 1:
            neighbors[(row, column - radius)] = self._grid[row, column - radius]

        # Get RIGHT neighbor value
        if column < len(self._grid[0]) - 1:
            neighbors[(row, column + radius)] = self._grid[row, column + radius]

        # Get DOWN neighbor value
        if row < len(self._grid) - 1:
            neighbors[(row + radius, column)] = self._grid[row + radius, column]

        return neighbors

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            for elem in row:
                output = output + f"{elem:>3}"
            output = output + "\n"
        return output


def calculate_risk(heights):
    # Risk is 1 plus the height
    return sum([height + 1 for height in heights])


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            # Create a new board
            area = HeightMap()

            # Read the rows and setup the HeightMap
            for line in file:
                line = line.strip()

                input_row = [int(x) for x in str(line)]
                area.add_row(input_row)

            print("The input grid: ")
            print(area)
            low_points = area.find_low_points()
            basins = area.find_basins(low_points=low_points)

            # Find the 3 largest basins and multiply
            basin_sizes = [len(basin) for basin in basins]
            basin_sizes.sort()
            three_largest = np.prod(basin_sizes[-3:])

            print(
                f"The product of the three largest basins {basin_sizes[-3:]}: {three_largest}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
