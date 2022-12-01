#!/usr/bin/env python

'''
Advent of Code 2022 - Day 01: Calorie Counting (Part 1)
https://adventofcode.com/2022/day/01
'''

import time

def calculate_most_calories(most_calories: int, calories: list) -> int:
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
                line = line.strip()

                if not line:
                    most_calories = calculate_most_calories(most_calories, calories) 
                    calories = []
                    continue

                calories.append(int(line))
            
            most_calories = calculate_most_calories(most_calories, calories) 

            print(f"The most calories carried: {most_calories}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
