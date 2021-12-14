#!/usr/bin/env python

'''
Advent of Code 2021 - Day 3: Binary Diagnostic (Part 1)
https://adventofcode.com/2021/day/3
'''

filename = input("What is the input file name? ")

try:
    total_one_bits = []
    total_zero_bits = []
    most_common_bit = []
    with open(filename, "r") as file:
        # Process the binary numbers
        for lineno, line in enumerate(file):
            bin_lst = list(line.strip())
            if lineno == 0:
                # Making the assumption that all binary numbers are same width
                total_one_bits = [0] * len(bin_lst)
                total_zero_bits = [0] * len(bin_lst)

            for position, bin_digit in enumerate(bin_lst):
                if bin_digit == '1':
                    total_one_bits[position] += 1
                else:
                    total_zero_bits[position] += 1

                # Calculate gamma and epsilon rate
                BIT = '1' if total_one_bits[position] > total_zero_bits[position] else '0'
                try:
                    most_common_bit[position] = BIT
                except IndexError:
                    most_common_bit.insert(position, BIT)

    GAMMA_RATE = ''.join(most_common_bit)
    EPSILON_RATE = ''.join(['1' if i == '0' else '0' for i in GAMMA_RATE])
    print(f"Gamma rate: {GAMMA_RATE} = {int(GAMMA_RATE,2)}")
    print(f"Epsilon rate: {EPSILON_RATE} = {int(EPSILON_RATE,2)}")
    print(f"Power Consumption: {int(GAMMA_RATE, 2) * int(EPSILON_RATE, 2)}")

except FileNotFoundError:
    print(f"No such file or directory: '{filename}'")
