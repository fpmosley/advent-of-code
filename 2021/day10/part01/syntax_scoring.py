#!/usr/bin/env python

'''
Advent of Code 2021 - Day 10: Syntax Scoring (Part 1)
https://adventofcode.com/2021/day/10
'''


from queue import LifoQueue

OPEN_CHARS = ['(', '[', '{', '<']


def scoring(illegal_char):
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    return points.get(illegal_char, 0)


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

            score = 0

            # Read the lines and check the syntax
            for line in file:
                line = line.strip()

                stack = LifoQueue()
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
                        score += scoring(char)
                        break

            print(f"\nTotal syntax error score: {score}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
