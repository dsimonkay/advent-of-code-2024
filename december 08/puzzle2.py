#!/usr/bin/python

from typing import Set, Tuple
# import math


MAX_ROW = -1
MAX_COL = -1


def is_within_map(position: Tuple[int, int]) -> bool:
    return 0 <= position[0] and position[0] <= MAX_ROW and \
           0 <= position[1] and position[1] <= MAX_COL


def store_antinode_candidates(start_position: Tuple[int, int], row_diff: int, col_diff: int, antinodes: Set[Tuple[int, int]]):
    # We're gonna store the antennas themselves (=specified by the starting position) as antinodes, too.
    antinode_candidate = start_position
    while is_within_map(antinode_candidate):
        antinodes.add(antinode_candidate)
        antinode_candidate = (antinode_candidate[0] + row_diff, antinode_candidate[1] + col_diff)


if __name__ == "__main__":

    antinodes = set()
    nodes = dict()

    row = -1
    col = -1    # only so that `col` be in scope at this level
    with open("input.txt") as file:
        for line in file:
            row += 1
            col = -1
            for ch in line.strip():
                col += 1
                if ch == ".":
                    continue

                if ch not in nodes:
                    nodes[ch] = []

                nodes[ch].append((row, col))

    # Updating global constants (don't say a word)
    MAX_ROW = row
    MAX_COL = col

    for antennas in nodes.values():
        for i in range(0, len(antennas)):
            for j in range(i+1, len(antennas)):

                row_diff = antennas[j][0] - antennas[i][0]
                col_diff = antennas[j][1] - antennas[i][1]

                # ***************************************************************************************
                #    The funny (=sad) thing is that the following lines are actually not needed for
                #    the result to be accepted. Come on, we're talking about "being on the same line"!
                # ***************************************************************************************
                # "Normalize" the differences so that adding/subtracting them will yield integer coordinates
                # diff_gcd = math.gcd(row_diff, col_diff)
                # row_diff = int(row_diff / diff_gcd)
                # col_diff = int(col_diff / diff_gcd)

                # Probing the antinodes in both direction, starting from node_1. Going "backward" first...
                store_antinode_candidates(antennas[i], -row_diff, -col_diff, antinodes)

                # ...then "forward"
                store_antinode_candidates(antennas[i], row_diff, col_diff, antinodes)

    print(f"Number of unique antinode locations: {len(antinodes)}")
