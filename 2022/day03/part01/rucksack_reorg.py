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
            for rucksack in file:
                rucksack = rucksack.strip()

                # A given rucksack always has the same number of items in each of its two compartments.
                compartment1 = set(rucksack[:len(rucksack)//2])
                compartment2 = set(rucksack[len(rucksack)//2:])

                # Check which items are in each compartment using set intersection
                result = compartment1.intersection(compartment2)
                common_item = ''.join(result)

                # Calculate priority using the integer value of the Unicode character.
                # Priority a-z = 1-26; A-Z = 27-52
                # ord('a') = 97  ord('A') = 65
                priority = ord(common_item) - 96 if common_item.islower() else ord(common_item) - 38
                print(f"Rucksack: {rucksack} has common item in compartments: {common_item} with priority: {priority}")

                sum_of_priorities += priority

            print(f"The sum of the priorities: {sum_of_priorities}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
