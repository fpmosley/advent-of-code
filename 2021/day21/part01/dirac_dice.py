#!/usr/bin/env python

'''
Advent of Code 2021 - Day 21: Dirac Dice (Part 1)
https://adventofcode.com/2021/day/21
'''


import re
import time
from collections import deque
from itertools import cycle


WINNING_SCORE = 1000


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


def check_for_winner(players: list) -> Player:
    for player in players:
        if player.score >= WINNING_SCORE:
            return player

    return None


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

        # Play the game
        start = time.time()
        rolls = 0
        roll = cycle(range(1, 101)).__next__
        turns = deque(players)
        while turns:
            # Get the player whose turn it is
            player = turns.popleft()
            spaces = 0

            # Roll the die. Number of spaces to move forward is the total of 3 dice rolls.
            for _ in range(3):
                spaces += roll()

            rolls += 3

            # Move the player
            player.move(spaces)

            # Check for winner (This implementation assumes there are two players only)
            winner = check_for_winner(players)
            if winner:
                print(
                    f"\nThe winning player is Player {winner.id} with a score of {winner.score}")
                loser = turns.popleft()
                print(
                    f"The loser's score ({loser.score}) multiplied by number of dice roles ({rolls}): {loser.score * rolls}\n")
                break

            # Game continues. Send the player to the back of the turns queue
            turns.append(player)

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
