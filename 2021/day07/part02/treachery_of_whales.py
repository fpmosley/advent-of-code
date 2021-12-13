#!/usr/bin/env python

'''
Advent of Code 2021 - Day 7: The Treachery of Whales (Part 2)
https://adventofcode.com/2021/day/7

Minimizing the sum of accumulation of the absolute distances to a point.
'''

import random
import sys
from math import ceil, floor
from statistics import mean


def generate_list():
    return random.sample(range(1, 20), 11)


def calculate_cost(positions, align_at=1):
    return sum([sum(range(abs(x - align_at)+1)) for x in positions])


def find_mean_position(positions):
    print(f"Mean: {mean(positions)}")
    return mean(positions)


def find_position_to_align_on(positions):
    align_at_mean = find_mean_position(positions)
    align_at_pos = align_at_mean if isinstance(align_at_mean, float) and align_at_mean.is_integer() else round_mean(positions, align_at_mean)
    print(f"The mean position to align on is: {align_at_pos}\n")

    return align_at_pos

'''
Rounds the mean value to the lowest cost position after checking the floor and ceiling costs.
This was added because just rounding the mean could provide the wrong position the closer
the mean gets to the middle of two whole numbers.
'''
def round_mean(positions, mean_float):
    floor_cost = calculate_cost(positions, align_at=floor(mean_float))
    ceil_cost = calculate_cost(positions, align_at=ceil(mean_float))
    rounded_mean = floor(mean_float) if floor_cost <= ceil_cost else ceil(mean_float)
    return rounded_mean


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

            positions_str = ','.join(map(str, positions))
            print(f"\nTest #{i}")
            print(f"Initial positions:\t{positions_str}\n")

            # Find the min and max
            start = min(positions)
            stop = max(positions)

            costs = {}
            for position in range(start, stop+1):
                cost = calculate_cost(positions, align_at=position)
                costs[position] = cost
                print(f"Cost to align at position '{position:>2}': {cost}")

            print(
                f"\nThe position with the lowest cost is: {min(costs, key=costs.get)}")

            find_position_to_align_on(positions)
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

            align_at_pos = find_position_to_align_on(positions) 
            cost = calculate_cost(positions, align_at=align_at_pos)
            print(f"Cost to align at position '{align_at_pos}': {cost}\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
