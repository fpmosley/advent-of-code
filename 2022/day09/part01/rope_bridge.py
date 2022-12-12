#!/usr/bin/env python

'''
Advent of Code 2022 - Day 9: Rope Bridge (Part 1)
https://adventofcode.com/2022/day/9
'''

from enum import Enum
import time
from typing import Tuple

TAIL_POSITIONS = {(0, 0)}


class DIRECTION(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# The move functions use a Cartesian Coordinate system
def move_up(head: list, tail: list, steps: int) -> Tuple:
    count = 1
    while count <= steps:
        head[0] += 1
        tail = move_tail(head=head, tail=tail, direction=DIRECTION.UP)
        count += 1
    return head, tail


def move_down(head: list, tail: list, steps: int) -> Tuple:
    count = 1
    while count <= steps:
        head[0] -= 1
        tail = move_tail(head=head, tail=tail, direction=DIRECTION.DOWN)
        count += 1
    return head, tail


def move_left(head: list, tail: list, steps: int) -> Tuple:
    count = 1
    while count <= steps:
        head[1] -= 1
        tail = move_tail(head=head, tail=tail, direction=DIRECTION.LEFT)
        count += 1
    return head, tail


def move_right(head: list, tail: list, steps: int) -> Tuple:
    count = 1
    while count <= steps:
        head[1] += 1
        tail = move_tail(head=head, tail=tail, direction=DIRECTION.RIGHT)
        count += 1
    return head, tail


def calc_adjacent_positions(coordinate: list) -> list:
    row, col = coordinate
    return [(i, j) for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)]


def move_tail(head: list, tail: list, direction: DIRECTION) -> list:
    """Move the tail knot in the given direction"""
    match direction:
        case DIRECTION.UP:
            adjacent_positions = calc_adjacent_positions(tail)
            if tuple(head) not in adjacent_positions:
                # Move tail to be adjacent to head
                TAIL_POSITIONS.add((head[0] - 1, head[1]))
                return [head[0] - 1, head[1]]
            return tail  # Head is adjacent to tail
        case DIRECTION.DOWN:
            adjacent_positions = calc_adjacent_positions(tail)
            if tuple(head) not in adjacent_positions:
                # Move tail to be adjacent to head
                TAIL_POSITIONS.add((head[0] + 1, head[1]))
                return [head[0] + 1, head[1]]
            return tail  # Head is adjacent to tail
        case DIRECTION.LEFT:
            adjacent_positions = calc_adjacent_positions(tail)
            if tuple(head) not in adjacent_positions:
                # Move tail to be adjacent to head
                TAIL_POSITIONS.add((head[0], head[1] + 1))
                return [head[0], head[1] + 1]
            return tail  # Head is adjacent to tail
        case DIRECTION.RIGHT:
            adjacent_positions = calc_adjacent_positions(tail)
            if tuple(head) not in adjacent_positions:
                # Move tail to be adjacent to head
                TAIL_POSITIONS.add((head[0], head[1] - 1))
                return [head[0], head[1] - 1]
            return tail  # Head is adjacent to tail


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Create the head and tail knots
            head = [0, 0]
            tail = [0, 0]

            # Read the motions and move the knots
            for line in file:
                line = line.strip()

                direction, steps = line.split()
                steps = int(steps)

                match direction:
                    case "U":
                        head, tail = move_up(head, tail, steps)
                    case "D":
                        head, tail = move_down(head, tail, steps)
                    case "L":
                        head, tail = move_left(head, tail, steps)
                    case "R":
                        head, tail = move_right(head, tail, steps)
                    case _:
                        print(f"Direction '{direction}' is invalid")
                        continue

        end = time.time()
        print(f"Tail rope positions: {TAIL_POSITIONS}")
        print(f"Number of tail rope positions: {len(TAIL_POSITIONS)}")
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
