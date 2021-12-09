#!/usr/bin/env python

'''
Advent of Code 2021 - Day 1: Sonar Sweep
https://adventofcode.com/2021/day/1
'''

filename = input("What is the input file name? ")

depths = []
index = 0 
increases = 0
try:
    with open(filename, "r") as file:
        for line in file:
            depth = int(line.strip())
            depths.append(depth)
            index += 1
            if index == 1:
                print(f"{depth} (N/A - no previous measurement)")
                continue

            if depths[index-1] > depths[index-2]:
                print(f"{depth} (increased)")
                increases += 1
            else:
                print(f"{depth} (decreased)")
    print(f"There are {increases} measurements that are larger than the previous measurement.")
except FileNotFoundError as e:
    print(f"No such file or directory: '{filename}'")
