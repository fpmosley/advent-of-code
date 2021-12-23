#!/usr/bin/env python

'''
Advent of Code 2021 - Day 15: Chiton (Part 2)
https://adventofcode.com/2021/day/15

Reference: Dijksta's Algorithm
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
'''

import heapq
import math
import time
from typing import List
import numpy as np


class ChitonMap():
    def __init__(self) -> None:
        self._grid = np.array([])
        self._path = []

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def find_shortest_path(self, start=(0, 0)):
        # Create grid of distances
        distances = np.full(self._grid.shape, math.inf)
        distances[start] = 0
        queue = []
        heapq.heappush(queue, (0, start))

        while True:
            _, coordinates = heapq.heappop(queue)
            self._path.append(coordinates)
            cost = distances[coordinates]

            rows, cols = self._grid.shape
            if coordinates == (rows - 1, cols - 1):
                # Reached the end of the path (lower right).
                return cost

             # Who Da Neighbors (https://youtu.be/l37eskdhXeE)
            neighbors = self._neighbors(radius=1, coordinates=coordinates)

            for neighbor in neighbors:
                distance = cost + self._grid[neighbor]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

    # Searches for horizontal and vertical adjacent neighors
    def _neighbors(self, radius, coordinates=None) -> List:
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
            # Create a new map
            chiton_map = ChitonMap()

            # Read the rows and setup the map. Scale input 5 times in each dimension
            lines = file.read().splitlines()
            for y in range(5):
                for line in lines:
                    risks = [(int(char) - 1 + x + y) %
                             9 + 1 for x in range(5) for char in line]
                    chiton_map.add_row(risks)

            start = time.time()
            risk = chiton_map.find_shortest_path()
            end = time.time()

            print(f"\nThe lowest total risk of any path: {int(risk)}\n")
            print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
