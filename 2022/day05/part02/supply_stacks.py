#!/usr/bin/env python

'''
Advent of Code 2022 - Day 05: Supply Stacks (Part 2)
https://adventofcode.com/2022/day/5
'''

import re
import time
from collections import deque, OrderedDict

STACKS = {}

def move_crates(step: str):
    result = re.search(r"move (\d+) from (\d+) to (\d+)", step)
    if not result:
        return

    num_of_crates = int(result.group(1))
    source = int(result.group(2))
    destination = int(result.group(3))

    stack = deque()
    for _ in range(num_of_crates):
        try:
            crate = STACKS[source].pop()
            stack.appendleft(crate)
        except:
            pass

    for crate in stack:
        STACKS[destination].append(crate)

def process_level(level: list):
    for stack_number, crate in enumerate(level):
        stack_number += 1
        if crate.isspace():
            continue

        stack = STACKS.get(stack_number, deque())
        stack.appendleft(crate)
        STACKS[stack_number] = stack

def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Read the lines
            for line in file:
                line = line.rstrip()
                if not line:  # skip the blank line
                    continue

                res = [ele for ele in ['move', '['] if ele in line] # skip stack number line
                if not res:
                    continue

                if 'move' in line:
                    move_crates(line)
                else:
                    n = 4
                    level = [line[idx:idx + n - 1] for idx in range(0, len(line), n)]
                    process_level(level)

        sorted_stacks = OrderedDict(sorted(STACKS.items()))
        top_of_stacks = [stack.pop()[1] for _, stack in sorted_stacks.items()]
        end = time.time()
        print(f"The crates on top of the stacks: {''.join(top_of_stacks)}")
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
