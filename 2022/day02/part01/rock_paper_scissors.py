#!/usr/bin/env python

'''
Advent of Code 2022 - Day 02: Rock, Paper, Scissors (Part 1)
https://adventofcode.com/2022/day/2
'''

import time

def score_round(opponent: str, strategy: str) -> int:

    outcome_table = {
        'A' : {
            'X': 'draw',
            'Y': 'win',
            'Z': 'lose'
        },
        'B' : {
            'X': 'lose',
            'Y': 'draw',
            'Z': 'win'
        },
        'C' : {
            'X': 'win',
            'Y': 'lose',
            'Z': 'draw'
        },
    } 

    shape_score = {
        'X': 1, # Rock
        'Y': 2, # Paper
        'Z': 3  # Scissors
    }

    round_score = {
        'win': 6,
        'lose': 0,
        'draw': 3
    }

    try:
        outcome = outcome_table[opponent][strategy] 
        return round_score[outcome] + shape_score[strategy]

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
