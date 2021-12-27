#!/usr/bin/env python

'''
Advent of Code 2021 - Day 17: Trick Shot (Part 1)
https://adventofcode.com/2021/day/17

References:
https://en.wikipedia.org/wiki/Triangular_number
'''


import re


def triangular_number(n):
    return n * (n + 1) // 2


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

        y_high = triangular_number(ymin)
        print(f"The highest y position: {y_high}")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
