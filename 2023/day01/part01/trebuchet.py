#!/usr/bin/env python

'''
Advent of Code 2023 - Day 1: Trebuchet?! (Part 1)
https://adventofcode.com/2023/day/1
'''

import time
import re

def find_calibration_value(line: str) -> int:
    num_string = ''
    match = re.findall(r'\d', line)
    if match:
        num_string += match[0]
        num_string += match[-1]

    return int(num_string)


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            calibration_values = []
            for line in file:
                line = line.strip()

                calibration_value = find_calibration_value(line)
                calibration_values.append(calibration_value)

            print(f"The sum of all the calibration values: {sum(calibration_values)}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
