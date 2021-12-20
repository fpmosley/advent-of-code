#!/usr/bin/env python

'''
Advent of Code 2021 - Day 12: Passage Pathing (Part 2)
https://adventofcode.com/2021/day/12
'''


class CaveMap():
    def __init__(self) -> None:
        self._paths = []
        self._connections = []

    def add_connection(self, connection=None):
        self._connections.append(connection)

    def find_paths(self):
        self._traverse(name='start')

    def _find_cave_connections(self, name):
        return [connection[0] if connection[0] != name else connection[1] for connection in self._connections if name in connection]

    def _traverse(self, name, path=None):
        if not path:
            path = []

        path.append(name)
        if name == 'end':
            # Reached the end of the path. Add to list of paths.
            self._paths.append(path)
            return

        caves = self._find_cave_connections(name=name)
        for cave in caves:
            if not self.valid_cave(name=cave, path=path):
                continue

            self._traverse(name=cave, path=path.copy())

    # Checks that a single small cave can be visited at most twice, and the remaining small caves can be visited at most once.
    @staticmethod
    def valid_cave(name, path):
        if name == 'start':  # 'start' can only be visited once
            return False

        if name.isupper():  # Large caves are valid
            return True

        if name not in path:  # Small cave is not in the current path
            return True

        # Get list of small caves in the path
        small_caves = [cave for cave in path if cave.islower()]

        # Find the small cave with the max number of occurrences and check if it is the max of 2
        max_small_cave = max(small_caves, key=small_caves.count)
        if small_caves.count(max_small_cave) != 2:
            return True

        return False

    @property
    def paths(self):
        return self._paths


def main():

    filename = input("What is the input file name? ")
    cave_map = CaveMap()
    try:
        with open(filename, "r") as file:
            for line in file:
                entry = line.strip()
                connection = tuple(entry.split("-"))
                cave_map.add_connection(connection)

        cave_map.find_paths()
        paths = cave_map.paths
        for path in paths:
            print(f"{','.join(path)}")
        print(f"\nNumber of paths: {len(paths)}\n")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
