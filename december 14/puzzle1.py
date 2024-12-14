#!/usr/bin/python

from typing import List
from sys import argv
import re

NR_OF_STEPS = 100
NR_OF_COLS = 101
NR_OF_ROWS = 103


def get_quadrants(robot_positions: List) -> int:
    nr_of_robots_in_quadrants = [0, 0, 0, 0]

    middle_col = (NR_OF_COLS - 1) / 2
    middle_row = (NR_OF_ROWS - 1) / 2

    for x, y in robot_positions:
        if x == middle_col or y == middle_row:
            continue

        col_half = 0 if x < middle_col else 1
        row_half = 0 if y < middle_row else 1
        quadrant = 2 * row_half + col_half

        nr_of_robots_in_quadrants[quadrant] += 1

    print(f"quadrants: {nr_of_robots_in_quadrants}")
    return nr_of_robots_in_quadrants


if __name__ == "__main__":

    input_file_name = argv[1] if len(argv) > 1 else "input.txt"
    robot_positions = []
    robot_velocities = []
    with open(input_file_name) as file:
        for line in file:
             parsed_line = re.findall("^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$", line.strip())
             [pos_x, pos_y, v_x, v_y] = list(map(int, parsed_line[0]))

             robot_positions.append([pos_x, pos_y])
             robot_velocities.append((v_x, v_y))

    NR_OF_ROBOTS = len(robot_positions)

    # move the robots for NR_OF_STEPS steps
    for _ in range(NR_OF_STEPS):
        for i in range(NR_OF_ROBOTS):
            robot_positions[i][0] = (robot_positions[i][0] + robot_velocities[i][0]) % NR_OF_COLS
            robot_positions[i][1] = (robot_positions[i][1] + robot_velocities[i][1]) % NR_OF_ROWS

    # calculate the quadrants
    quadrant1, quadrant2, quadrant3, quadrant4 = get_quadrants(robot_positions)
    safety_factor = quadrant1 * quadrant2 * quadrant3 * quadrant4

    print(f"Safety factor after {NR_OF_STEPS} steps: {safety_factor}")