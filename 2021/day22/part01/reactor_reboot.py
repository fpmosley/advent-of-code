#!/usr/bin/env python

'''
Advent of Code 2021 - Day 22: Reactor Reboot (Part 1)
https://adventofcode.com/2021/day/22
'''


import re
import time
from itertools import product

MIN = -50
MAX = 50


def check_adjust_range(rmin: int, rmax: int) -> tuple:
    # Check if in valid range
    if rmin < rmax < MIN or MAX < rmin < rmax:
        return None, None

    # Check if we need to adjust the min or the max
    a_range = list(range(rmin, rmax + 1))
    rmin = -50 if MIN in a_range else rmin
    rmax = 50 if MAX in a_range else rmax

    return rmin, rmax


'''
Uses itertools.product to generate all the cube positions within the cuboid.
'''
def create_cuboid(xmin: int, xmax: int, ymin: int, ymax: int, zmin: int, zmax: int) -> set:
    return set(product(range(xmin, xmax + 1), range(ymin, ymax + 1), range(zmin, zmax + 1)))


def cubes_on(cubes: set, cuboid: set) -> set:
    return cubes | cuboid


def cubes_off(cubes: set, cuboid: set) -> set:
    return cubes - cuboid


def main():

    filename = input("What is the input file name? ")

    try:
        start = time.time()
        cubes = set()
        with open(filename, "r") as file:

            pattern = r'(?P<action>(on|off)) x=(?P<xmin>-?\d+)..(?P<xmax>-?\d+),y=(?P<ymin>-?\d+)..(?P<ymax>-?\d+),z=(?P<zmin>-?\d+)..(?P<zmax>-?\d+)'
            for line in file:
                line = line.strip()
                matches = re.match(pattern, line)
                if matches:
                    action = (matches.group('action'))
                    xmin = int(matches.group('xmin'))
                    xmax = int(matches.group('xmax'))
                    ymin = int(matches.group('ymin'))
                    ymax = int(matches.group('ymax'))
                    zmin = int(matches.group('zmin'))
                    zmax = int(matches.group('zmax'))

                xmin, xmax = check_adjust_range(rmin=xmin, rmax=xmax)
                ymin, ymax = check_adjust_range(rmin=ymin, rmax=ymax)
                zmin, zmax = check_adjust_range(rmin=zmin, rmax=zmax)
                if None in [xmin, xmax, ymin, ymax, zmin, zmax]:
                    # We have a cube outside the MIN and MAX region. Ignore it.
                    continue

                cuboid = create_cuboid(
                    xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax)

                if action == 'on':
                    cubes = cubes_on(cubes=cubes, cuboid=cuboid)
                else:
                    cubes = cubes_off(cubes=cubes, cuboid=cuboid)

        print(f"\nNumber of cubes that are on: {len(cubes)}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
