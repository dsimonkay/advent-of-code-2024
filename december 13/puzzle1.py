#!/usr/bin/python

from sys import argv
import re


TOKEN_A_COST = 3
TOKEN_B_COST = 1


if __name__ == "__main__":

    token_count = 0

    input_file_name = argv[1] if len(argv) > 1 else "input.txt"
    with open(input_file_name) as file:
        lines = file.readlines()
        while lines:
            line_a = lines.pop(0).rstrip()
            line_b = lines.pop(0).rstrip()
            line_prize = lines.pop(0).rstrip()
            if lines:
                lines.pop(0)

            [a_x, a_y] = list(map(int, re.findall("\d+", line_a)))
            [b_x, b_y] = list(map(int, re.findall("\d+", line_b)))
            [prize_x, prize_y] = list(map(int, re.findall("\d+", line_prize)))

            numerator_b = prize_y * a_x - prize_x * a_y
            denominator_b = a_x * b_y - b_x * a_y

            if numerator_b % denominator_b != 0:
                continue

            b = int(numerator_b / denominator_b)
            numerator_a = prize_x - b * b_x
            denominator_a = a_x
            if numerator_a % denominator_a != 0:
                continue

            a = int(numerator_a / denominator_a)
            token_count += a * TOKEN_A_COST + b * TOKEN_B_COST

    print(f"Nr. of tokens used: {token_count}")
