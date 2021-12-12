#!/usr/bin/env python

'''
Advent of Code 2021 - Day 6: Lanternfish (Part 1)
https://adventofcode.com/2021/day/6
'''

import sys


def print_state(state, day):
    state_str = ','.join(map(str, state))
    if day == 0:
        print(f"Initial state:\t{state_str}")
    elif day == 1:
        print(f"After {day:>3} day:\t{state_str}")
    else:
        print(f"After {day:>3} days:\t{state_str}")


def add_day(state):
    new_state = []
    num_fish_to_add = 0
    for time in state:
        if time > 0:
            time -= 1
        else:
            time = 6
            num_fish_to_add += 1
        new_state.append(time)

    for _ in range(num_fish_to_add):
        new_state.append(8)

    return new_state


def main():

    filename = input("What is the input file name? ")
    try:
        days = int(input("How many days to simulate? "))
    except ValueError:
        print("Entered an invalid number of days. Please enter an integer value.")
        sys.exit()

    try:
        state = []
        with open(filename, "r") as file:

            # Read the initial state
            line = file.readline().strip()
            state = [int(x) for x in line.split(',')]

        print()
        print_state(state, 0)
        for day in range(1, days+1):
            state = add_day(state)
            print_state(state, day)

        day_str = 'days' if days > 1 else 'day'
        print(f"\nNumber of lanternfish after {days} {day_str}: {len(state)}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
