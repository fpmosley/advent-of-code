#!/usr/bin/env python

'''
Advent of Code 2021 - Day 7: The Treachery of Whales (Part 1)
https://adventofcode.com/2021/day/7

Minimizing the sum of absolute distances to a point.

References:
https://www.geeksforgeeks.org/optimum-location-point-minimize-total-distance/
https://math.stackexchange.com/questions/3092033/find-a-number-having-minimum-sum-of-distances-between-a-set-of-numbers
'''

import random
import sys
from math import ceil
from statistics import median


def generate_list():
    return random.sample(range(1, 20), 11)


def calculate_cost(positions, align_at=1):
    return sum([abs(x - align_at) for x in positions])


def find_position_to_align_on(positions):
    return ceil(median(positions))


def main():
    test_resp = input("Do you want to run a test (Y/N)? ")
    run_test = True if test_resp.upper() == 'Y' else False

    if run_test:
        try:
            num_of_tests = int(input("How many tests? "))
        except ValueError:
            print("Please enter a valid number.")
            sys.exit()

        for i in range(1, num_of_tests+1):
            positions = generate_list()

            # Find the min and max
            start = min(positions)
            stop = max(positions)

            positions_str = ','.join(map(str, positions))
            print(f"\nTest #{i}")
            print(f"Initial positions:\t{positions_str}\n")

            costs = {}
            for position in range(start, stop+1):
                cost = calculate_cost(positions, align_at=position)
                costs[position] = cost
                print(f"Cost to align at position '{position}': {cost}")

            print(
                f"\nThe position with the lowest cost is: {min(costs, key=costs.get)}")

            align_at_median = find_position_to_align_on(positions)
            print(f"The median position to align on is: {align_at_median}\n")
    else:
        filename = input("What is the input file name? ")
        try:
            positions = []
            with open(filename, "r") as file:

                # Read the initial positions
                line = file.readline().strip()
                positions = [int(x) for x in line.split(',')]

            positions_str = ','.join(map(str, positions))
            print(f"\nInitial positions:\t{positions_str}\n")

            align_at_median = find_position_to_align_on(positions)
            print(f"The median position to align on is: {align_at_median}")
            cost = calculate_cost(positions, align_at=align_at_median)
            print(f"Cost to align at position '{align_at_median}': {cost}\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
