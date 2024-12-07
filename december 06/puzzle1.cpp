#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <unordered_map>

using Move = std::pair<int, int>;
const std::vector<Move> moves{
   {-1, 0},   // ^
   {0, 1},    // >
   {1, 0},    // V
   {0, -1}    // <
};

int Walk(std::vector<std::vector<char>>& map, const int starting_row, const int starting_col, const int starting_direction_idx)
{
    // Preconditions
    assert(!map.empty());
    assert(!map[0].empty());

    const int max_row{static_cast<int>(map.size() - 1U)};
    const int max_col{static_cast<int>(map[0].size() - 1U)};
    assert(starting_row <= max_row);
    assert(starting_col <= max_col);

    int row{starting_row};
    int col{starting_col};
    int direction{starting_direction_idx};

    // Mark the initial position as visited
    map[row][col] = 'X';
    int nr_of_distinct_positions_visited = 1;

    while (true)
    {
        // Probe: one step in the given direction
        const int new_row = row + moves[direction].first;
        const int new_col = col + moves[direction].second;

        if ((new_row < 0) || (new_row > max_row) || (new_col < 0) || (new_col > max_col))
        {
            // Leaving the map; that was it
            break;
        }

        if (map[new_row][new_col] == '#')
        {
            // Turn 90 degrees
            direction = (direction + 1) % 4;
            continue;
        }

        if (map[new_row][new_col] == '.')
        {
            nr_of_distinct_positions_visited++;
            map[new_row][new_col] = 'X';
        }

        row = new_row;
        col = new_col;
    }

    return nr_of_distinct_positions_visited;
}

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int nr_of_distinct_positions_visited{0};
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
    const char starting_direction{'^'};
    const int starting_direction_idx{0};

    int row_counter{0};
    while (std::getline(input_file, line))
    {
        map.push_back(std::vector<char>{line.begin(), line.end()});
        const auto guard_pos = line.find(starting_direction);
        if (guard_pos != std::string::npos)
        {
            starting_row = row_counter;
            starting_col = guard_pos;
        }

        row_counter++;
    }

    input_file.close();
    nr_of_distinct_positions_visited = Walk(map, starting_row, starting_col, starting_direction_idx);
    std::cout << "Number of distinct positions visited: " << nr_of_distinct_positions_visited << std::endl;

    return 0;
}
