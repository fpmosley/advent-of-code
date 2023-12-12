#!/usr/bin/env python

'''
Advent of Code 2023 - Day 4: Scratchcards (Part 2)
https://adventofcode.com/2023/day/4
'''

import time

SCRATCHCARDS = {}

def add_card(card_id):
    if SCRATCHCARDS.get(card_id):
        SCRATCHCARDS[card_id] += 1
    else:
        SCRATCHCARDS[card_id] = 1


def collect_wins(winning_id, wins):
    # Get number of winning cards to use as multipler
    multiplier = SCRATCHCARDS[winning_id]
    for i in range(winning_id + 1, winning_id + wins + 1):
        if SCRATCHCARDS.get(i):
            SCRATCHCARDS[i] += 1 * multiplier
        else:
            SCRATCHCARDS[i] = 1 * multiplier


def calculate_wins(winning: set, have: set) -> int:
    intersection = winning & have  # Calculate the intersection

    '''
      Return the number of wins 
      Win more scratchcards equal to the number of winning numbers you have 
    '''
    return len(intersection)


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            for line in file:
                line = line.strip()

                # Get the Card Label and Info
                card_label, card_info = line.split(':')

                # Get the Card ID
                _, card_id = card_label.strip().split()
                try:
                    card_id = int(card_id)
                except ValueError as e:
                    print(f"Invalid card ID: {e}")
                    continue

                # Get the Card numbers
                winning_numbers, nums_i_have = card_info.strip().split('|')

                # Convert to sets
                set_winning_numbers = set(winning_numbers.strip().split())
                set_nums_i_have = set(nums_i_have.strip().split())

                # Add the current card
                add_card(card_id)

                # Calculate Wins
                wins = calculate_wins(set_winning_numbers, set_nums_i_have)
                if wins != 0:
                    collect_wins(card_id, wins)

            print(
                f"The total number of scratchcards: {sum(SCRATCHCARDS.values())}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
