#!/usr/bin/env python

'''
Advent of Code 2021 - Day 9: Smoke Basin (Part 1)
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
        low_points = []
        for index, point in np.ndenumerate(self._grid):
            neighbor_points = self._neighbors(radius, coordinates=index)

            if point < min(neighbor_points):
                low_points.append(point)

        return low_points

    def _neighbors(self, radius, coordinates=(0, 0)):
        neighbors = []
        row = coordinates[0]
        column = coordinates[1]

        # Get UP neighbor value
        if row >= 1:
            neighbors.append(self._grid[row - radius, column])

        # Get LEFT neighbor value
        if column >= 1:
            neighbors.append(self._grid[row, column - radius])

        # Get RIGHT neighbor value
        if column < len(self._grid[0]) - radius:
            neighbors.append(self._grid[row, column + radius])

        # Get DOWN neighbor value
        if row < len(self._grid) - radius:
            neighbors.append(self._grid[row + radius, column])

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
            sum_risk_levels = calculate_risk(
                low_points) if low_points else None

            if sum_risk_levels:
                low_points_str = [str(point) for point in low_points]
                print(f"Number of low points: {len(low_points)}")
                print(f"Low points: {', '.join(low_points_str)}")
                print(
                    f"\nThe sum of the risk levels of all low points is: {sum_risk_levels}\n")
            else:
                print("The sum of the risk levels of all low points not found.\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
