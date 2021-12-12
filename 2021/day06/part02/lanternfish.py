#!/usr/bin/env python

'''
Advent of Code 2021 - Day 6: Lanternfish (Part 2)
https://adventofcode.com/2021/day/6
'''

import sys
import time
from collections import deque

OLD_CYCLE = 6
NEW_CYCLE = 8


def get_day_str(day_num):
    return 'days' if day_num > 1 else 'day'


def simulate(state, days):
    totals = deque(state.count(i) for i in range(9))
    for day in range(days):
        totals.rotate(-1)
        totals[OLD_CYCLE] += totals[NEW_CYCLE]
        day_str = get_day_str(day+1)
        print(f"After {day:>3} {day_str}:\t{sum(totals)} fish")
    return sum(totals)


def main():
    filename = input("What is the input file name? ")
    try:
        days = int(input("How many days to simulate? "))
    except ValueError:
        print("Entered an invalid number of days. Please enter an integer value.")
        sys.exit()

    try:
        initial_state = []
        with open(filename, "r") as file:

            # Read the initial state
            line = file.readline().strip()
            initial_state = [int(x) for x in line.split(',')]

        state_str = ','.join(map(str, initial_state))
        print(f"\nInitial state:\t{state_str}\n")

        start = time.time()
        total_fish_on_day = simulate(initial_state, days)
        end = time.time()
        print(
            f"\nNumber of lanternfish after {days} {get_day_str(days)}: {total_fish_on_day}\n")
        print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
