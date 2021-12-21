#!/usr/bin/env python

'''
Advent of Code 2021 - Day 14: Extended Polymerization (Part 1)
https://adventofcode.com/2021/day/14
'''


import re
import time
from collections import Counter

RULES = {}


def process_template(polymer):
    if not polymer:
        return polymer

    new_polymer = polymer[0]
    for index, _ in enumerate(polymer):
        try:
            pair = polymer[index] + polymer[index + 1]
            insertion = RULES[pair]
            new_polymer += insertion + polymer[index + 1]
        except KeyError:
            print(f"Pair insertion rule not found for '{pair}'")
            continue
        except IndexError:
            break

    return new_polymer


def print_frequency(polymer):
    print("\nFrequency of elements:")
    frequency = Counter(polymer).most_common()
    for element, count in frequency:
        print(f"'{element}':\t{count:>6}")


def most_common(polymer):
    return Counter(polymer).most_common(1)[0]


def least_common(polymer):
    return Counter(polymer).most_common()[-1]


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
        for step in range(steps):
            polymer_template = process_template(polymer=polymer_template)
            print(f"After step {step + 1}: {polymer_template}")
        end = time.time()

        print_frequency(polymer_template)
        most_frequent = most_common(polymer=polymer_template)
        least_frequent = least_common(polymer=polymer_template)
        print(
            f"\nDifference between most and least common: {most_frequent[1] - least_frequent[1]}\n")
        print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError:
        print("Please enter a valid integer.")


if __name__ == "__main__":
    main()
