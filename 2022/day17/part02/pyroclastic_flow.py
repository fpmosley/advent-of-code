#!/usr/bin/env python

'''
Advent of Code 2022 - Day 17: Pyroclastic Flow (Part 2)
https://adventofcode.com/2022/day/17
'''
from dataclasses import dataclass
from enum import Enum
from itertools import cycle
import time

CHAMBER_WIDTH = 7

# Initialize floor and map
floor = [(0, x) for x in range(CHAMBER_WIDTH)]
map = set(floor)
top = 0

rock_count = num_cycles = cycle_height_incr = 0


class SHAPES(Enum):
    HORIZONTAL_BAR = 1
    CROSS = 2
    REVERSE_L = 3
    VERTICAL_BAR = 4
    CUBE = 5


shapes = cycle(enumerate([SHAPES.HORIZONTAL_BAR, SHAPES.CROSS,
                          SHAPES.REVERSE_L, SHAPES.VERTICAL_BAR, SHAPES.CUBE]))


@dataclass
class Shape():
    top: int
    left: int
    right: int
    bottom: int

    def move_left(self):
        if self.left == 0:
            return

        self.left -= 1
        self.right -= 1

    def move_right(self):
        if self.right == CHAMBER_WIDTH - 1:
            return

        self.left += 1
        self.right += 1

    def move_down(self):
        self.bottom -= 1
        self.top -= 1

    def points(self):
        return []


class HorizontalBar(Shape):
    def __init__(self, top):
        self.left = 2
        self.right = 5
        self.bottom = top + 4
        self.top = self.bottom

    def points(self) -> list:
        return sorted([(self.bottom, x) for x in range(self.left, self.right + 1)])


class Cross(Shape):
    def __init__(self, top):
        self.left = 2
        self.right = 4
        self.bottom = top + 4
        self.top = self.bottom + 2

    def points(self) -> list:
        points = [(self.bottom + 1, x)
                  for x in range(self.left, self.right + 1)]
        points.append((self.bottom, self.left + 1))
        points.append((self.top, self.left + 1))
        return sorted(points)


class ReverseL(Shape):
    def __init__(self, top):
        self.left = 2
        self.right = 4
        self.bottom = top + 4
        self.top = self.bottom + 2

    def points(self) -> list:
        h_positions = [(self.bottom, x)
                       for x in range(self.left, self.right + 1)]
        v_positions = [(y, self.right) for y in range(
            self.bottom, self.top + 1)]
        return sorted(h_positions + v_positions)


class VerticalBar(Shape):
    def __init__(self, top):
        self.left = 2
        self.right = 2
        self.bottom = top + 4
        self.top = self.bottom + 3

    def points(self) -> list:
        return sorted([(y, self.left) for y in range(self.bottom, self.top + 1)])


class Cube(Shape):
    def __init__(self, top):
        self.left = 2
        self.right = 3
        self.bottom = top + 4
        self.top = self.bottom + 1

    def points(self) -> list:
        return sorted([(self.bottom, self.left), (self.bottom, self.right), (self.top, self.left), (self.top, self.right)])


def get_rock() -> tuple:
    shape_index, shape = next(shapes)
    match shape:
        case SHAPES.HORIZONTAL_BAR:
            rock = HorizontalBar(top)
        case SHAPES.CROSS:
            rock = Cross(top)
        case SHAPES.REVERSE_L:
            rock = ReverseL(top)
        case SHAPES.VERTICAL_BAR:
            rock = VerticalBar(top)
        case SHAPES.CUBE:
            rock = Cube(top)
        case _:
            rock = HorizontalBar(top)
    return shape_index, rock


def get_formation(map: set, top: int) -> str:
    """Convert the recent formation into a string representation"""
    rows = []
    min_y = max(0, top-20)  # we want the last 20 rows
    for y in range(min_y, top+1):
        line = ""
        for x in range(0, CHAMBER_WIDTH):
            if (y, x) in map:
                line += '#'
            else:
                line += '.'

        rows.append(line)

    return "\n".join(rows[::-1])


def can_move_left(rock: Shape, map: set) -> bool:
    if rock.left == 0:
        return False

    for point in rock.points():
        row, col = point
        if (row, col - 1) in map:
            return False

    return True


def can_move_right(rock: Shape, map: set) -> bool:
    if rock.right == CHAMBER_WIDTH - 1:
        return False

    for point in rock.points():
        row, col = point
        if (row, col + 1) in map:
            return False

    return True


def can_fall_down(rock: Shape, map: set) -> bool:

    for point in rock.points():
        row, col = point
        if (row - 1, col) in map:
            return False

    return True


def drop_next_shape(jet_pattern: cycle):
    global top, rock_count

    jet_index = 0
    rock_index, rock = get_rock()
    rock_count += 1
    for index, direction in jet_pattern:
        # Push the rock
        match direction:
            case '<':
                if can_move_left(rock=rock, map=map):
                    rock.move_left()
            case '>':
                if can_move_right(rock=rock, map=map):
                    rock.move_right()

        # Can we fall down?
        if can_fall_down(rock=rock, map=map):
            rock.move_down()
        else:
            # Add the rock to the map and get top
            map.update(rock.points())
            top = max(rock.top, top)
            jet_index = index
            break

    return rock_index, jet_index


def main():

    filename = input("What is the input file name? ")

    try:
        limit = int(input("How many rocks to simulate? "))

        with open(filename, "r") as file:

            start = time.time()

            # Read the jet pattern
            content = file.read()
            jet_pattern = cycle(enumerate(content.strip()))

            # Initialize cache of seen patterns for recognizing a cycle
            # K=(rock_idx, jet_idx, rock_formation): V=(height, rock_count)
            cache = {}

            while True:
                rock_index, jet_index = drop_next_shape(jet_pattern)

                key = (rock_index, jet_index, get_formation(map, top))
                if key in cache:
                    break
                else:  # cache miss, so add new entry to the cache
                    cache[key] = (top, rock_count)

        # Number of drops to reach cycle start
        offset = cache[key][1]
        offset_height = cache[key][0]  # height at cycle start
        cycle_length = rock_count-offset
        cycle_height_incr = top-offset_height  # height increment each cycle
        num_cycles, remainder = divmod(
            1000000000000-offset, cycle_length)

        for _ in range(remainder):
            drop_next_shape(jet_pattern)

        max_height = top + (num_cycles-1)*cycle_height_incr
        print(
            f"After {limit} rocks have stopped the tower height is: {max_height}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except ValueError:
        print("Please enter a valid integer for the simulation limit.")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
