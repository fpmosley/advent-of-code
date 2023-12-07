#!/usr/bin/env python

'''
Advent of Code 2023 - Day 1: Trebuchet?! (Part 2)
https://adventofcode.com/2023/day/1
'''

import time
import regex as re

def get_numeric_value(value: str) -> str:
    if value.isdigit():
        return value

    match value.lower():
        case 'one':
            return '1'
        case 'two':
            return '2'
        case 'three':
            return '3'
        case 'four':
            return '4'
        case 'five':
            return '5'
        case 'six':
            return '6'
        case 'seven':
            return '7'
        case 'eight':
            return '8'
        case 'nine':
            return '9'
        case _:
            return None
        

def find_calibration_value(line: str) -> int:
    num_string = ''
    match = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', line, overlapped=True)
    if match:
        num_string += get_numeric_value(match[0])
        num_string += get_numeric_value(match[-1])

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
