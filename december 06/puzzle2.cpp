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

int GetNumberOfPossibleObstructions(const std::vector<std::vector<char>>& map,
                                    const int starting_row,
                                    const int starting_col,
                                    const int starting_direction_idx = 0)
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

    int nr_of_possible_obstructions = 0;

    // The tuple encodes the <row, column, direction> of the guard at a given step
    std::set<std::tuple<int, int, int>> path{};

    while (true)
    {
        const auto result = path.insert({row, col, direction});
        assert(result.second); // Make sure the insertion was successful

        // Lookahead: one step in the given direction
        const int new_row = row + moves[direction].first;
        const int new_col = col + moves[direction].second;

        if (!IsWithinMap(new_row, new_col, max_row, max_col))
        {
            // Leaving the map; that was it
            break;
        }

        if (map[new_row][new_col] == '#')
        {
            direction = (direction + 1) % 4;   // Turn right
            continue;
        }

        // What would happen if there was an obstruction at (new_row, new_col) and we turned to the right
        // at this very position (because of the new obstruction)? Would we end up hitting a known path?
        int probe_direction{(direction + 1) % 4};
        int probe_row{row};
        int probe_col{col};
        std::set<std::tuple<int, int, int>> probe_path{};
        while (true)
        {
            if (path.contains({probe_row, probe_col, probe_direction}) ||
                probe_path.contains({probe_row, probe_col, probe_direction}))
            {
                // We have just discovered a loop!
                std::cout << "Possible obstruction position: (" << new_row << ", " << new_col << ")\n";
                nr_of_possible_obstructions++;
                break;
            }

            const auto probe_result = probe_path.insert({probe_row, probe_col, probe_direction});
            assert(probe_result.second);

            // Advance (hypothetically)
            probe_row += moves[probe_direction].first;
            probe_col += moves[probe_direction].second;

            if (!IsWithinMap(probe_row, probe_col, max_row, max_col))
            {
                // Leaving the map; that was it
                break;
            }

            if (map[probe_row][probe_col] == '#')
            {
                // Backtrack...
                probe_row -= moves[probe_direction].first;
                probe_col -= moves[probe_direction].second;
                // ...and turn
                probe_direction = (probe_direction + 1) % 4;
            }
        }

        row = new_row;
        col = new_col;
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
    const int nr_of_possible_obstructions = GetNumberOfPossibleObstructions(map, starting_row, starting_col, starting_direction_idx);
    std::cout << "Number of possible obstructions: " << nr_of_possible_obstructions << std::endl;

    return 0;
}
