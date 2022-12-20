#!/usr/bin/env python

'''
Advent of Code 2022 - Day 15: Beacon Exclusion Zone (Part 2)
https://adventofcode.com/2022/day/15

Utilized the Shapely library (Could not solve it without the library)
https://pypi.org/project/shapely/
'''

from collections import OrderedDict
from itertools import product
import time
import re
from shapely.ops import unary_union, clip_by_rect
from shapely.geometry import Polygon


def manhattan(scanner: tuple, beacon: tuple) -> int:
    x1, y1 = scanner
    x2, y2 = beacon

    return abs(x2 - x1) + abs(y2 - y1)


def main():

    filename = input("What is the input file name? ")

    try:
        upper_bound = int(input("What is the upper bound? (Lower Bound = 0) "))

        with open(filename, "r") as file:

            start = time.time()

            # Create a Shapely Polygon 
            union_poly = Polygon()

            # Read the sensor and beacon positions
            for line in file:
                line = line.strip()

                # Find all the points in the input line
                result = re.search(
                    r"^Sensor at x=([\d-]+), y=([\d-]+):.+x=([-\d]+), y=([\d-]+)$", line)
                if result:
                    sx = int(result.group(1))
                    sy = int(result.group(2))
                    scanner = (sx, sy)

                    bx = int(result.group(3))
                    by = int(result.group(4))
                    beacon = (bx, by)

                    # Calculate the Manhattan distance to the nearest beacon
                    md = manhattan(
                        scanner=scanner, beacon=beacon)

                    coordinates = [(sx, sy + md), (sx - md, sy), (sx, sy - md), (sx + md, sy)]

                    # Create a polygon with the coordinates for the shape +/- distance in x, y.
                    # Create a union of the polygon and existing polygon shapes.
                    union_poly = unary_union([union_poly, Polygon(coordinates)])

        interior = clip_by_rect(union_poly, 0, 0, upper_bound, upper_bound).interiors[0]
        distress_beacon = tuple(map(round, interior.centroid.coords[:][0]))
        x, y = distress_beacon
        tuning_signal = x * 4000000 + y
        print(f"Location for the distress beacon: {distress_beacon}")
        print(f"Tuning signal: {tuning_signal}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
