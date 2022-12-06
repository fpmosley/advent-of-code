#!/usr/bin/env python

'''
Advent of Code 2022 - Day 3: Rucksack Reorganization (Part 1)
https://adventofcode.com/2022/day/3
'''

import time

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            sum_of_priorities = 0
            for line in file:
                line = line.strip()
                compartment1 = set(line[:len(line)//2])
                compartment2 = set(line[len(line)//2:])
                result = compartment1.intersection(compartment2)
                common_item = ''.join(result)
                priority = ord(common_item) - 96 if common_item.islower() else ord(common_item) - 38
                print(f"Rucksack: {line} has common item in compartments: {common_item} with priority: {priority}")

                sum_of_priorities += priority

            print(f"The sum of the priorities: {sum_of_priorities}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
