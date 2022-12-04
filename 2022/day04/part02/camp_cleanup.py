#!/usr/bin/env python

'''
Advent of Code 2022 - Day 04: Camp Cleanup (Part 1)
https://adventofcode.com/2022/day/4
'''

import time

def get_section(arange: str) -> set:
    try:
        lower, upper = arange.split('-')
        return set(range(int(lower), int(upper)+1))
    except ValueError as e:
        print(e)
        return None

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            fully_contained = 0
            for line in file:
                pairs = line.strip()

                section_one_range, section_two_range = pairs.split(',')
                section_one = get_section(section_one_range)
                section_two = get_section(section_two_range)

                if (section_one and section_two) and section_one.intersection(section_two):
                    fully_contained += 1

            print(f"The number of assignments that overlap: {fully_contained}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
