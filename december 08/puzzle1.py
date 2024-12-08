#!/usr/bin/python

from typing import Tuple


MAX_ROW = -1
MAX_COL = -1


def is_within_map(position: Tuple[int, int]) -> bool:
    return 0 <= position[0] and position[0] <= MAX_ROW and \
           0 <= position[1] and position[1] <= MAX_COL


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

    for ch, antennas in nodes.items():
        for i in range(0, len(antennas)):
            for j in range(i+1, len(antennas)):

                node1_row, node1_col = antennas[i]
                node2_row, node2_col = antennas[j]

                d_row = node2_row - node1_row
                d_col = node2_col - node1_col

                antinode_candidate_1 = (node1_row - d_row, node1_col - d_col)
                if is_within_map(antinode_candidate_1):
                    antinodes.add(antinode_candidate_1)

                antinode_candidate_2 = (node2_row + d_row, node2_col + d_col)
                if is_within_map(antinode_candidate_2):
                    antinodes.add(antinode_candidate_2)

    print(f"Number of unique antinode locations: {len(antinodes)}")
