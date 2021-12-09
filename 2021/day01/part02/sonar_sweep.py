#!/usr/bin/env python

'''
Advent of Code 2021 - Day 1: Sonar Sweep
https://adventofcode.com/2021/day/1
'''

def window_measurement(depths, count):
    sum = 0
    for i in range(1, 4):
        sum += depths[count-i]
    return sum

def main():
    filename = input("What is the input file name? ")

    depths = []
    measurement_count = 0 
    increases = 0

    try:
        with open(filename, "r") as file:
            for line in file:
                depth = int(line.strip())
                depths.append(depth)
                measurement_count += 1
                if measurement_count == 3: 
                    window_sum = window_measurement(depths, measurement_count)
                    print(f"{window_sum} (N/A - no previous sum)")
                    continue
                elif measurement_count >= 4:
                    previous_window_sum = window_measurement(depths, measurement_count-1)
                    current_window_sum = window_measurement(depths, measurement_count)

                    if current_window_sum > previous_window_sum: 
                        print(f"{current_window_sum} (increased)")
                        increases += 1
                    elif current_window_sum == previous_window_sum: 
                        print(f"{current_window_sum} (no change)")
                    else:
                        print(f"{current_window_sum} (decreased)")
        print(f"There are {increases} sums that are larger than the previous sum.")
    except FileNotFoundError as e:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
