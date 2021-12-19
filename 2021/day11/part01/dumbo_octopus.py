#!/usr/bin/env python

'''
Advent of Code 2021 - Day 11: Dumbo Octopus (Part 1)
https://adventofcode.com/2021/day/11
'''

import numpy as np


class EnergyLevelGrid():
    def __init__(self) -> None:
        self._grid = np.array([])

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def simulate_step(self):
        # Increment the energy level by 1
        self.increment_grid(increment_by=1)

        # Find all octopuses where energy level > 9
        result = np.where(self._grid > 9)
        octopuses = self.get_coordinates(result)

        flashed = []
        for coordinates in octopuses:
            self._flash(coordinates=coordinates, flashed=flashed)

        for coordinates in flashed:
            self._grid[coordinates] = 0

        return len(flashed)

    def increment_grid(self, increment_by=0):
        increment_grid = np.full(self._grid.shape, increment_by)
        self._grid = self._grid + increment_grid

    def _flash(self, coordinates=(0, 0), flashed=None):

        if coordinates in flashed:
            return

        # Add the coordinates to list of flashed
        flashed.append(coordinates)

        # Who Da Neighbors (https://youtu.be/l37eskdhXeE)
        neighbors = self._neighbors(radius=1, coordinates=coordinates)

        # Increment the neighbors, if not already flashed
        for neighbor in neighbors:
            self._grid[neighbor] += 1 if neighbor not in flashed else 0
            if self._grid[neighbor] > 9 and neighbor not in flashed:
                self._flash(coordinates=neighbor, flashed=flashed)

    # Searches for horizontal, vertical, and diagonal adjacent neighors

    def _neighbors(self, radius, coordinates=(0, 0)):
        neighbors = []
        row = coordinates[0]
        column = coordinates[1]

        for j in range(column - radius, column + radius + 1):
            for i in range(row - radius, row + radius + 1):
                if self._inbounds(row=i, column=j) and (i, j) != coordinates:
                    neighbors.append((i, j))

        return neighbors

    def _inbounds(self, row, column):
        return True if row >= 0 and row < len(self._grid) and column >= 0 and column < len(self._grid[0]) else False

    @staticmethod
    def get_coordinates(result):
        return list(zip(result[0], result[1]))

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
        steps = int(input("How many steps to simulate? "))

        with open(filename, "r") as file:

            # Create a new grid
            grid = EnergyLevelGrid()

            # Read the rows and setup the HeightMap
            for line in file:
                line = line.strip()

                input_row = [int(x) for x in str(line)]
                grid.add_row(input_row)

            print("The input grid: ")
            print(grid)
            total_num_of_flashes = 0
            for step in range(steps):
                # Flash the grid
                num_of_flashes = grid.simulate_step()
                print()
                print(grid)
                total_num_of_flashes += num_of_flashes
                print(
                    f"Number of flashes for step {step + 1}: {total_num_of_flashes}")

            print(
                f"\nThe total number of flashes for {steps} steps: {total_num_of_flashes}")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError:
        print("Please enter a valid integer.")


if __name__ == "__main__":
    main()
