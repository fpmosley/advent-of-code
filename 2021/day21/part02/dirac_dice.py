#!/usr/bin/env python

'''
Advent of Code 2021 - Day 21: Dirac Dice (Part 2)
https://adventofcode.com/2021/day/21
'''


import re
import time
from dataclasses import dataclass
from functools import cache
from itertools import product


WINNING_SCORE = 21

# Setup a tuple of the sum of all the possible roll combinations. 27 total (3x3x3).
QUANTUM_ROLLS = tuple(map(sum, product(range(1, 4), range(1, 4), range(1, 4))))


@dataclass
class Wins:
    player_one: int
    player_two: int


class Player():
    def __init__(self, player_id, position) -> None:
        self.id = player_id
        self.position = position
        self.score = 0

    def move(self, spaces: int) -> int:
        # Calculate number of spaces between 1 and 10 to move foward
        forward = (spaces - 1) % 10 + 1

        # Set the new position between 1 and 10
        self.position = (self.position + forward - 1) % 10 + 1

        # Update the score based on position
        self.score += self.position


def check_for_winner(player: Player) -> bool:
    if player.score >= WINNING_SCORE:
        return True

    return False


@cache
def play(position_one: int, score_one: int, position_two: int, score_two: int, turn: int) -> Wins:
    if turn == 1:
        if score_one >= WINNING_SCORE:
            return Wins(player_one=1, player_two=0)

        if score_two >= WINNING_SCORE:
            return Wins(player_one=0, player_two=1)
    else:
        if score_two >= WINNING_SCORE:
            return Wins(player_one=0, player_two=1)

        if score_one >= WINNING_SCORE:
            return Wins(player_one=1, player_two=0)

    wins_one = wins_two = 0

    for roll in QUANTUM_ROLLS:
        if turn == 1:
            # Set the new position between 1 and 10
            new_position_one = (position_one + roll - 1) % 10 + 1

            # Update the score based on position
            new_score_one = score_one + new_position_one

            # Next player's turn
            wins = play(new_position_one, new_score_one,
                        position_two, score_two, turn=2)
        else:
            # Set the new position between 1 and 10
            new_position_two = (position_two + roll - 1) % 10 + 1

            # Update the score based on position
            new_score_two = score_two + new_position_two

            # Next player's turn
            wins = play(position_one, score_one,
                        new_position_two, new_score_two, turn=1)

        wins_one += wins.player_one
        wins_two += wins.player_two

    return Wins(wins_one, wins_two)


def main():

    filename = input("What is the input file name? ")

    try:
        with open(filename, "r") as file:

            players = []
            pattern = r'Player (?P<id>\d+) starting position: (?P<position>\d+)'
            for line in file:
                line = line.strip()
                matches = re.match(pattern, line)
                if matches:
                    player_id = int(matches.group('id'))
                    position = int(matches.group('position'))
                    player = Player(player_id=player_id, position=position)
                    players.append(player)

        # Play the game; Player 1 has the first turn.
        start = time.time()
        wins = play(players[0].position, players[0].score,
                    players[1].position, players[1].score, turn=1)
        if wins.player_one > wins.player_two:
            print(f"\nPlayer 1 wins more in '{wins.player_one}' universes")
        else:
            print(f"\nPlayer 2 wins more in '{wins.player_two}' universes")
        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
