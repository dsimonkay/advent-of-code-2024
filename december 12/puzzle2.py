#!/usr/bin/python

from typing import Dict, List, Tuple
from functools import cmp_to_key
from sys import argv


def create_garden_map_from_file(input_file_name: str) -> Dict[str, List]:
    garden_map = {}
    with open(input_file_name) as file:
        row = -1
        col = -1
        for line in file:
            row += 1
            col = -1
            for ch in line.strip():
                col += 1
                if ch not in garden_map:
                    garden_map[ch] = []

                garden_map[ch].append((row, col))

    return garden_map


def get_connected_squares(start_square: Tuple[int, int], squares: List[Tuple[int,int]]) -> List[Tuple[int, int]]:
    connected_squares = []
    (row, col) = start_square
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    for candidate in candidates:
        if candidate in squares:
            squares.remove(candidate)
            connected_squares += [candidate]
            connected_squares += get_connected_squares(candidate, squares)

    return connected_squares


def find_plots_in(garden_map: Dict[str, List]) -> List[List[Tuple[int,int]]]:
    plots = []
    for plant, squares in garden_map.items():

        while squares:
            start_square = squares.pop(0)
            plot = [start_square] + get_connected_squares(start_square, squares)
            plots.append(plot)

    return plots


def count_corners(squares: List[Tuple[int, int]], corner_specs: List) -> int:
    corners = 0

    for square in squares:
        square_qualifies_as_corner = True
        for (d_row, d_col), square_needs_to_exist in corner_specs:
            candidate = (square[0] + d_row, square[1] + d_col)
            complies_with_spec = (not square_needs_to_exist and candidate not in squares) or (square_needs_to_exist and candidate in squares)
            square_qualifies_as_corner = complies_with_spec
            if not square_qualifies_as_corner:
                break

        if square_qualifies_as_corner:
           corners += 1

    return corners


def calculate_budget_fence_price_of(plots: List[List[Tuple[int,int]]]) -> int:
    total_price = 0

    # corner specifications
    top_left_outer_corner     = [((-1, 0), False), ((0, -1), False), ((-1, -1), False)]
    top_right_outer_corner    = [((-1, 0), False), ((0, +1), False), ((-1, +1), False)]
    bottom_right_outer_corner = [((+1, 0), False), ((0, +1), False), ((+1, +1), False)]
    bottom_left_outer_corner  = [((+1, 0), False), ((0, -1), False), ((+1, -1), False)]

    top_left_inner_corner     = [((0, +1), True),  ((+1, 0), True),  ((+1, +1), False)]
    top_right_inner_corner    = [((0, -1), True),  ((+1, 0), True),  ((+1, -1), False)]
    bottom_right_inner_corner = [((-1, 0), True),  ((0, -1), True),  ((-1, -1), False)]
    bottom_left_inner_corner  = [((-1, 0), True),  ((0, +1), True),  ((-1, +1), False)]

    dumb_bottom_right_corner  = [((0, -1), False), ((+1, 0), False), ((+1, -1), True)]
    dumb_top_left_corner      = [((-1, 0), False), ((0, +1), False), ((-1, +1), True)]
    dumb_bottom_left_corner   = [((0, +1), False), ((+1, 0), False), ((+1, +1), True)]
    dumb_top_right_corner     = [((-1, 0), False), ((0, -1), False), ((-1, -1), True)]

    for plot in plots:
        distinct_plot_sides = 0

        if len(plot) < 3:
            distinct_plot_sides = 4

        else:
            # Counting the corners instead of sides.
            corner_count = 0

            # outer corners
            corner_count += count_corners(plot, top_left_outer_corner)
            corner_count += count_corners(plot, top_right_outer_corner)
            corner_count += count_corners(plot, bottom_right_outer_corner)
            corner_count += count_corners(plot, bottom_left_outer_corner)

            # inner corners
            corner_count += count_corners(plot, top_left_inner_corner)
            corner_count += count_corners(plot, top_right_inner_corner)
            corner_count += count_corners(plot, bottom_left_inner_corner)
            corner_count += count_corners(plot, bottom_right_inner_corner)

            # dumb inner corners
            corner_count += count_corners(plot, dumb_bottom_right_corner)
            corner_count += count_corners(plot, dumb_top_left_corner)
            corner_count += count_corners(plot, dumb_bottom_left_corner)
            corner_count += count_corners(plot, dumb_top_right_corner)

            distinct_plot_sides = corner_count

        total_price += distinct_plot_sides * len(plot)

    return total_price


if __name__ == "__main__":

    input_file_name = argv[1] if len(argv) > 1 else "input.txt"
    garden_map = create_garden_map_from_file(input_file_name)
    plots = find_plots_in(garden_map)
    total_price = calculate_budget_fence_price_of(plots)

    print(f"The total price of fencing all regions is {total_price}")
