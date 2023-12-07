#!/usr/bin/env python

'''
Advent of Code 2023 - Day 1: Cube Conundrum (Part 2)
https://adventofcode.com/2023/day/2
'''

import time
import re


def fewest_num_cubes(game_sets: list) -> tuple:
    # Check each set of cubes for the fewest number for each color needed for the game
    game_cube_colors = {
        'red': [],
        'blue': [],
        'green': []
    }

    for game_set in game_sets:
        cubes = game_set.split(',')  # Split the cubes in each set
        for cube in cubes:
            # Get the number and color
            match = re.search(r'(\d+) (red|blue|green)', cube)
            if match:
                num_cubes = int(match.group(1))
                color_cubes = match.group(2)
                game_cube_colors[color_cubes].append(num_cubes)

    # Return the max of each color to get the fewest number needed for each color
    return max(game_cube_colors['red']), max(game_cube_colors['blue']), max(game_cube_colors['green'])


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            game_set_powers = []
            for line in file:
                line = line.strip()

                # Get the Game Info
                _, game_info = line.split(':')

                # Get the Game Sets
                game_sets = game_info.strip().split(';')

                # Get the fewest number of each color needed
                red, blue, green = fewest_num_cubes(game_sets)

                # Calculate the power of the set
                game_set_powers.append(red * blue * green)

            print(f"The sum of the power of the sets: {sum(game_set_powers)}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
