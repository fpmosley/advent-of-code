#!/usr/bin/env python

'''
Advent of Code 2022 - Day 15: Beacon Exclusion Zone (Part 1)
https://adventofcode.com/2022/day/15
'''

from collections import OrderedDict
import time
import re

# Create a new map
sensor_beacon_map = OrderedDict()


def manhattan(scanner: tuple, beacon: tuple) -> int:
    x1, y1 = scanner
    x2, y2 = beacon

    return abs(x2 - x1) + abs(y2 - y1)

# My first attempt at solving Part 01 used this function with nested loops.
# This solution did not work.


def detect_no_beacons(scanner: tuple, distance: int) -> None:
    """Use Manhattan distance value to calculate range in x and y directions"""
    x, y = scanner
    for i in range(x - distance, x + distance + 1):
        # y range is result of x - scanner(x) - distance
        y_range = abs(abs(i - x) - distance)
        for j in range(y - y_range, y + y_range + 1):
            value = sensor_beacon_map.get((i, j), None)
            if value and value in ['B', 'S']:  # Don't overwrite a beacon or sensor
                continue
            sensor_beacon_map[(i, j)] = '#'


def main():

    filename = input("What is the input file name? ")

    try:
        y_value = int(input("What is the y value? "))

        with open(filename, "r") as file:

            start = time.time()

            # Create a set to maintain the possible X positions with no beacon on the Y value
            no_beacon_x_positions = set()

            # Create a set to maintain the scanner and beacon X positions on the Y value
            scanner_beacon_x_positions = set()

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
                    if sy == y_value:  # Add the scanner X position if on the Y value
                        scanner_beacon_x_positions.add(sx)

                    bx = int(result.group(3))
                    by = int(result.group(4))
                    beacon = (bx, by)
                    if by == y_value:  # Add the beacon X position if on the Y value
                        scanner_beacon_x_positions.add(bx)

                    # Calculate the Manhattan distance to the nearest beacon
                    distance_to_beacon = manhattan(
                        scanner=scanner, beacon=beacon)

                    # Is distance to Y value within range of nearest beacon?
                    distance_to_y_value = abs(sy - y_value)
                    if distance_to_y_value <= distance_to_beacon:
                        # Find positions with no beacon along Y value using Manhattan distance.
                        # Any position with a Manhattan distance <= distance to nearest beacon
                        # abs(x) = distance to beacon - abs(scanner(Y) - Y Value)
                        x = abs(distance_to_beacon - distance_to_y_value)

                        # Put the range of X positions along the row in a list
                        x_positions = list(range(sx - x, sx + x + 1))
                        no_beacon_x_positions.update(x_positions)

        # Remove the X positions that are beacons and scanners
        no_beacon_x_positions.difference_update(scanner_beacon_x_positions)

        print(
            f"In row y={y_value} the number of positions with no beacon: {len(no_beacon_x_positions)}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
