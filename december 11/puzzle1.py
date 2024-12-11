#!/usr/bin/python

BLINK_COUNT = 25


if __name__ == "__main__":

    input_file = open("input.txt")
    assert not input_file.closed, " * Error on opening the input file."
    stones = input_file.readline().rstrip().split(" ")
    input_file.close()

    for _ in range(BLINK_COUNT):

        skip_next_stone = False
        for i, stone in enumerate(stones):
            if skip_next_stone:
                skip_next_stone = False
                continue

            if stone == "0":
                stones[i] = "1"

            elif len(stone) % 2 == 0:
                divider = int(len(stone) / 2)
                left = stone[:divider]
                right = str(int(stone[divider:]))
                stones[i] = left
                stones.insert(i + 1, right)
                skip_next_stone = True

            else:
                stones[i] = str(2024 * int(stone))

    print(f"The number of stones after blinking {BLINK_COUNT} times: {len(stones)}")
