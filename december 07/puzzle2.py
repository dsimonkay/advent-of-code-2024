#!/usr/bin/python

from typing import List


def mul(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def get_operator_permutations(length: int) -> List[List]:
    if length == 0:
        return [[]]

    sub_operators = get_operator_permutations(length - 1)
    result = []

    for sub_op in sub_operators:
        result.append(sub_op + [mul])
        result.append(sub_op + [add])
        result.append(sub_op + [concat])

    return result


def test_value_can_be_calculated_from(test_value: int, operands: List[int]) -> bool:
    assert operands, " * No operands given."

    operator_permutations = get_operator_permutations(len(operands) - 1)
    for operators in operator_permutations:
        value = operands[0]
        for i in range(1, len(operands)):
            value = operators[i-1](value, operands[i])
            if value == test_value:
                return True

            if value > test_value:
                break

    return False


if __name__ == "__main__":

    sum_of_satisfied_test_values = 0

    line_nr = 0
    with open("input.txt") as file:
        for line in file:
            line_nr += 1
            test_value, operands = line.split(": ")
            test_value = int(test_value)
            operands = [int(value) for value in operands.split(" ")]

            # Need some output to show progress :-/
            # print(f"[line {line_nr}] test_value: {test_value}   operands: {operands}")
            if test_value_can_be_calculated_from(test_value, operands):
                sum_of_satisfied_test_values += test_value

    print(f"Calibration result: {sum_of_satisfied_test_values}")
