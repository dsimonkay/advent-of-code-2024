#!/usr/bin/python

from typing import List, Tuple

EMPTY_SPACE = -1

def create_map(input: str) -> Tuple[List[int], Tuple[int], List[int]]:
    disk_map = []
    file_map = []
    free_space_map = []
    file_id = 0
    position = 0
    is_file = True

    for ch in input:
        symbol = EMPTY_SPACE
        nr_of_fields = int(ch)

        if is_file:
            symbol = file_id
            if nr_of_fields > 0:
                file_map.append((file_id, position, nr_of_fields))
            file_id += 1

        elif nr_of_fields > 0:
            free_space_map.append([position, nr_of_fields])

        disk_map += nr_of_fields * [symbol]
        position += nr_of_fields
        is_file = not is_file

    return disk_map, file_map, free_space_map


def reorganize2(disk_map: List[int], file_map: Tuple[int], free_space_map: List[int]):
    for i in range(len(file_map)-1, -1, -1):
        file_id, file_start_pos, file_length = file_map[i]

        for j in range(len(free_space_map)):
            free_space_pos, free_space_length = free_space_map[j]

            if free_space_pos > file_start_pos:
                break

            if free_space_length < file_length:
                continue

            # do the swap
            for k in range(free_space_pos, free_space_pos + file_length):
                disk_map[k] = file_id
            for k in range(file_start_pos, file_start_pos + file_length):
                disk_map[k] = EMPTY_SPACE

            # do the bookeeping of the free space...
            free_space_map[j][0] += file_length
            free_space_map[j][1] -= file_length
            free_space_map.append([file_start_pos, file_length])
            # ..and just forget about the file entry (it won't be touched again)

            # close your eyes
            if free_space_map[j][1] == 0:
                del free_space_map[j]

            break


def calculate_checksum(disk_map: List[int]) -> int:
    checksum = 0
    for i in range(len(disk_map) - 1):
        if disk_map[i] == EMPTY_SPACE:
            continue
        checksum += i * disk_map[i]

    return checksum


if __name__ == "__main__":

    input_file = open("input.txt")
    assert not input_file.closed, " * Error on opening the input file."
    input = input_file.readline().rstrip()
    input_file.close()

    disk_map, file_map, free_space_map = create_map(input)
    reorganize2(disk_map, file_map, free_space_map)
    checksum = calculate_checksum(disk_map)

    print(f"The checksum of the reordered hard drive: {checksum}")
