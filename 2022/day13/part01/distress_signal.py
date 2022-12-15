#!/usr/bin/env python

'''
Advent of Code 2022 - Day 12: Distress Signal (Part 1)
https://adventofcode.com/2022/day/13

Solution makes use of recursion to process the packet pairs.
'''

import time
from ast import literal_eval
from collections import deque


def compare_ints(left_item: int, right_item: int) -> bool:
    if left_item < right_item:
        return True
    elif left_item > right_item:
        return False
    return None


def process_items(left_item: any, right_item: any) -> bool:
    if type(left_item) == int and type(right_item) == int: # Check if we have two integers
        result = compare_ints(left_item=left_item, right_item=right_item)
        if result != None:
            return result
        return None
    elif type(left_item) == list and type(right_item) == list: # Check if we have two lists
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


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Create list for pairs in correct order
            pairs_in_correct_order = []

            # Read the lines and process the pairs
            pairs_of_packets = []
            pair_count = 0
            for line in file:
                line = line.strip()

                if not line:
                    pair_count += 1
                    if packets_in_order(pairs=pairs_of_packets):
                        pairs_in_correct_order.append(pair_count)
                    pairs_of_packets = []  # Reset the list of pairs of packets
                    continue

                pair = literal_eval(line)
                pairs_of_packets.append(pair)

            end = time.time()
            print(
                f"\nThe sum of the indicies of packet pairs in correct order: {sum(pairs_in_correct_order)}\n")
            print(f"Execution time in seconds: {end - start}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
