#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <optional>
#include <string>
#include <sstream>
#include <iostream>
#include <vector>

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int nr_of_safe_reports{0};
    std::string line;

    while (std::getline(input_file, line))
    {
        std::stringstream line_stream{line};
        std::string word;
        int level;
        std::optional<int> previous{};
        bool report_is_safe{true};
        std::optional<bool> levels_increasing{};

        while(line_stream >> word)
        {
            if (std::stringstream(word) >> level)
            {
                if (previous_level.has_value())
                {
                    const auto diff = level - *previous;
                    const bool increasing = diff > 0;
                    if (!levels_increasing.has_value())
                    {
                        levels_increasing = increasing;
                    }

                    const bool series_direction_has_changed{increasing != *levels_increasing};
                    const bool difference_is_too_big{(std::abs(diff) < 1) || (std::abs(diff) > 3)};
                    if (series_direction_has_changed || difference_is_too_big) 
                    {
                        report_is_safe = false;
                        break;
                    }
                }

                previous = level;
            }
        }

        if (report_is_safe)
        {
            nr_of_safe_reports++;
        }
    }

    input_file.close();
    std::cout << "Nr. of safe reports: " << nr_of_safe_reports << "\n";

    return 0;
}
