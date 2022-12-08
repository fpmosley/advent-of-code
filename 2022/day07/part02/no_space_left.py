#!/usr/bin/env python

'''
Advent of Code 2022 - Day 7: No Space Left On Device (Part 2)
https://adventofcode.com/2022/day/7
'''

import re
import time
from collections import deque, OrderedDict

class Node:

    def __init__(self, name: str) -> None:
        self._name = name
        self._parent = None

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def path(self):
        path = deque()
        path.appendleft(self._name)
        parent = self._parent
        while parent:
            path.appendleft(parent.name)
            parent = parent.parent
        return "/".join(path)

    def _get_depth(self):
        parent = self._parent
        depth = 0
        while parent:
            depth += 1
            parent = parent.parent
        return depth

class DirNode(Node):

    def __init__(self, name: str) -> None:
        self._children = []
        super().__init__(name)

    def add_node(self, node: Node):
        node.parent = self
        self._children.append(node)

    @property
    def children(self):
        return self._children

    def __repr__(self) -> str:
        if self._name == '/':
            output = f"- {self._name} (dir)\n"

        depth = self._get_depth()
        output = f"{'-':>{depth * 3}} {self._name} (dir)\n"

        for child in self._children:
            output += f"{child}"

        return output

class FileNode(Node):

    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    @property
    def size(self):
        return self._size

    def __repr__(self) -> str:
        depth = self._get_depth()
        return f"{'-':>{depth * 3}} {self._name} (file, size={self._size})\n"

# Initialize the root node and set it as the current working directory node
ROOT = DirNode('/')
CWD = ROOT

DIR_SIZES = {}  # Dict of directory names and sizes

FILESYSTEM_SIZE = 70000000
LEAST_UNUSED_SPACE = 30000000

def change_directory(path: str) -> None:
    """Change the directory"""

    global CWD

    # Move up one level
    if path == "..":
        CWD = CWD.parent
        return

    # Move to the root directory
    if path == "/":
        CWD = ROOT
        return

    for child in CWD.children:
        if child.name == path:
            CWD = child
            return

def get_directory_sizes(node: DirNode) -> int:
    """Calculates the directory sizes starting at the given node."""
    total_size = 0
    for child in node.children:
        if isinstance(child, DirNode):
            total_size += get_directory_sizes(child)
        else:
            total_size += child.size

    path = node.path  # Get the path to use as the key for the dictionary
    print(f"Directory '{path}' size: {total_size}")
    DIR_SIZES[path] = total_size  # Save the directory size in the dictionary
    return total_size

def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            start = time.time()

            # Read the terminal output
            for output in file:
                output = output.strip()

                # Parse the output for a command
                result = re.search(r"^\$ (cd|ls)\s*([\w./]*)", output)
                if result:  # We have a command to execute
                    # Check the command
                    command = result.group(1)
                    if command == 'ls':  # if 'ls' we process the following output
                        continue

                    # Get the path for the 'cd' command and execute
                    path = result.group(2)
                    change_directory(path)
                    continue

                # Parse the output of a directory listing
                result = re.search(r"^(\d+|dir)\s*([\w.]+)", output)
                if not result:
                    continue

                size_or_dir = result.group(1)
                name = result.group(2)
                if size_or_dir == 'dir':
                    CWD.add_node(DirNode(name)) # Add a directory to the CWD node
                else:
                    CWD.add_node(FileNode(name, int(size_or_dir))) # Add a file to the CWD node

        get_directory_sizes(ROOT)
        size = DIR_SIZES.get('/', 0)

        # Calculate the free space of the filesystem
        free_space = FILESYSTEM_SIZE - size
        needed_space = LEAST_UNUSED_SPACE - free_space
        print(f"Free space on filesystem: {free_space}")
        print(f"Space needed for update: {needed_space}")

        # Sort the directory sizes in descending order
        sorted_dir_sized = OrderedDict(sorted(DIR_SIZES.items(), key=lambda x:x[1], reverse=True))

        # Find the first directory size to free up enough space
        previous_size = size
        for _, size in sorted_dir_sized.items():
            if size <= needed_space:
                print(f"Smallest directory size to free up space: {previous_size}")
                break
            previous_size = size

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")

if __name__ == "__main__":
    main()
