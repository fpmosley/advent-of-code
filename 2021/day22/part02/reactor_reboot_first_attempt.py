#!/usr/bin/env python

'''
Advent of Code 2021 - Day 22: Reactor Reboot (Part 2)
https://adventofcode.com/2021/day/22

Went to Reddit to get help debugging my solution. This comment showed me my error:

Tho cuboids overlap when their projections on all 3 axes also overlap. More specifically, 
on this puzzle, you need to check (for each axis) if the minimum coordinate of one cuboid 
is smaller or equal than the maximum coordinate of the other cuboid. They overlap only if 
those check pass for all axes and both cuboids.
'''


import re
import time


class InvalidInputError(Exception):
    pass


'''
Finds the 
'''
def find_off_overlaps(ranges: set, test_min: int, test_max: int) -> tuple:
    new_ranges = set()
    if not ranges:
        return 0, ranges 

    intersection = set()
    test_range = range(test_min, test_max + 1)
    for range_min, range_max in ranges:
        a_range = set(range(range_min, range_max + 1))
        result = a_range.intersection(test_range)
        if result:
            # Update the intersection set and update the range
            intersection.update(result)
            if range_min < test_min < test_max < range_max:
                # Test min and max are enclosed in range
                new_ranges.update([(range_min, test_min), (test_max, range_max)])
            elif range_min < test_min < range_max:
                # Test min is in the range
                new_ranges.update([(range_min, test_min)])
            elif range_min < test_max < range_max:
                # Test max is in the range
                new_ranges.update([(test_max, range_max)])
        else:
            # No intersection. Add the existing range.
            new_ranges.update([(range_min, range_max)])

    return len(intersection), new_ranges 

def find_on_overlaps(ranges: set, test_min: int, test_max: int) -> tuple:
    new_ranges = set()
    if not ranges:
        new_ranges.update([(test_min, test_max)])
        return 0, new_ranges 

    intersection = set()
    test_range = range(test_min, test_max + 1)
    for range_min, range_max in ranges:
        a_range = set(range(range_min, range_max + 1))
        result = a_range.intersection(test_range)
        if result:
            # Update the intersection set and update the range
            intersection.update(result)
            new_min = min(range_min, test_min) 
            new_max = max(range_max, test_max)
            new_ranges.update([(new_min, new_max)])
        else:
            # No intersection with this range. Add the range back in.
            new_ranges.update([(range_min, range_max)])

    if not intersection:
        # No intersection with any ranges. Add the test values as a new range. 
        new_ranges.update([(test_min, test_max)])

    return len(intersection), new_ranges 


def number_of_cubes(xmin: int, xmax: int, ymin: int, ymax: int, zmin: int, zmax: int) -> int:
    return (abs(xmax - xmin) + 1) * (abs(ymax - ymin) + 1) * (abs(zmax - zmin) + 1)


def main():

    filename = input("What is the input file name? ")

    try:
        start = time.time()
        cube_count = 0 

        with open(filename, "r") as file:

            x_ranges = set()
            y_ranges = set()
            z_ranges = set()

            pattern = r'(?P<action>(on|off)) x=(?P<xmin>-?\d+)..(?P<xmax>-?\d+),y=(?P<ymin>-?\d+)..(?P<ymax>-?\d+),z=(?P<zmin>-?\d+)..(?P<zmax>-?\d+)'
            for line in file:
                line = line.strip()
                matches = re.match(pattern, line)
                if not matches:
                    raise InvalidInputError("Received invalid input")

                action = (matches.group('action'))
                xmin = int(matches.group('xmin'))
                xmax = int(matches.group('xmax'))
                ymin = int(matches.group('ymin'))
                ymax = int(matches.group('ymax'))
                zmin = int(matches.group('zmin'))
                zmax = int(matches.group('zmax'))

                if action == 'on':
                    cuboid_count = number_of_cubes(
                        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax)

                    x_overlaps, new_x_ranges = find_on_overlaps(x_ranges, xmin, xmax)
                    y_overlaps, new_y_ranges = find_on_overlaps(y_ranges, ymin, ymax)
                    z_overlaps, new_z_ranges = find_on_overlaps(z_ranges, zmin, zmax)

                    # Check if there is overlap on all 3 axes
                    if all((x_overlaps, y_overlaps, z_overlaps)) or any(not x for x in [x_ranges, y_ranges, z_ranges]):
                        x_ranges = new_x_ranges
                        y_ranges = new_y_ranges
                        z_ranges = new_z_ranges
                    else:
                        # No overlap with all ranges. Add the step values as a new range. 
                        x_ranges.update([(xmin, xmax)])
                        y_ranges.update([(ymin, ymax)])
                        z_ranges.update([(zmin, zmax)])

                        # Set overlap to 0 if not on all 3 axes
                        x_overlaps = y_overlaps = z_overlaps = 0

                    # Subtract the overlaps from the set of all cubes (cuboid)
                    cuboid_count = cuboid_count - (x_overlaps * y_overlaps * z_overlaps)

                    # Add (turn on) the cubes that did not overlap
                    cube_count += cuboid_count 
                else:
                    x_overlaps, new_x_ranges = find_off_overlaps(x_ranges, xmin, xmax)
                    y_overlaps, new_y_ranges = find_off_overlaps(y_ranges, ymin, ymax)
                    z_overlaps, new_z_ranges = find_off_overlaps(z_ranges, zmin, zmax)

                    # Check if there is overlap on all 3 axes
                    if all((x_overlaps, y_overlaps, z_overlaps)):
                        x_ranges = new_x_ranges
                        y_ranges = new_y_ranges
                        z_ranges = new_z_ranges
                    else:
                        # Set overlap to 0 if not on all 3 axes
                        x_overlaps = y_overlaps = z_overlaps = 0

                    # Remove (turn off) the cubes that overlap
                    cube_count -= (x_overlaps * y_overlaps * z_overlaps)

        print(f"x range: {x_ranges}")
        print(f"y range: {y_ranges}")
        print(f"z range: {z_ranges}")
        print(f"\nNumber of cubes that are on: {cube_count}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except InvalidInputError as e:
        print(e)


if __name__ == "__main__":
    main()
