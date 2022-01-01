#!/usr/bin/env python

'''
Advent of Code 2021 - Day 19: Beacon Scanner (Part 2)
https://adventofcode.com/2021/day/19

Got a lot of help from Reddit for this one.

Steps
1. Calculate the distances between all the beacons detected by each scanner.
2. Iterate through each of the scanners. For each, rotate it and compare the
   vectors to the vectors from the base (scanner 0)
3. If there is overlap of at least 12 beacons, then we have found the correct orientation of the scanner.
4. Find the offset. The offset becomes the new coordinates of the test scanner.
5. Use the offset to update the beacons of the test scanner with position relative to the base scanner.
6. Add the updated beacons to the base scanner.
7. Calculate the max Manhattan distance.
'''


import re
import time
from collections import deque, defaultdict
from copy import copy
from itertools import product, combinations, starmap

OVERLAP_THRESHOLD = 11
ROTATIONS = 24


class Scanner():

    def __init__(self, sid) -> None:
        self.sid = sid
        self.position = (0, 0, 0)

        # Beacons from the input
        self.beacons = None

        # Vectors (distances in a given direction) from a beacon to all other detected beacons
        self.vectors = None

    def calculate_vectors(self) -> None:
        pairs = combinations(self.beacons, 2)
        vectors = defaultdict(set)

        for beacon1, beacon2 in pairs:
            vectors[beacon1].add(self._distance(beacon1, beacon2))
            vectors[beacon2].add(self._distance(beacon2, beacon1))

        self.vectors = vectors

    @staticmethod
    def _distance(beacon1: tuple, beacon2: tuple) -> tuple:
        x1, y1, z1 = beacon1
        x2, y2, z2 = beacon2

        return ((x2 - x1), (y2 - y1), (z2 - z1))

    def rotate(self, i: int) -> None:
        rotated_beacons = [self._rotations(beacon, i)
                           for beacon in self.beacons]
        self.beacons = rotated_beacons
        self.calculate_vectors()

    '''
    The puzzle stated 24 permutations. In my mind, I calculated 48 (positive/negative over 3 axis = 8 * 6 directions) 
    
    Here are some explanations of why there are 24:

    https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp54e16/?utm_source=share&utm_medium=web2x&context=3
    https://en.wikipedia.org/wiki/Cross_product
    https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp54okv/?utm_source=share&utm_medium=web2x&context=3
    '''
    @staticmethod
    def _rotations(beacon, i) -> tuple:
        x, y, z = beacon
        rotates = [
            (x, y, z),
            (z, y, -x),
            (-x, y, -z),
            (-z, y, x),
            (-x, -y, z),
            (-z, -y, -x),
            (x, -y, -z),
            (z, -y, x),
            (x, -z, y),
            (y, -z, -x),
            (-x, -z, -y),
            (-y, -z, x),
            (x, z, -y),
            (-y, z, -x),
            (-x, z, y),
            (y, z, x),
            (z, x, y),
            (y, x, -z),
            (-z, x, -y),
            (-y, x, z),
            (-z, -x, y),
            (y, -x, z),
            (z, -x, -y),
            (-y, -x, -z)
        ]

        return rotates[i]


def manhattan(scanner1: Scanner, scanner2: Scanner) -> tuple:
    x1, y1, z1 = scanner1.position
    x2, y2, z2 = scanner2.position

    return (scanner1.sid, scanner2.sid), abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


def find_overlaps(scanner1: Scanner, scanner2: Scanner) -> tuple:
    beacon_pairs = product(scanner1.beacons, scanner2.beacons)
    for beacon1, beacon2 in beacon_pairs:
        v1 = scanner1.vectors[beacon1]
        v2 = scanner2.vectors[beacon2]
        overlap = len(v1 & v2)
        if overlap >= OVERLAP_THRESHOLD:
            return (beacon1[0] - beacon2[0], beacon1[1] - beacon2[1], beacon1[2] - beacon2[2])

    return None


def find_beacons(scanners: deque) -> int:

    base = scanners.popleft()

    while scanners:
        overlap_found = False
        compare_scanner = scanners.popleft()

        for i in range(ROTATIONS):
            rotated_scanner = copy(compare_scanner)
            rotated_scanner.rotate(i)
            offset = find_overlaps(base, rotated_scanner)

            if offset:
                overlap_found = True

                new_beacons = []
                for beacon in rotated_scanner.beacons:
                    x, y, z = beacon
                    ox, oy, oz = offset
                    offset_beacon = (x + ox, y + oy, z + oz)
                    new_beacons.append(offset_beacon)

                base.beacons = list(set(base.beacons + new_beacons))
                base.calculate_vectors()

                # Set the new scanner position relative to base scanner
                compare_scanner.position = offset

                break

        if not overlap_found:
            scanners.append(compare_scanner)

    return len(set(base.beacons))


def find_max_distance(scanners: list) -> tuple:
    return max(starmap(manhattan, combinations(scanners, 2)), key=lambda item: item[1])


def main():

    filename = input("What is the input file name? ")
    print()

    try:
        with open(filename, "r") as file:

            scanners = []
            scanner = None
            beacons = None
            pattern = r'---\s+scanner\s+(?P<id>-?\d+)\s+---'
            for line in file:
                line = line.strip()

                if not line:
                    continue

                matches = re.match(pattern, line)
                if matches:
                    if scanner and beacons:
                        scanner.beacons = beacons
                    scanner_id = int(matches.group('id'))
                    scanner = Scanner(scanner_id)
                    scanners.append(scanner)
                    beacons = []
                    continue

                beacon = tuple(int(x) for x in line.split(','))
                beacons.append(beacon)

        scanner.beacons = beacons

        # Calculate the vectors for each scanner's beacons
        start = time.time()
        for scanner in scanners:
            scanner.calculate_vectors()

        scanners_deque = deque(scanners)

        print(f"Number of beacons: {find_beacons(scanners_deque)}")
        scanner_tuple, distance = find_max_distance(scanners)
        print(
            f"Largest Mahanttan distance is {distance} between scanner {scanner_tuple[0]} and scanner {scanner_tuple[1]}\n")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
