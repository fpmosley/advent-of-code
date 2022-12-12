#!/usr/bin/env python

'''
Advent of Code 2022 - Day 1: Calorie Counting (Part 2)
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
                food_calories = line.strip()

                if not food_calories:  # Blank line separates the calorie counts for each elf
                    calories_per_elf.append(sum(calories))  # Add the calorie sum to a list
                    calories = []
                    continue

                calories.append(int(food_calories))

            calories_per_elf.append(sum(calories))
            calories_per_elf.sort(reverse=True)  # Sort the list in descending order

            # Slice off the first three (highest) values
            print(f"Total calories carried by top 3 elves: {sum(calories_per_elf[0:3])}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
