#!/usr/bin/env python

'''
Advent of Code 2022 - Day 10: Cathode-Ray Tube (Part 2)
https://adventofcode.com/2022/day/10
'''

import time

SIGNAL_STRENGTHS = {}


def move_register_row(cycle: int, register: int) -> int:
    if cycle == 0:
        return register

    # Move the register to the next row after 40 cycles
    return register + 40 if cycle % 40 == 0 else register


def draw(screen: list, cycle: int, register: int) -> None:
    """Draw a lit pixel if the sprite '#' is visible"""
    if cycle - 1 in range(register - 1, register + 2):
        screen[cycle - 1] = "#"


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            register_x = 1
            cycle = 0
            screen = ['.' for _ in range(240)]

            # Read the program
            for instruction in file:
                instruction = instruction.strip()

                if instruction == "noop":
                    cycle += 1
                    register_x = move_register_row(
                        cycle=cycle - 1, register=register_x)
                    draw(screen=screen, cycle=cycle, register=register_x)
                    continue

                _, value = instruction.split()
                try:
                    value = int(value)
                except TypeError as e:
                    print(e)
                    continue

                # Loop through 2 cycles of the 'addx' instruction
                for i in range(1, 3):
                    cycle += 1
                    register_x = move_register_row(
                        cycle=cycle - 1, register=register_x)
                    draw(screen=screen, cycle=cycle, register=register_x)
                    if i == 2:  # Add the value to the register after the cycle
                        register_x += value

        # Print the screen
        for i in range(1, 241):
            print(screen[i - 1], end='')
            if i % 40 == 0:
                print()
        print()

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
