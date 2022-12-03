#!/usr/bin/env python

'''
Advent of Code 2022 - Day 03: Rucksack Reorganization (Part 2)
https://adventofcode.com/2022/day/3
'''

import time

def find_badge_and_priority(rucksacks: list) -> int:
    rucksack1, rucksack2, rucksack3 = rucksacks
    result = set(rucksack1).intersection(set(rucksack2), set(rucksack3))
    badge = ''.join(result)
    priority = ord(badge) - 96 if badge.islower() else ord(badge) - 38
    print(f"Group has badge: {badge} with priority: {priority}")
    return priority

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            sum_of_priorities = 0
            rucksacks = []
            for count, line in enumerate(file):
                line = line.strip()
                rucksack = set(line)
                rucksacks.append(rucksack)
                if (count + 1) % 3 == 0:
                    sum_of_priorities += find_badge_and_priority(rucksacks)
                    rucksacks = []

            if rucksacks:
                sum_of_priorities += find_badge_and_priority(rucksacks)

            print(f"The sum of the priorities: {sum_of_priorities}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
