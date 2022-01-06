#!/usr/bin/env python

'''
Advent of Code 2021 - Day 22: Reactor Reboot (Part 2)
https://adventofcode.com/2021/day/22

Reference (Inclusion-exclusion Principle):
https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle
'''


import re
import time


class InvalidInputError(Exception):
    pass


'''
To find an overlap:
    overlap = max(min values) < min(max values) over all axes 
Format of input lists: [action, xmin, xmax, ymin, ymax, zmin, zmax]

For an 'on' action, we subtract the intersection. We add the intersection for an 'off' action.
'''
def overlap(cuboid: list, step: list) -> list:
    def reverse(a): return -a
    # Add or subtract the intersection based on step action
    intersection = [reverse(step[0])]
    for i in range(1, 6, 2):
        max_value = max([cuboid[i], step[i]])  # Max of the minimum values
        min_value = min([cuboid[i+1], step[i+1]])  # Min of the maximum values
        intersection.extend([max_value, min_value])

        if max_value > min_value:
            return None

    return intersection


def number_of_cubes(action: int, xmin: int, xmax: int, ymin: int, ymax: int, zmin: int, zmax: int) -> int:
    return action * (abs(xmax - xmin) + 1) * (abs(ymax - ymin) + 1) * (abs(zmax - zmin) + 1)


def count_cubes(steps: list) -> int:
    cube_count = 0
    for step in steps:
        cube_count += number_of_cubes(*step)

    return cube_count


def main():

    filename = input("What is the input file name? ")

    try:
        start = time.time()
        steps = []

        with open(filename, "r") as file:

            pattern = r'(?P<action>(on|off)) x=(?P<xmin>-?\d+)..(?P<xmax>-?\d+),y=(?P<ymin>-?\d+)..(?P<ymax>-?\d+),z=(?P<zmin>-?\d+)..(?P<zmax>-?\d+)'
            for line in file:
                line = line.strip()
                matches = re.match(pattern, line)
                if not matches:
                    raise InvalidInputError("Received invalid input")

                action = (matches.group('action'))
                action = 1 if action == 'on' else -1
                xmin = int(matches.group('xmin'))
                xmax = int(matches.group('xmax'))
                ymin = int(matches.group('ymin'))
                ymax = int(matches.group('ymax'))
                zmin = int(matches.group('zmin'))
                zmax = int(matches.group('zmax'))

                cuboid = [action, xmin, xmax, ymin, ymax, zmin, zmax]

                # Add a cuboid if 'on'
                steps_to_add = [cuboid] if cuboid[0] == 1 else []
                for step in steps:
                    intersection = overlap(cuboid, step)
                    if intersection:
                        steps_to_add += [intersection]
                steps += steps_to_add

        print(f"\nNumber of cubes that are on: {count_cubes(steps)}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except InvalidInputError as e:
        print(e)


if __name__ == "__main__":
    main()
