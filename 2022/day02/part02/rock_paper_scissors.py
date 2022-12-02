#!/usr/bin/env python

'''
Advent of Code 2022 - Day 02: Rock, Paper, Scissors (Part 2)
https://adventofcode.com/2022/day/2
'''

import time

def score_round(opponent: str, strategy: str) -> int:

    strategy_table = {
        'A' : {
            'X': 'scissors',    # lose
            'Y': 'rock',        # draw
            'Z': 'paper'        # win
        },
        'B' : {
            'X': 'rock',        # lose
            'Y': 'paper',       # draw
            'Z': 'scissors'     # win
        },
        'C' : {
            'X': 'paper',       # lose
            'Y': 'scissors',    # draw
            'Z': 'rock'         # win
        },
    } 

    shape_score = {
        'rock': 1,
        'paper': 2,
        'scissors': 3 
    }

    round_score = {
        'Z': 6, # win
        'Y': 3, # draw
        'X': 0, # lose
    }

    try:
        outcome = strategy_table[opponent][strategy] 
        return round_score[strategy] + shape_score[outcome]

    except KeyError:
        return 0

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            total_score = 0
            for line in file:
                line = line.strip()
                opponent, strategy = line.split(' ')
                total_score += score_round(opponent, strategy)
            
            print(f"The total score: {total_score}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
