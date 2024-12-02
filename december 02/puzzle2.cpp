#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <optional>
#include <string>
#include <sstream>
#include <iostream>
#include <vector>

/// @brief Checks a report (constisting of sequential level values) for safety.
/// @see the puzzle description for the mentioned concepts.
bool IsSafe(const std::vector<int>& levels)
{
		bool report_is_safe{true};
    std::optional<int> previous_level{};
    std::optional<bool> levels_increasing{};

    for (const auto level : levels)
    {
		    if (previous_level.has_value())
		    {
		        const auto diff = level - *previous_level;
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

		    previous_level = level;
    }

    return report_is_safe;
}

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
        std::vector<int> levels{};
        int level;

        // This works because we know that the input lines consist of space separated integers
        while(line_stream >> level)
        {
        	  levels.push_back(level);
        }

        if (IsSafe(levels))
        {
            nr_of_safe_reports++;
        }
        else
        {
        	  for (auto i{0U}; i < levels.size(); ++i)
        	  {
        	  	  auto modified_levels{levels};
        	  	  modified_levels.erase(modified_levels.begin() + i, modified_levels.begin() + i + 1U);
        	  	  if (IsSafe(modified_levels))
        	  	  {
        	  	  	  nr_of_safe_reports++;
        	  	  	  break;
        	  	  }
        	  }
        }
    }

    input_file.close();
    std::cout << "Nr. of safe reports: " << nr_of_safe_reports << "\n";

    return 0;
}
