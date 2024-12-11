#!/usr/bin/python

from typing import List


BLINK_COUNT = 75
register = {}

def blink_at(stones: List[int], remaining_blink_count: int) -> int:

    if remaining_blink_count == 0:
        return len(stones)

    nr_of_stones = 0
    for stone in stones:
        key = (stone, remaining_blink_count)
        if key in register:
            nr_of_stones += register[key]
            continue

        nr_of_stones_after_blinking_at_this_one = 0
        if stone == 0:
            nr_of_stones_after_blinking_at_this_one = blink_at([1], remaining_blink_count - 1)

        else:
            stone_str = str(stone)
            stone_digit_length = len(stone_str)
            if stone_digit_length & 1:
                nr_of_stones_after_blinking_at_this_one = blink_at([stone * 2024], remaining_blink_count - 1)
         
            else:
                divider = int(stone_digit_length / 2)
                left_stone = int(stone_str[:divider])
                right_stone = int(stone_str[divider:])
                nr_of_stones_after_blinking_at_this_one = blink_at([left_stone, right_stone], remaining_blink_count - 1)

        register[key] = nr_of_stones_after_blinking_at_this_one
        nr_of_stones += nr_of_stones_after_blinking_at_this_one

    return nr_of_stones;


if __name__ == "__main__":

    input_file = open("input.txt")
    assert not input_file.closed, " * Error on opening the input file."
    stones = [int(ch) for ch in input_file.readline().rstrip().split(" ")]
    input_file.close()

    nr_of_stones = blink_at(stones, BLINK_COUNT)
    print(f"The number of stones after blinking {BLINK_COUNT} times: {nr_of_stones}")
