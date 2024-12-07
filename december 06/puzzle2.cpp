#include <cassert>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <tuple>
#include <vector>
#include <utility>

using DeltaMove = std::pair<int, int>;   // Expresses the delta in both row and column coordinates
const std::vector<DeltaMove> moves{
   {-1, 0},   // ^ -- direction: 0
   {0, 1},    // > -- direction: 1
   {1, 0},    // V -- direction: 2
   {0, -1}    // < -- direction: 3
};

bool IsWithinMap(const int row, const int col, const int max_row, const int max_col)
{
    return (0 <= row) && (row <= max_row) && (0 <= col) && (col <= max_col);
}

bool ContainsLoop(const std::vector<std::vector<char>>& map,
                  const int obstruction_row,
                  const int obstruction_col,
                  const int starting_row,
                  const int starting_col,
                  const int starting_direction,
                  const int max_row,
                  const int max_col)
{
    // The tuple encodes the <row, col, direction> of a step of the guard's path 
    std::set<std::tuple<int, int, int>> path{};
    int row{starting_row};
    int col{starting_col};
    int direction{starting_direction};
    bool loop_found{false};

    while (true)
    {
        if (path.contains({row, col, direction}))
        {
            loop_found = true;
            break;
        }

        const auto result = path.insert({row, col, direction});
        assert(result.second);   // Make sure the insertion was successful

        // Lookahead: one step in the given direction
        const int new_row = row + moves[direction].first;
        const int new_col = col + moves[direction].second;

        if (!IsWithinMap(new_row, new_col, max_row, max_col))
        {
            // Leaving the map; that was it
            break;
        }

        if ((map[new_row][new_col] == '#') || ((new_row == obstruction_row) && (new_col == obstruction_col)))
        {
            direction = (direction + 1) % 4;   // Turn right
        }
        else
        {
            row = new_row;
            col = new_col;
        }
    }

    return loop_found;
}

int GetNumberOfPossibleObstructions(const std::vector<std::vector<char>>& map,
                                    const int starting_row,
                                    const int starting_col,
                                    const int starting_direction = 0)
{
    // Preconditions
    assert(!map.empty());
    assert(!map[0].empty());

    const int max_row{static_cast<int>(map.size() - 1U)};
    const int max_col{static_cast<int>(map[0].size() - 1U)};
    assert(starting_row <= max_row);
    assert(starting_col <= max_col);

    int nr_of_possible_obstructions = 0;

    // Put an extra obstruction at each available position in the map and check whether it contains then a loop.
    // TODO: get the original path and only put obstacles along it.
    for (int i{0}; i <= max_row; ++i)
    {
        std::cout << "Checking loops in row " << i << "...\n";
        for (int j{0}; j <= max_col; ++j)
        {
            if (((i == starting_row) && (j == starting_col)) || map[i][j] == '#')
            {
                // Don't put an obstacle on the starting position or over existing obstructions
                continue;
            }

            if (ContainsLoop(map, i, j, starting_row, starting_col, starting_direction, max_row, max_col))
            {
                nr_of_possible_obstructions++;
            }
        }
    }

    return nr_of_possible_obstructions;
}


int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int nr_of_distinct_positions_path{0};
    std::string line;
    std::vector<std::vector<char>> map{};
    int starting_row{-1};
    int starting_col{-1};

    // Preassumptions:
    //  - the starting direction points upwards and is denoted by '^' in the input
    //  - the directions map to the following indices:
    //     ^: 0
    //     >: 1
    //     V: 2
    //     <: 3
    //    Note that in this order the direction turns 90 degrees as the index increases (modulo 4).
    const int starting_direction{0};

    int row_counter{0};
    while (std::getline(input_file, line))
    {
        map.push_back(std::vector<char>{line.begin(), line.end()});
        const auto guard_pos = line.find('^');
        if (guard_pos != std::string::npos)
        {
            starting_row = row_counter;
            starting_col = guard_pos;
        }

        row_counter++;
    }

    input_file.close();

    assert((starting_row >= 0) && (starting_col >= 0));
    const int nr_of_possible_obstructions = GetNumberOfPossibleObstructions(map, starting_row, starting_col, starting_direction);
    std::cout << "Number of possible obstructions: " << nr_of_possible_obstructions << std::endl;

    return 0;
}
