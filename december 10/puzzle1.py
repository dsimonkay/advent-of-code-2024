#!/usr/bin/python

from typing import List, Set, Tuple


PEAK = 9


def get_trailheads(trail_map: List[List[str]]) -> Set[Tuple[int]]:
    trailheads = set()

    for row in range(len(trail_map)):
        for col in range(len(trail_map[row])):
            if trail_map[row][col] == 0:
                trailheads.add((row, col, 0))

    return trailheads


def check_if_fitting(trail_map: List[List[int]],
                     row: int,
                     col:int,
                     prev_value: int,
                     to_visit: Set[Tuple[int]],
                     visited: Set[Tuple[int]]) -> int:

    next_value = trail_map[row][col]
    if (row, col) not in visited and next_value == prev_value + 1:

        if next_value == PEAK:
            visited.add((row, col))
            return 1

        else:
            to_visit.add((row, col, next_value))

    return 0


if __name__ == "__main__":

    trail_map = []

    with open("input.txt") as file:
        trail_map = [[int(ch) for ch in line.rstrip()] for line in file]

    trailheads = get_trailheads(trail_map)
    trailhead_score_sum = 0

    for trailhead in trailheads:
        to_visit = {trailhead}
        visited = set()

        while to_visit:
            row, col, value = to_visit.pop()
            visited.add((row, col))

            if row > 0:                 # looking up
                trailhead_score_sum += check_if_fitting(trail_map, row - 1, col, value, to_visit, visited)

            if row < len(trail_map) - 1:      # looking down
                trailhead_score_sum += check_if_fitting(trail_map, row + 1, col, value, to_visit, visited)

            if col > 0:                 # looking left
                trailhead_score_sum += check_if_fitting(trail_map, row, col - 1, value, to_visit, visited)

            if col < len(trail_map[0]) - 1:   # looking right
                trailhead_score_sum += check_if_fitting(trail_map, row, col + 1, value, to_visit, visited)

    print(f"The sum of all the trailhead scores: {trailhead_score_sum}")
