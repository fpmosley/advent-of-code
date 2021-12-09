#!/usr/bin/env python

'''
Advent of Code 2021 - Day 3: Binary Diagnostic (Part 2) 
https://adventofcode.com/2021/day/3
'''

def find_rating(numbers, position, system="oxygen"):
    total_one_bits = 0
    total_zero_bits = 0
    one_bit_nums = []
    zero_bit_nums = []

    # Have we reached the end of the rating calculation?
    if len(numbers) == 1:
        return numbers[0]

    for number in numbers:
        if number[position] == '1':
            total_one_bits += 1
            one_bit_nums.append(number)
        else:
            total_zero_bits += 1
            zero_bit_nums.append(number)

    if system == 'oxygen':
        if total_one_bits >= total_zero_bits:
            return find_rating(one_bit_nums, position + 1, system)
        else: 
            return find_rating(zero_bit_nums, position + 1, system)
    else:
        if total_one_bits < total_zero_bits:
            return find_rating(one_bit_nums, position + 1, system)
        else: 
            return find_rating(zero_bit_nums, position + 1, system)

filename = input("What is the input file name? ")

try:
    with open(filename, "r") as file:
        numbers = file.read().splitlines()
    
    oxygen_generator_rating = find_rating(numbers, 0, 'oxygen')
    co2_scrubber_rating = find_rating(numbers, 0, 'co2')

    print(f"Oxygen generator rating:\t{oxygen_generator_rating} = {int(oxygen_generator_rating,2)}")
    print(f"CO2 scrubber rating:\t\t{co2_scrubber_rating} = {int(co2_scrubber_rating,2)}")
    print(f"Power Consumption:\t\t{int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)}")

except FileNotFoundError as e:
    print(f"No such file or directory: '{filename}'")
