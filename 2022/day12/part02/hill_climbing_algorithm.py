#!/usr/bin/env python

'''
Advent of Code 2022 - Day 12: Hill Climbing Algorithm (Part 2)
https://adventofcode.com/2022/day/12

Reference: Breadth-First Search (using since it's an unweighted graph)
https://en.wikipedia.org/wiki/Breadth-first_search
'''

import time
from typing import List
import numpy as np
from collections import deque


class HeightMap():
    def __init__(self) -> None:
        self._grid = np.array([])

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def mark_map(self, x: int, y: int, marker: str) -> None:
        self._grid[(x, y)] = marker

    def _find_height_difference(self, current_height: str, neighbor_height: str) -> int:
        current_height = 'a' if current_height == 'S' else current_height
        current_height = 'z' if current_height == 'E' else current_height
        neighbor_height = 'a' if neighbor_height == 'S' else neighbor_height
        neighbor_height = 'z' if neighbor_height == 'E' else neighbor_height
        return ord(neighbor_height) - ord(current_height)

    def find_marker(self, marker: str) -> list:
        """Find the given marker in the grid"""
        result = np.where(self._grid == marker)
        return list(zip(result[0], result[1]))

    def find_shortest_path(self, start=(0, 0, 0)) -> int:
        """Find the shortest path using a breadth-first search"""
        queue = deque([start])
        visited = set()

        while queue:
            x, y, distance = queue.popleft()

            if self._grid[(x, y)] == 'E':
                # Reached the end of the path ('E').
                return distance

            # Who Da Neighbors (https://youtu.be/l37eskdhXeE)
            neighbors = self._neighbors(radius=1, coordinates=(x, y))

            for neighbor in neighbors:
                height_diff = self._find_height_difference(
                    current_height=self._grid[(x, y)], neighbor_height=self._grid[neighbor])
                if height_diff <= 1 and neighbor not in visited:  # Rule is the destination can be at most 1 higher
                    visited.add(neighbor)
                    queue.append((neighbor[0], neighbor[1], distance + 1))

    def _neighbors(self, radius, coordinates=None) -> List:
        """Searches for horizontal and vertical adjacent neighors"""

        neighbors = []

        if not coordinates:
            return neighbors

        row, column = coordinates

        # Get UP neighbor value
        if row >= 1:
            neighbors.append((row - radius, column))

        # Get LEFT neighbor value
        if column >= 1:
            neighbors.append((row, column - radius))

        # Get RIGHT neighbor value
        if column < len(self._grid[0]) - radius:
            neighbors.append((row, column + radius))

        # Get DOWN neighbor value
        if row < len(self._grid) - radius:
            neighbors.append((row + radius, column))

        return neighbors


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Create a new map
            height_map = HeightMap()

            # Read the rows and setup the map
            for line in file:
                line = line.strip()

                input_row = [x for x in str(line)]
                height_map.add_row(input_row)

            # Find the starting point and change to elevation 'a'
            coordinates = height_map.find_marker('S')
            x, y = coordinates[0]
            height_map.mark_map(x, y, 'a')

            # Find the lowest elevations
            coordinates = height_map.find_marker('a')

            # Find the paths from the lowest elevation(s)
            steps = []
            for x, y in coordinates:
                num_steps = height_map.find_shortest_path(start=(x, y, 0))
                if num_steps:
                    steps.append(num_steps)

            end = time.time()
            print(
                f"The fewest steps from the lowest elevation: {min(steps)}")
            print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
