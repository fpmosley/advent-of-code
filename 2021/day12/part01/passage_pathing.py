#!/usr/bin/env python

'''
Advent of Code 2021 - Day 12: Passage Pathing (Part 1)
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
            self._paths.append(path) # Reached the end of the path. Add to list of paths.
            return

        caves = self._find_cave_connections(name=name)
        for cave in caves:
            if cave.islower() and cave in path:  # Check that small caves entered only once
                continue

            self._traverse(name=cave, path=path.copy())

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
