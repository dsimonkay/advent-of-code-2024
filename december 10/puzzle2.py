#!/usr/bin/python

from typing import List, Set, Tuple


PEAK = 9


def get_trailheads_as_paths(trail_map: List[List[int]]) -> List[List[Tuple[int]]]:
    trailheads = []

    for row in range(len(trail_map)):
        for col in range(len(trail_map[row])):
            if trail_map[row][col] == 0:
                trailheads.append([(row, col)])

    return trailheads


def grow_path(path: List[int], trail_map: List[List[int]]) -> List[List[int]]:
    grown_paths = []

    # Path tail element
    row, col  = path[-1]
    value = trail_map[row][col]

    if row > 0 and trail_map[row - 1][col] == value + 1:
        grown_paths.append(path + [(row - 1, col)])

    if row < len(trail_map)-1 and trail_map[row + 1][col] == value + 1:
        grown_paths.append(path + [(row + 1, col)])

    if col > 0 and trail_map[row][col - 1] == value + 1:
        grown_paths.append(path + [(row, col - 1)])

    if col < len(trail_map[0])-1 and trail_map[row][col + 1] == value + 1:
        grown_paths.append(path + [(row , col + 1)])

    return grown_paths


if __name__ == "__main__":

    trail_map = []
    with open("input.txt") as file:
        trail_map = [[int(ch) for ch in line.rstrip()] for line in file]

    rating_sum = 0
    paths = get_trailheads_as_paths(trail_map)
    while paths:
        path = paths.pop(0)
        grown_paths = grow_path(path, trail_map)

        for grown_path in grown_paths:
            row, col = grown_path[-1]
            if trail_map[row][col] == PEAK:
                rating_sum += 1
            else:
                paths.append(grown_path)

    print(f"The sum of all the trailhead ratings: {rating_sum}")
