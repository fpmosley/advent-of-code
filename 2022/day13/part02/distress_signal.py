#!/usr/bin/env python

'''
Advent of Code 2022 - Day 12: Distress Signal (Part 2)
https://adventofcode.com/2022/day/13

Sorting problem. Uses a Quicksort algorithm (O(n log2n))
https://en.wikipedia.org/wiki/Quicksort
'''

import time
from ast import literal_eval
from collections import deque
from random import randint


def compare_ints(left_item: int, right_item: int) -> bool:
    if left_item < right_item:
        return True
    elif left_item > right_item:
        return False
    return None


def process_items(left_item: any, right_item: any) -> bool:
    if type(left_item) == int and type(right_item) == int:  # Check if we have two integers
        result = compare_ints(left_item=left_item, right_item=right_item)
        if result != None:
            return result
        return None
    elif type(left_item) == list and type(right_item) == list:  # Check if we have two lists
        index = 0
        while True:
            try:
                ele_left = left_item[index]
            except IndexError:
                if len(left_item) == len(right_item):
                    break  # Ran out of elements in both lists; keep checking input
                return True  # Ran out of elements on the left first; right order

            try:
                ele_right = right_item[index]
            except IndexError:
                return False  # Ran out of elements on the right first; incorrect order
            result = process_items(left_item=ele_left, right_item=ele_right)

            if result != None:
                return result

            index += 1  # increment index and check the next elements in list
    elif type(left_item) == int:  # Only left item is an integer; convert to a list
        left_item = list([left_item])
        return process_items(left_item=left_item, right_item=right_item)
    else:  # Only right item is an integer; convert to a list
        right_item = list([right_item])
        return process_items(left_item=left_item, right_item=right_item)


def packets_in_order(pairs: list) -> bool:
    if not pairs:
        return False

    left = deque(pairs[0])
    right = deque(pairs[1])

    while True:
        # Check if we have run out of items
        try:
            left_item = left.popleft()
        except IndexError:
            if len(right) > 0:
                return True  # Ran out of elements on the left first; right order

        try:
            right_item = right.popleft()
        except IndexError:
            return False  # Ran out of elements on the right first; incorrect order

        # Process the items
        result = process_items(left_item=left_item, right_item=right_item)
        if result != None:
            return result


def quicksort(packets: list) -> list:
    # If the input list contains fewer than two elements,
    # then return it as the result of the function
    if len(packets) < 2:
        return packets

    low, same, high = [], [], []

    # Select your `pivot` element randomly
    pivot = packets[randint(0, len(packets) - 1)]

    for item in packets:
        # Elements that are in the correct order vs. the `pivot` go to
        # the `low` list. Elements that are in the incorrect order vs. the
        # `pivot` go to the `high` list. Elements that are
        # equal to `pivot` go to the `same` list.
        if process_items(left_item=item, right_item=pivot):
            low.append(item)
        elif item == pivot:
            same.append(item)
        else:
            high.append(item)

    # The final result combines the sorted `low` list
    # with the `same` list and the sorted `high` list
    return quicksort(low) + same + quicksort(high)


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Read the lines and process the pairs
            packets = []
            for line in file:
                line = line.strip()

                # Skip the blank lines and combine all packets into a single list
                if not line:
                    continue

                pair = literal_eval(line)
                packets.append(pair)

            # Add the divider packets
            packets.append([[2]])
            packets.append([[6]])

            # Quicksort the packets
            packets = quicksort(packets=packets)

            try:
                decoder_key = (packets.index(
                    [[2]]) + 1) * (packets.index([[6]]) + 1)
                print(
                    f"\nThe decoder key for the distress signal: {decoder_key}\n")
            except ValueError as e:
                print("Unable to find the decoder key: {e}\n")

            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
