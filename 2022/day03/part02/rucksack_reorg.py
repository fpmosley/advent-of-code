#!/usr/bin/env python

'''
Advent of Code 2022 - Day 3: Rucksack Reorganization (Part 2)
https://adventofcode.com/2022/day/3
'''

import time

def find_badge_and_priority(rucksacks: list) -> int:
    rucksack1, rucksack2, rucksack3 = rucksacks

    # Check which items are in each rucksack using set intersection
    result = set(rucksack1).intersection(set(rucksack2), set(rucksack3))
    badge = ''.join(result)

    # Calculate priority using the integer value of the Unicode character.
    # Priority a-z = 1-26; A-Z = 27-52
    # ord('a') = 97  ord('A') = 65
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
            for count, rucksack in enumerate(file):
                rucksack = rucksack.strip()
                rucksack = set(rucksack)
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
