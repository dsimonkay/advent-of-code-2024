#!/usr/bin/python

from typing import List, Set, Tuple
from sys import argv, exit
import re

NR_OF_COLS = 101
NR_OF_ROWS = 103


def get_number_of_connected_robots(start_robot_position: Tuple[int, int],
                                   robot_positions: List[List],
                                   visited_robot_positions: Set[Tuple[int,int]]) -> List[Tuple[int,int]]:
    nr_of_connected_robots = 0
    (col, row) = start_robot_position
    candidates = [(col, row - 1), (col, row + 1), (col - 1, row), (col + 1, row)]

    for candidate in candidates:
        # #$$S#$%GDGD#$A$#%*%*%!!!! `candidate` is a tuple, `robot_positions` contains __lists__ (...)
        candidate_is_a_robot_on_the_map = list(candidate) in robot_positions
        we_dont_know_this_candidate_yet = candidate not in visited_robot_positions

        if candidate_is_a_robot_on_the_map and we_dont_know_this_candidate_yet:
            visited_robot_positions.add(candidate)
            nr_of_connected_robots += 1 + get_number_of_connected_robots(candidate, robot_positions, visited_robot_positions)

    return nr_of_connected_robots


def dump_robot_map_to_file(robot_positions, robot_velocities, elapsed_seconds):
    robot_map = [['.' for col in range(NR_OF_COLS)] for row in range(NR_OF_ROWS)]

    for i, (col, row) in enumerate(robot_positions):
        robot_map[row][col] = "#"

    with open(f"robot_map_at_second_{elapsed_seconds}.txt", "w") as map_file:
        for i in range(NR_OF_ROWS):
            map_row = "".join(robot_map[i])
            map_file.write(f"{map_row}\n")


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
    filename_containing_elapsed_seconds = re.findall("^robots_at_second_(\d+)\.txt$", input_file_name)
    elapsed_seconds = int(filename_containing_elapsed_seconds[0]) if filename_containing_elapsed_seconds else 0

    # The image of the Christmas tree is built from a large set of connected (neighboring) robots.
    # Shooting in the wild.
    while True:
        christmas_tree_found = False
        elapsed_seconds += 1

        for i in range(NR_OF_ROBOTS):
            robot_positions[i][0] = (robot_positions[i][0] + robot_velocities[i][0]) % NR_OF_COLS
            robot_positions[i][1] = (robot_positions[i][1] + robot_velocities[i][1]) % NR_OF_ROWS

        for robot_position in robot_positions:
            nr_of_connected_robots = 1 + get_number_of_connected_robots(robot_position, robot_positions, set(robot_position))
            if (nr_of_connected_robots > 20):
                christmas_tree_found = True
                dump_robot_map_to_file(robot_positions, robot_velocities, elapsed_seconds)
                break

        if christmas_tree_found:
            break

    print(f"Nr. of steps (seconds...) after which the robots seem to be arranged in some formation: {elapsed_seconds}")
