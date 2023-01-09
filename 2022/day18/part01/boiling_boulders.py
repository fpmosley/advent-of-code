#!/usr/bin/env python

'''
Advent of Code 2022 - Day 18: Boiling Boulders (Part 1)
https://adventofcode.com/2022/day/18
'''
import time

DELTAS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]


def find_adjacent_positions(cube: tuple) -> list[tuple]:
    '''Finds the positions that are +/- 1 position across each axis'''

    x, y, z = cube
    return [(x+dx, y+dy, z+dz) for dx, dy, dz in DELTAS]


def calculate_surface_area(cubes: dict[tuple, int]) -> int:
    for position in cubes:
        adjacent_positions = find_adjacent_positions(position)

        for adjacent_position in adjacent_positions:
            if adjacent_position in cubes:
                # Reduce the number of sides that aren't covered
                cubes[position] -= 1

    return sum(cubes.values())


def main():

    filename = input("What is the input file name? ")

    try:

        with open(filename, "r") as file:

            start = time.time()

            # Create dictionary of cubes (K: position, V: Uncovered sides)
            cubes = {}
            for line in file:
                x, y, z = line.strip().split(',')
                # Create a key that is a tuple of the coordinates
                key = (int(x), int(y), int(z))
                cubes[key] = 6  # Initialize cube to 6 uncovered sides

        print(
            f"\nThe surface area of the scanned lava droplet: {calculate_surface_area(cubes=cubes)}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
