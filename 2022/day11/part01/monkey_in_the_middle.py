#!/usr/bin/env python

'''
Advent of Code 2022 - Day 11: Monkey In The Middle (Part 1)
https://adventofcode.com/2022/day/11
'''

from collections import OrderedDict, deque
import time
import re
from dataclasses import dataclass


@dataclass
class Monkey:
    number: int
    items: deque
    operation: str
    divisor: int
    true_throw_to: int
    false_throw_to: int
    num_inspected: int = 0

    def add_item(self, item):
        self.items.append(item)

    def inspect(self, monkeys: dict):
        while self.items:
            item = self.items.popleft()
            self.num_inspected += 1
            # Evaluate the string operation as an expression
            def f(old): return eval(self.operation)
            worry_level = f(item)  # Change the worry level
            worry_level = worry_level // 3  # Floor division
            throw_to = self.true_throw_to if worry_level % self.divisor == 0 else self.false_throw_to
            monkeys[throw_to].add_item(worry_level)  # Throw item to monkey


def create_monkey(note: re.Match) -> Monkey:
    monkey_no = int(note.group(1))
    items = note.group(2).split(',')
    items = [int(item) for item in items]  # Convert items to integers
    operation = note.group(3)
    divisor = int(note.group(4))
    true = int(note.group(5))
    false = int(note.group(6))

    return Monkey(number=monkey_no, items=deque(
        items), operation=operation, divisor=divisor, true_throw_to=true, false_throw_to=false)


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            monkeys = {}

            # Read the notes
            note = ''
            for line in file:
                # Process note if a blank line
                if line == '\n':
                    # Generated regex using regex101.com (https://regex101.com/r/hLTCaG/1)
                    result = re.search(
                        "^Monkey (\d){1}:\n^\s+Starting items: ([\d,\s]+)\n^\s+Operation: new = (.+)\n^\s+Test: divisible by (\d+)\n^\s+If true: throw to monkey (\d+)\n^\s+If false: throw to monkey (\d)+$", note, re.MULTILINE)
                    if not result:
                        print("Could not find an observation note for a monkey")
                        continue

                    monkey = create_monkey(result)
                    monkeys[monkey.number] = monkey
                    note = ''  # reset to blank
                    continue

                note += line

            # Add the last monkey note
            result = re.search(
                "^Monkey (\d){1}:\n^\s+Starting items: ([\d,\s]+)\n^\s+Operation: new = (.+)\n^\s+Test: divisible by (\d+)\n^\s+If true: throw to monkey (\d+)\n^\s+If false: throw to monkey (\d)+$", note, re.MULTILINE)
            if result:
                monkey = create_monkey(result)
                monkeys[monkey.number] = monkey

            # Sort the monkeys into ascending order
            monkeys = OrderedDict(sorted(monkeys.items()))

            for round in range(20):  # Inspect over 20 rounds
                for _, monkey in monkeys.items():
                    monkey.inspect(monkeys)

            num_inspected = []
            for _, monkey in monkeys.items():
                num_inspected.append(monkey.num_inspected)
                print(
                    f"Monkey {monkey.number} inspected items {monkey.num_inspected} times.")

            num_inspected = sorted(num_inspected, reverse=True)
            print(
                f"The level of monkey business: {num_inspected[0] * num_inspected[1]}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
