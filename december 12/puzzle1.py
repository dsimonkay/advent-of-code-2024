#!/usr/bin/python

from typing import Dict, List, Tuple


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


def calculate_fence_price_of(plots: List[List[Tuple[int,int]]]) -> int:
    total_price = 0

    for plot in plots:
        plot_perimeter = 0
        for square in plot:
            (row, col) = square
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            square_perimeter = 4
            for neighbor in neighbors:
                if neighbor in plot:
                    square_perimeter -= 1

            plot_perimeter += square_perimeter

        total_price += plot_perimeter * len(plot)

    return total_price


if __name__ == "__main__":

    garden_map = create_garden_map_from_file("input.txt")
    plots = find_plots_in(garden_map)
    total_price = calculate_fence_price_of(plots)

    print(f"The total price of fencing all regions is {total_price}")
