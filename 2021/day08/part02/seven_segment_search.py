#!/usr/bin/env python

'''
Advent of Code 2021 - Day 8: Seven Segment Search (Part 2)
https://adventofcode.com/2021/day/8
'''

PATTERNS = {}
PATTERNS_BY_LENGTH = {}

'''
Digits
0 = 6 segements
1 = 2 segements
2 = 5 segements
3 = 5 segements
4 = 4 segements
5 = 5 segements
6 = 6 segements
7 = 3 segements
8 = 7 segements
9 = 6 segements
'''

'''
Digits 1, 4, 7, and 8 each use a unique number of segments.
1 = 2 segements
4 = 4 segements
7 = 3 segements
8 = 7 segements
'''
def process_patterns(patterns):
    global PATTERNS
    global PATTERNS_BY_LENGTH

    # For unique digits
    segments_to_digits = {
        2: 1,
        4: 4,
        3: 7,
        7: 8
    }

    for pattern in patterns:
        length = len(pattern)
        if length in segments_to_digits.keys():
            PATTERNS[sort_pattern(pattern)] = segments_to_digits.get(length)
        else:
            pattern_list = PATTERNS_BY_LENGTH.get(length, [])
            pattern_list.append(pattern)
            PATTERNS_BY_LENGTH[length] = pattern_list


def get_pattern_by_digit(lookup_value):
    lst = [pattern for pattern, digit in PATTERNS.items() if digit ==
           lookup_value]
    return ''.join(lst)


def sort_pattern(pattern):
    return ''.join(sorted(pattern))


'''
Anaylsis Steps:
1. Find unique digits and patterns by number of segments
2. Subtract three 6 segments from 1. 1 result in diff is 6. Segments known: right top and bottom. Digits known: 1, 4, 6, 7, 8 
3. Subtract 2 remaining 6 segments from 4. 1 diff result = 0; empty = 9  Digits known: 0, 1, 4, 6, 7, 8, 9
4. Subtract three 5 segments from 1. Empty result is 3. Digits known: 0, 1, 3, 4, 6, 7, 8, 9
5. Check 2 remaining 5 segments for RB. If RB segment digit in pattern, digit is 5 else is 2. Digits known: ALL
'''
def analysis():

    # Steps 2 and 3
    digit_one = set(get_pattern_by_digit(1))
    digit_four = set(get_pattern_by_digit(4))
    right_top = None
    right_bottom = None
    for pattern in PATTERNS_BY_LENGTH[6]:
        pattern_len_six = set(pattern)
        diff = digit_one - pattern_len_six
        if diff:
            right_top = ''.join(diff)
            result_list = [
                segment for segment in digit_one if segment != right_top]
            right_bottom = ''.join(result_list)
            PATTERNS[sort_pattern(pattern)] = 6
        else:
            diff = digit_four - pattern_len_six
            if diff:
                PATTERNS[sort_pattern(pattern)] = 0
            else:
                PATTERNS[sort_pattern(pattern)] = 9

    # Steps 4 and 5
    for pattern in PATTERNS_BY_LENGTH[5]:
        pattern_len_five = set(pattern)
        diff = digit_one - pattern_len_five
        if diff and right_bottom in pattern:
            PATTERNS[sort_pattern(pattern)] = 5
        elif diff:
            PATTERNS[sort_pattern(pattern)] = 2
        else:
            PATTERNS[sort_pattern(pattern)] = 3


def decode(output_values):
    decoded = [str(PATTERNS.get(sort_pattern(pattern)))
               for pattern in output_values]
    return int(''.join(decoded))


def reset():
    global PATTERNS
    global PATTERNS_BY_LENGTH
    PATTERNS = {}
    PATTERNS_BY_LENGTH = {}


def main():
    filename = input("What is the input file name? ")
    try:
        total_entry_value = 0
        with open(filename, "r") as file:

            # Read the entries
            for line in file:
                first_part, second_part = line.split('|')
                patterns = first_part.strip().split()
                output_values = second_part.strip().split()

                # Step 1
                reset()
                process_patterns(patterns)

                # Steps 2-5
                analysis()

                decoded_value = decode(output_values)
                total_entry_value += decoded_value
                print(f"{' '.join(output_values):<31}: {decoded_value}")

        print(f"\nTotal of entry values: {total_entry_value}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
