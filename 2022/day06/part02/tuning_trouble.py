#!/usr/bin/env python

'''
Advent of Code 2022 - Day 6: Tuning Trouble (Part 2)
https://adventofcode.com/2022/day/6
'''

import time
from collections import deque

def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            start = time.time()
            num_of_chars = 0
            for line in file:
                buffer = line.strip()

                k = 14  # sliding window size

                # Check first k characters for a marker
                window = deque(buffer[:k])
                if len(set(window)) == k:
                    num_of_chars = k
                    break

                # Create a sliding window of k characters over the buffer
                for i in range(k, len(buffer)):
                    window.popleft()
                    window.append(buffer[i])
                    if len(set(window)) == k:
                        num_of_chars = i + 1  # Add 1 to account for zero-based index
                        break

            print(f"Number of characters processed before first start-of-message marker: {num_of_chars}")
            end = time.time()
            print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
