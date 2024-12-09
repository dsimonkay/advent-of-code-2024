#!/usr/bin/python

from typing import List

EMPTY_SPACE = -1

def create_map(input: str) -> List[int]:
    disk_map = []
    file_id = 0
    is_file = True
    for ch in input:
        symbol = EMPTY_SPACE
        nr_of_fields = int(ch)

        if is_file:
            symbol = file_id
            file_id += 1

        disk_map += nr_of_fields * [symbol]
        is_file = not is_file

    return disk_map


def find_free_space_pos(disk_map: List[int], start_pos: int) -> int:
    for i in range(start_pos, len(disk_map)-1):
        if disk_map[i] == EMPTY_SPACE:
            return i
    return -2


def find_occupied_space_pos_from_behind(disk_map: List[int], start_pos: int) -> int:
    for i in range(start_pos, -1, -1):
        if not disk_map[i] == EMPTY_SPACE:
            return i
    return -2


def reorganize(disk_map: List[int]):
    free_space_pos = find_free_space_pos(disk_map, 0)
    file_id_pos = find_occupied_space_pos_from_behind(disk_map, len(disk_map)-1)
    while free_space_pos < file_id_pos:
        # swap
        disk_map[free_space_pos] = disk_map[file_id_pos]
        disk_map[file_id_pos] = EMPTY_SPACE

        free_space_pos = find_free_space_pos(disk_map, free_space_pos)
        file_id_pos = find_occupied_space_pos_from_behind(disk_map, file_id_pos)


def calculate_checksum(disk_map: List[int]) -> int:
    checksum = 0
    for i in range(len(disk_map) - 1):
        if disk_map[i] == EMPTY_SPACE:
            break
        checksum += i * disk_map[i]
    return checksum


if __name__ == "__main__":

    input_file = open("input.txt")
    assert not input_file.closed, " * Error on opening the input file."
    input = input_file.readline().rstrip()
    input_file.close()

    disk_map = create_map(input)
    reorganize(disk_map)
    checksum = calculate_checksum(disk_map)

    print(f"The checksum of the reordered hard drive: {checksum}")
