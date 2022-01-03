#!/usr/bin/env python

'''
Advent of Code 2021 - Day 20: Trench Map (Part 1)
https://adventofcode.com/2021/day/20
'''


import time
import numpy as np


class ImageMap():
    def __init__(self, algorithm: list) -> None:
        self._grid = np.array([])
        self._algorithm = algorithm

    def add_row(self, row):
        np_row = np.array(row)
        if self._grid.size != 0:
            self._grid = np.vstack([self._grid, np_row])
        else:
            self._grid = np_row

    def _neighbors(self, radius, coordinates=(0, 0)):  # Includes the center coordinates
        neighbors = []
        row = coordinates[0]
        column = coordinates[1]

        for j in range(column - radius, column + radius + 1):
            for i in range(row - radius, row + radius + 1):
                neighbors.append((i, j))

        # Sort so we can iterate from left to right and top to bottom
        return sorted(neighbors, key=lambda s: (s[0], s[1]))

    def _inbounds(self, row, column):
        return 0 <= row < len(self._grid) and 0 <= column < len(self._grid[0])

    def _pixel_str_to_pixel(self, pixel_str: str) -> str:
        bin_lst = [1 if pixel == '#' else 0 for pixel in pixel_str]
        bin_str = ''.join(map(str, bin_lst))
        try:
            dec = int(bin_str, 2)
        except ValueError as e:
            dec = 0
            print(e)

        return self._algorithm[dec]

    def enhance(self, infinite_pixel_on=False):
        new_image_map = ImageMap(self._algorithm)

        # Add the upper border for 1 pixel expansion
        rows, cols = self._grid.shape
        infinite_pixel = '.' if self._algorithm[0] == '.' else '#' if not infinite_pixel_on else '.'
        new_image_map.add_row([infinite_pixel] * (cols + 2))

        for r in range(0, rows):
            row = [infinite_pixel]
            for c in range(0, cols):
                # Find the neighbors and get their value to create the 9-char pixel string
                pixel_str = ''
                neighbors = self._neighbors(radius=1, coordinates=(r, c))
                for x, y in neighbors:
                    pixel = self._grid[(x, y)] if self._inbounds(
                        row=x, column=y) else '#' if infinite_pixel_on else '.'
                    pixel_str += pixel

                # Convert the pixel string to a pixel based on the image enhancement algorithm
                pixel = self._pixel_str_to_pixel(pixel_str)

                # Add the pixel to the row for the new image map
                row.extend(pixel)

            row.extend(infinite_pixel)
            new_image_map.add_row(row)

        # Add the lower border for 1 pixel expansion
        _, cols = new_image_map.size
        new_image_map.add_row([infinite_pixel] * cols)

        return new_image_map

    def lit_pixel_count(self) -> int:
        result = np.where(self._grid == '#')
        return len(list(zip(result[0], result[1])))

    @property
    def size(self) -> tuple:
        return self._grid.shape

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            for elem in row:
                output = output + f"{elem:>3}"
            output = output + "\n"
        return output


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            rules = []
            image_map = None
            algorithm = True

            for line in file:
                line = line.strip()

                if not line:
                    algorithm = False
                    continue

                if algorithm:
                    rules.extend(list(line))
                    continue

                if not image_map:
                    image_map = ImageMap(rules)

                    # Add the upper border for 1 pixel expansion
                    input_row = ['.'] * (len(line) + 2)
                    image_map.add_row(input_row)

                input_row = ['.'] + list(line) + ['.']  # Add the side border
                image_map.add_row(input_row)

        # Add the lower border
        _, cols = image_map.size
        image_map.add_row(['.'] * cols)

        start = time.time()
        for i in range(2):
            # Infinite pixels are on in the odd iteration
            infinite_on = False if rules[0] == '.' else True if i % 2 == 1 else False
            image_map = image_map.enhance(infinite_on)
        end = time.time()
        print(f"\nNumber of lit pixels: {image_map.lit_pixel_count()}")
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
