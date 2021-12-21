#!/usr/bin/env python

'''
Advent of Code 2021 - Day 14: Extended Polymerization (Part 2)
https://adventofcode.com/2021/day/14
'''


import re
import time
from collections import Counter
from functools import cache

RULES = {}


@cache
def process_pair(pair, steps=0):
    if not pair:
        return Counter()

    # Check if we are at the last step
    if steps == 0:
        return Counter()

    try:
        insertion = RULES[pair]

        # Unpack the pair, create new pairs and process the pairs
        first_element, second_element = pair  # Unpack the pair
        return Counter(insertion) + process_pair(pair=first_element + insertion, steps=steps-1) + process_pair(pair=insertion + second_element, steps=steps-1)

    except KeyError:
        print(f"Pair insertion rule not found for '{pair}'")
        return Counter()


def process_template(polymer, steps):
    if not polymer:
        return polymer

    counter = Counter(polymer)
    for index, _ in enumerate(polymer):
        try:
            pair = polymer[index] + polymer[index + 1]
            counter += process_pair(pair=pair, steps=steps)
        except IndexError:
            break

    return counter


def print_frequency(counter):
    print("\nFrequency of elements:")
    frequency = counter.most_common()
    for element, count in frequency:
        print(f"'{element}':\t{count:>6}")


def most_common(counter):
    return counter.most_common(1)[0]


def least_common(counter):
    return counter.most_common()[-1]


def main():

    filename = input("What is the input file name? ")

    try:
        steps = int(input("How many steps to apply? "))
        print()

        with open(filename, "r") as file:

            pattern = r'^(?P<adjacent>[A-Z]{2})\s+->\s+(?P<insertion>[A-Z])'

            # Read the polymer template and pair rules
            for lineno, line in enumerate(file):
                line = line.strip()
                if lineno == 0:
                    polymer_template = line
                    continue

                # Skip blank lines
                if not line:
                    continue

                matches = re.match(pattern, line)
                if matches:
                    adjacent = matches.group('adjacent')
                    insertion = matches.group('insertion')
                    RULES[adjacent] = insertion

        start = time.time()
        counter = process_template(polymer=polymer_template, steps=steps)
        end = time.time()

        print_frequency(counter)
        most_frequent = most_common(counter)
        least_frequent = least_common(counter)
        print(
            f"\nDifference between most and least common: {most_frequent[1] - least_frequent[1]}\n")
        print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError:
        print("Please enter a valid integer.")


if __name__ == "__main__":
    main()
