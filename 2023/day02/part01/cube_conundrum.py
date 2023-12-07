#!/usr/bin/env python

'''
Advent of Code 2023 - Day 1: Cube Conundrum (Part 1)
https://adventofcode.com/2023/day/2
'''

import time
import re

RED_LIMIT = 12
BLUE_LIMIT = 14
GREEN_LIMIT = 13


def valid_num_cubes(num: int, color: str) -> bool:
    match color.lower():
        case 'red':
            return num <= RED_LIMIT
        case 'blue':
            return num <= BLUE_LIMIT
        case 'green':
            return num <= GREEN_LIMIT
        case _:
            return False


def valid_game(game_sets: list) -> bool:
    # Check each set of cubes for a valid number for each color
    for game_set in game_sets:
        cubes = game_set.split(',')  # Split the cubes in each set
        for cube in cubes:
            # Get the number and color
            match = re.search(r'(\d+) (red|blue|green)', cube)
            if match:
                num_cubes = match.group(1)
                color_cubes = match.group(2)
                if not valid_num_cubes(int(num_cubes), color_cubes):
                    return False

    return True


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            valid_game_ids = []
            for line in file:
                line = line.strip()

                # Get the Game Label and Info
                game_label, game_info = line.split(':')

                # Get the Game ID
                _, game_id = game_label.strip().split()

                # Get the Game sets
                game_sets = game_info.strip().split(';')

                if valid_game(game_sets):
                    try:
                        valid_game_ids.append(int(game_id))
                    except ValueError as e:
                        print(f"Error converting game ID to an int: {e}")

            print(f"The sum of all the valid game IDs: {sum(valid_game_ids)}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
