#!/usr/bin/env python

'''
Advent of Code 2023 - Day 4: Scratchcards (Part 1)
https://adventofcode.com/2023/day/4
'''

import time


def calculate_points(winning: set, have: set) -> int:
    intersection = winning & have  # Calculate the intersection

    '''
      Return the number of points
      The first match makes the card worth one point and each match after the first doubles the point value of that card
    '''
    return 2 ** (len(intersection) - 1) if intersection else 0


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            card_points = []
            for line in file:
                line = line.strip()

                # Get the Card Label and Info
                _, card_info = line.split(':')

                # Get the Card numbers
                winning_numbers, nums_i_have = card_info.strip().split('|')

                # Convert to sets
                set_winning_numbers = set(winning_numbers.strip().split())
                set_nums_i_have = set(nums_i_have.strip().split())

                card_points.append(calculate_points(
                    set_winning_numbers, set_nums_i_have))
            print(
                f"The number of points the cards are worth: {sum(card_points)}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
