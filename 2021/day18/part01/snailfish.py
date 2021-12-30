#!/usr/bin/env python

'''
Advent of Code 2021 - Day 18: Snailfish (Part 1)
https://adventofcode.com/2021/day/18
'''


import ast
import time


def is_number(item) -> bool:
    return isinstance(item, int)


def is_pair(item) -> bool:
    if isinstance(item, list) and len(item) == 2 and all(isinstance(x, int) for x in item):
        return True

    return False


def create_index(lst: list) -> list:
    value_index_lst = []

    for indx0, lst0 in enumerate(lst):
        if isinstance(lst0, int):
            value_index_lst.append((lst0, (indx0)))
            continue
        for indx1, lst1 in enumerate(lst0):
            if isinstance(lst1, int):
                value_index_lst.append((lst1, (indx0, indx1)))
                continue
            for indx2, lst2 in enumerate(lst1):
                if isinstance(lst2, int):
                    value_index_lst.append((lst2, (indx0, indx1, indx2)))
                    continue
                for indx3, item in enumerate(lst2):
                    value_index_lst.append(
                        (item, (indx0, indx1, indx2, indx3)))

    return value_index_lst


def explode(first: int, index: list, pair_value: int, numbers: list, leftmost=True):

    if first < 0 or first >= len(index):
        return

    value, location = index[first]
    ispair = False
    if is_pair(value):
        ispair = True
        left_value, right_value = value
        value = left_value if leftmost else right_value
        pair_index = 0 if leftmost else 1

    new_value = value + pair_value

    if len(location) == 1:
        if ispair:
            numbers[location][pair_index] = new_value
        else:
            numbers[location] = new_value
    elif len(location) == 2:
        indx0, indx1 = location
        if ispair:
            numbers[indx0][indx1][pair_index] = new_value
        else:
            numbers[indx0][indx1] = new_value
    elif len(location) == 3:
        indx0, indx1, indx2 = location
        if ispair:
            numbers[indx0][indx1][indx2][pair_index] = new_value
        else:
            numbers[indx0][indx1][indx2] = new_value
    elif len(location) == 4:
        indx0, indx1, indx2, indx3 = location
        if ispair:
            numbers[indx0][indx1][indx2][indx3][pair_index] = new_value
        else:
            numbers[indx0][indx1][indx2][indx3] = new_value


def find_nested_pairs(numbers: list) -> int:
    count = 0
    while True:
        found = False
        index = create_index(numbers)
        for i, (value, location) in enumerate(index):
            # Only pairs nested inside 4 pairs
            if isinstance(value, list) and len(location) == 4:
                found = True

                # Explode the left number of the pair
                explode(first=i - 1, index=index,
                        pair_value=value[0], numbers=numbers, leftmost=False)

                # Explode the right number of the pair
                explode(first=i + 1, index=index,
                        pair_value=value[1], numbers=numbers)

                # Replace the pair with regular number 0
                indx0, indx1, indx2, indx3 = location
                numbers[indx0][indx1][indx2][indx3] = 0
                break

        if found:
            count += 1
            continue

        return count


def split(numbers: list) -> bool:
    index = create_index(numbers)
    for value, location in index:
        # Check if a regular number in a pair, or the regular number is < 10
        if (isinstance(value, list) and value[0] < 10 and value[1] < 10) or value < 10:
            continue

        # We have a number to split. Get the value from the regular number or start with leftmost if a pair
        value = value if not isinstance(
            value, list) else value[0] if value[0] >= 10 else value[1]

        left_value = value // 2  # Divided by two and rounded down
        right_value = value - left_value
        if len(location) == 1:
            numbers[location] = [left_value, right_value]
        elif len(location) == 2:
            indx0, indx1 = location
            numbers[indx0][indx1] = [left_value, right_value]
        elif len(location) == 3:
            indx0, indx1, indx2 = location
            numbers[indx0][indx1][indx2] = [left_value, right_value]
        elif len(location) == 4:
            indx0, indx1, indx2, indx3 = location
            numbers[indx0][indx1][indx2][indx3] = [left_value, right_value]

        return True

    return False


def reduce(numbers: list):
    keep_going = True
    while keep_going:
        # Find nested pairs and explode
        find_nested_pairs(numbers)

        # Split regular numbers greater than 10
        keep_going = split(numbers)


def magnitude(pair):
    if is_number(pair):
        return pair

    left, right = pair
    return 3 * magnitude(left) + 2 * magnitude(right)


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            # Read the snailfish numbers
            final_sum = None
            start = time.time()
            for line in file:
                line = line.strip()
                lst = ast.literal_eval(line)
                print(lst)
                if not final_sum:
                    final_sum = lst
                    continue

                final_sum = [final_sum, lst]
                reduce(final_sum)

        print(f"\nFinal sum: {final_sum}")
        print(f"Magnitude of the final sum: {magnitude(final_sum)}\n")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
