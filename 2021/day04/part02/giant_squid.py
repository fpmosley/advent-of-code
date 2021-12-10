#!/usr/bin/env python

'''
Advent of Code 2021 - Day 4: Giant Squid (Part 2)
https://adventofcode.com/2021/day/4
'''

import sys
import numpy as np


class Board():
    def __init__(self) -> None:
        self._board_marked = np.full((5, 5), False)  # input is a 5x5 grid
        self._board_nums = np.array([])

    def add_row(self, row):
        np_row = np.array(row)
        if self._board_nums.size != 0:
            self._board_nums = np.vstack([self._board_nums, np_row])
        else:
            self._board_nums = np_row

    def search_board(self, number):
        result = np.where(self._board_nums == number)
        coordinates = self.get_coordinates(result)
        for coordinate in coordinates:
            self._mark_board(coordinate)

    def bingo(self):
        # Check the rows of the board
        for row in self._board_marked:
            if False not in row:
                return True

        # Check the columns of the board
        columns = self._board_marked.transpose()
        for column in columns:
            if False not in column:
                return True

        return False

    def calculated_score(self, winning_number):
        result = np.where(self._board_marked == False)
        coordinates = self.get_coordinates(result)
        sum_unmarked = 0
        for coordinate in coordinates:
            value = self._board_nums[coordinate[0], coordinate[1]]
            try:
                sum_unmarked += value
            except TypeError:
                print(f"Invalid value found on board: '{value}'")

        return sum_unmarked * int(winning_number)

    @staticmethod
    def get_coordinates(result):
        return list(zip(result[0], result[1]))

    def _mark_board(self, coordinate):
        self._board_marked[coordinate[0], coordinate[1]] = True

    def __str__(self) -> str:
        output = ""
        for row in self._board_nums:
            for elem in row:
                output = output + f"{elem:>3}"
            output = output + "\n"
        return output


def search_boards(numbers, boards):
    # Search the boards
    for number in numbers:
        for index, board in enumerate(boards):
            board.search_board(number)
            bingo = board.bingo()
            if bingo:
                if len(boards) == 1:
                    print(
                        f"\nBingo on last board with winning number '{number}'!!!\n")
                    print(board)
                    print(
                        f"Calculated score: {board.calculated_score(number)}")
                    sys.exit()
                del boards[index]
                search_boards(numbers, boards)


def main():

    filename = input("What is the input file name? ")

    try:
        input_numbers = []
        boards = []
        board = None

        with open(filename, "r") as file:
            create_new_board = False

            # Read the drawn numbers and setup boards
            for lineno, line in enumerate(file):
                line = line.strip()
                if lineno == 0:
                    input_numbers = [int(x) for x in line.split(',')]
                    continue

                # Skip blank lines
                if not line:
                    create_new_board = True
                    continue

                if create_new_board:
                    # Create a new board
                    board = Board()
                    boards.append(board)
                    create_new_board = False

                input_row = [int(x) for x in line.split()]
                board.add_row(input_row)

        search_boards(input_numbers, boards)

        print("No last winning bingo board found.")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
