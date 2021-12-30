#!/usr/bin/env python

'''
Advent of Code 2021 - Day 17: Trick Shot (Part 2)
https://adventofcode.com/2021/day/17

References:
https://en.wikipedia.org/wiki/Triangular_number
'''


import re
from typing import Tuple


def triangular_number(n):
    return n * (n + 1) // 2


def initial_velocities(xmin, xmax, ymin, ymax) -> Tuple:
    velocities = set()
    y_high = 0

    for v0x in range(1, xmax + 1):  # Can assume velocity of x >= 1 and x <= xmax
        # velocity of y > -ymin will miss the target at y=0; y >= ymin hits target at t=1
        for v0y in range(ymin, -ymin):
            x, y = (0, 0)
            vx, vy = v0x, v0y

            # Check that we are in the target area
            while x <= xmax and y >= ymin:
                # Are we in the target area?
                if x >= xmin and y <= ymax:
                    velocities.add((v0x, v0y))
                    break

                # Advance the trajectory
                x, y = (x + vx, y + vy)
                vy -= 1

                # Make sure velocity of x is >= 0
                if vx > 0:
                    vx -= 1

                # Update the highest y position
                if y > y_high:
                    y_high = y

    return y_high, sorted(velocities, key=lambda s: (s[0], s[1]))


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            pattern = r'^target area: x=(?P<xmin>-?\d+)..(?P<xmax>-?\d+),\s+y=(?P<ymin>-?\d+)..(?P<ymax>-?\d+)'

            # Read the target area
            for line in file:
                line = line.strip()

                matches = re.match(pattern, line)
                if matches:
                    xmin = int(matches.group('xmin'))
                    xmax = int(matches.group('xmax'))
                    ymin = int(matches.group('ymin'))
                    ymax = int(matches.group('ymax'))

        y_high, velocities = initial_velocities(xmin, xmax, ymin, ymax)
        print()
        for index, velocity in enumerate(velocities):
            x, y = velocity
            velocity_str = f"{x},{y}"
            print(f"{velocity_str:<7}", end="  ")
            if (index + 1) % 8 == 0:
                print("\n")

        print(f"\n\nThe highest y position: {y_high}")
        print(
            f"The number of distinct initial velocites that hit the target area: {len(velocities)}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
