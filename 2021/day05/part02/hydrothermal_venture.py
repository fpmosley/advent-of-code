#!/usr/bin/env python

'''
Advent of Code 2021 - Day 5: Hydrothermal Venture (Part 2)
https://adventofcode.com/2021/day/5
'''

import re
import sys
import numpy as np


class Diagram():
    def __init__(self, size) -> None:
        self._diagram = np.full((size, size), 0)

    def add_horiz_line(self, y, lower_x_bound, upper_x_bound):
        for x in range(lower_x_bound, upper_x_bound+1):
            self._diagram[y, x] += 1

    def add_vert_line(self, x, lower_y_bound, upper_y_bound):
        for y in range(lower_y_bound, upper_y_bound+1):
            self._diagram[y, x] += 1

    def add_diag_line(self, x_range, y_range):
        x = x_range['start']
        y = y_range['start']
        while x != x_range['stop'] + x_range['direction'] and y != y_range['stop'] + y_range['direction']:
            self._diagram[y, x] += 1
            x = x + x_range['direction']
            y = y + y_range['direction']

    def calculate_overlap(self):
        result = np.where(self._diagram >= 2)
        coordinates = self.get_coordinates(result)
        return len(coordinates)

    @staticmethod
    def get_coordinates(result):
        return list(zip(result[0], result[1]))

    def __str__(self) -> str:
        output = ""
        for row in self._diagram:
            for elem in row:
                elem = '.' if elem == 0 else elem
                output = output + f"{elem:>3}"
            output = output + "\n"
        return output


def main():

    filename = input("What is the input file name? ")
    try:
        size = int(input("What size diagram? "))
    except ValueError:
        print("Entered an invalid size. Please enter an integer between 1-999.")
        sys.exit()

    # Create the diagram
    diagram = Diagram(size)

    try:
        with open(filename, "r") as file:

            # Create match pattern
            pattern = r'^(?P<x1>\d+),(?P<y1>\d+)\s+->\s+(?P<x2>\d+),(?P<y2>\d+)'

            # Read the coordinates
            for line in file:
                line = line.strip()

                matches = re.match(pattern, line)
                if matches:
                    x1 = int(matches.group('x1'))
                    y1 = int(matches.group('y1'))
                    x2 = int(matches.group('x2'))
                    y2 = int(matches.group('y2'))

                if x1 == x2:
                    lower_bound = y1 if y1 < y2 else y2
                    upper_bound = y2 if y1 < y2 else y1
                    diagram.add_vert_line(x1, lower_bound, upper_bound)
                elif y1 == y2:
                    lower_bound = x1 if x1 < x2 else x2
                    upper_bound = x2 if x1 < x2 else x1
                    diagram.add_horiz_line(y1, lower_bound, upper_bound)
                elif abs(x1 - x2) == abs(y1 - y2):  # Checking for 45 degree diagonal line
                    x_range = {
                        'start': x1,
                        'stop': x2,
                        'direction': 1 if x1 < x2 else -1,
                    }

                    y_range = {
                        'start': y1,
                        'stop': y2,
                        'direction': 1 if y1 < y2 else -1,
                    }
                    diagram.add_diag_line(x_range, y_range)

        print("\nDiagram:")
        print(diagram)
        num_overlaps = diagram.calculate_overlap()
        print(
            f"\nNumber of points at least two lines overlap: {num_overlaps}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
