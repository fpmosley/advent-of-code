#!/usr/bin/env python

'''
Advent of Code 2022 - Day 10: Cathode-Ray Tube (Part 1)
https://adventofcode.com/2022/day/10
'''

import time

SIGNAL_STRENGTHS = {}


def check_signal_strength(cycle: int, register: int) -> None:
    if cycle in [20, 60, 100, 140, 180, 220]:
        SIGNAL_STRENGTHS[cycle] = cycle * register
        print(f"Cycle: {cycle: >3} Signal Strength: {cycle * register: >4}")


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            register_x = 1
            cycle = 0

            # Read the program
            for instruction in file:
                instruction = instruction.strip()

                if instruction == "noop":
                    cycle += 1
                    check_signal_strength(cycle=cycle, register=register_x)
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
                    check_signal_strength(cycle=cycle, register=register_x)
                    if i == 2:  # Add the value to the register after the cycle
                        register_x += value

        print(f"Sum of signal strengths: {sum(SIGNAL_STRENGTHS.values())}")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
