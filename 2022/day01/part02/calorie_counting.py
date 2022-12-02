#!/usr/bin/env python

'''
Advent of Code 2022 - Day 01: Calorie Counting (Part 2)
https://adventofcode.com/2022/day/1
'''

import time

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            calories = []
            calories_per_elf = []
            for line in file:
                line = line.strip()

                if not line:
                    calories_per_elf.append(sum(calories))
                    calories = []
                    continue

                calories.append(int(line))

            calories_per_elf.append(sum(calories))
            calories_per_elf.sort(reverse=True)
            print(f"Total calories carried by top 3 elves: {sum(calories_per_elf[0:3])}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
