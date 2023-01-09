#!/usr/bin/env python

'''
Advent of Code 2022 - Day 18: Boiling Boulders (Part 2)
https://adventofcode.com/2022/day/18
'''
from collections import deque
import time


# Initialize deltas
DELTAS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

# Initiliaze bounds
min_x = min_y = min_z = 0
max_x = max_y = max_z = 0

# Initialize caches
internal_cubes = set()
external_cubes = set()


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


def has_path_to_outside(cube: tuple, cubes: list) -> bool:
    """Find path beyond bounds using a breadth-first search"""
    queue = deque([cube])
    visited = set()

    while queue:
        current_cube = queue.popleft()

        # Check caches
        if current_cube in external_cubes:
            return True  # We've got out from here before
        if current_cube in internal_cubes:
            continue  # This cube doesn't have a path, so no point checking its neighbours

        if current_cube in cubes:
            continue  # This path is blocked

        # Check if we've followed a path outside of the bounds
        x, y, z = current_cube
        if x > max_x or y > max_y or z > max_z:
            return True
        if x < min_x or y < min_y or z < min_z:
            return True

        # We want to look at all neighbors of this empty space
        # Who Da Neighbors (https://youtu.be/l37eskdhXeE)
        for neighbor in find_adjacent_positions(cube=current_cube):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return False


def calculate_external_surface_area(cubes: list) -> int:
    """ Determine surface area of all cubes that can reach the outside. """
    surfaces_to_outside = 0

    # Loop through the cubes and find any that can reach outside
    for cube in cubes:
        # for each adjacent...
        for adjacent in find_adjacent_positions(cube=cube):
            if has_path_to_outside(cube=adjacent, cubes=cubes):
                external_cubes.add(adjacent)
                surfaces_to_outside += 1
            else:
                internal_cubes.add(adjacent)

    return surfaces_to_outside


def main():
    global min_x, min_y, min_z
    global max_x, max_y, max_z

    filename = input("What is the input file name? ")

    try:

        with open(filename, "r") as file:

            start = time.time()

            # Create dictionary of cubes (K: position, V: Uncovered sides)
            cubes = {}
            for line in file:
                x, y, z = line.strip().split(',')

                # Create a key that is a tuple of the coordinates
                x, y, z = (int(x), int(y), int(z))
                # Initialize cube to 6 uncovered sides
                cubes[(x, y, z)] = 6

                # Set the bounds
                min_x = min(x, min_x)
                min_y = min(y, min_y)
                min_z = min(z, min_z)
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                max_z = max(z, max_z)

        print(
            f"\nThe exterior surface area of the scanned lava droplet: {calculate_external_surface_area(cubes=list(cubes.keys()))}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
