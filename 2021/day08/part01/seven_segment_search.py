#!/usr/bin/env python

'''
Advent of Code 2021 - Day 8: Seven Segment Search (Part 1)
https://adventofcode.com/2021/day/8
'''


'''
Digits 1, 4, 7, and 8 each use a unique number of segments.
1 = 2 segements
4 = 4 segements
7 = 3 segements
8 = 7 segements
'''
def count_unique_digits(digits):
    unique_digits = [digit for digit in digits if len(digit) in [2, 4, 3, 7]]
    return len(unique_digits)


def main():
    filename = input("What is the input file name? ")
    try:
        with open(filename, "r") as file:

            # Read the entries
            total_unique_digits = 0
            for line in file:
                _, second_part = line.split('|')
                four_digit_value = second_part.strip().split()
                total_unique_digits += count_unique_digits(four_digit_value)

            print(
                f"Number of times digits 1, 4, 7, or 8 appear: {total_unique_digits}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
