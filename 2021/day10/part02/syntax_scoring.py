#!/usr/bin/env python

'''
Advent of Code 2021 - Day 10: Syntax Scoring (Part 2)
https://adventofcode.com/2021/day/10
'''


from queue import LifoQueue
from statistics import median

OPEN_CHARS = ['(', '[', '{', '<']


def scoring(char):
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    return points.get(char, 0)


def get_paired_char(char):
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<',
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }

    return pairs.get(char, None)


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            scores = []

            # Read the lines and check the syntax
            for line in file:
                line = line.strip()

                stack = LifoQueue()
                corrupted = False
                for char in line:
                    if char in OPEN_CHARS:
                        # Push to the stack
                        stack.put(char)
                        continue

                    # Pop the stack
                    stack_char = stack.get()
                    if stack_char != get_paired_char(char):
                        print(
                            f"{line:30} - Expected {get_paired_char(stack_char)}, but found {char} instead.")
                        corrupted = True
                        break

                if not corrupted:
                    # Get the symbols needed for completion
                    completion_chars = []
                    score = 0
                    while not stack.empty():
                        stack_char = stack.get()
                        completion_chars.append(get_paired_char(stack_char))
                        score *= 5
                        score += scoring(get_paired_char(stack_char))
                    scores.append(score)
                    print(
                        f"{''.join(completion_chars):>30} - {score} Total points.")

            # Sort the scores
            scores.sort()
            print(f"\nThe middle score: {median(scores)}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
