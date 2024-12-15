#!/usr/bin/python

from typing import List, Tuple
from sys import argv


WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY_SPACE = "."
COMMAND_TO_MOVEMENT_MAP = {"<": (0, -1),
                           "^": (-1, 0),
                           ">": (0, +1),
                           "v": (+1, 0)}
# To be updated later
MAX_ROWS = 0
MAX_COLS = 0


def print_(warehouse_map: List[List[str]]):
    for row in warehouse_map:
        print("".join(row))


def read_input(input_file_name: str) -> Tuple[List, List, str]:
    warehouse_map = []
    robot_pos = (0,0)
    commands = ""

    with open(input_file_name) as file:
        horizontal_wall = file.readline().rstrip()
        warehouse_map.append(list(horizontal_wall))

        row = 0
        while (line := file.readline().rstrip()) != horizontal_wall:
            row += 1
            warehouse_map.append(list(line))
            if (robot_col := line.find(ROBOT)) > 0:
                robot_pos = [row, robot_col]

        warehouse_map.append(list(horizontal_wall))

        for line in file:
            commands += line.rstrip()

    return warehouse_map, robot_pos, commands, len(warehouse_map[0]), len(warehouse_map)


def move(pos: List, command: str) -> List:
    (row, col) = pos
    new_pos = (row, col)    # conservative approach

    assert command in COMMAND_TO_MOVEMENT_MAP, "Hey, buddy, watcha doin'?"
    new_row = row + COMMAND_TO_MOVEMENT_MAP[command][0]
    new_col = col + COMMAND_TO_MOVEMENT_MAP[command][1]

    if new_row >= 0 and new_row <= MAX_ROWS and new_col >= 0 and new_col <= MAX_COLS:
        new_pos = (new_row, new_col)

    return new_pos


def execute_commands(warehouse_map: List, robot_pos: List, commands: str):
    for command in commands:
        move_is_feasible = True
        pos = move(robot_pos, command)
        to_swap = [(pos, robot_pos)]
        while warehouse_map[pos[0]][pos[1]] != EMPTY_SPACE:

            if warehouse_map[pos[0]][pos[1]] == WALL:
                move_is_feasible = False
                break

            new_pos = move(pos, command)
            to_swap.append((new_pos, pos))
            pos = new_pos

        if move_is_feasible:
            # swap everything from the final position back from to the robot pos
            for pos_1, pos_2 in reversed(to_swap):
                tmp = warehouse_map[pos_1[0]][pos_1[1]]
                warehouse_map[pos_1[0]][pos_1[1]] = warehouse_map[pos_2[0]][pos_2[1]]
                warehouse_map[pos_2[0]][pos_2[1]] = tmp

            robot_pos = move(robot_pos, command)    # lame, but ok


def compute_sum_of_all_boxes_gps_coordinates(warehouse_map: List[List[str]]) -> int:
    gps_coordinates_sum = 0
    for i, row in enumerate(warehouse_map):
        for j, col in enumerate(row):
            if warehouse_map[i][j] == BOX:
                gps_coordinates_sum += 100 * i + j

    return gps_coordinates_sum


if __name__ == "__main__":

    input_file_name = argv[1] if len(argv) > 1 else "input.txt"
    warehouse_map, robot_pos, commands, MAX_COLS, MAX_ROWS = read_input(input_file_name)
    execute_commands(warehouse_map, robot_pos, commands)
    sum_of_all_boxes_gps_coordinates = compute_sum_of_all_boxes_gps_coordinates(warehouse_map)

    print(f"Sum of all boxes' GPS coordinates: {sum_of_all_boxes_gps_coordinates}")
