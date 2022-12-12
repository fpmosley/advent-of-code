#!/usr/bin/env python

'''
Advent of Code 2022 - Day 1: Calorie Counting (Part 1)
https://adventofcode.com/2022/day/1
'''

import time

def calculate_most_calories(most_calories: int, calories: list) -> int:
    """ Sum the calories and determine if the most calories."""
    total_calories = sum(calories)
    return total_calories if total_calories > most_calories else most_calories

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            calories = []
            most_calories = 0
            for line in file:
                food_calories = line.strip()

                if not food_calories:  # Blank line separates the calorie counts for each elf
                    most_calories = calculate_most_calories(most_calories, calories)
                    calories = []
                    continue

                calories.append(int(food_calories))  # Add the food calories to list of calories

            most_calories = calculate_most_calories(most_calories, calories)

            print(f"The most calories carried: {most_calories}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
