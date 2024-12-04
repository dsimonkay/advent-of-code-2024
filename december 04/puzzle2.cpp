#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int GetNumberOfOccurencesAtPosition(const std::vector<std::string>& input, const std::size_t row, const std::size_t col)
{
    static const std::string ms{"MS"};
    static const std::string sm{"SM"};

    if (input[row].substr(col, 1U) == "A")
    {
        const auto word1 = input[row - 1U].substr(col - 1U, 1U) + input[row + 1U].substr(col + 1U, 1U);
        const auto word2 = input[row + 1U].substr(col - 1U, 1U) + input[row - 1U].substr(col + 1U, 1U);
        if (((word1 == ms) || (word1 == sm)) && ((word2 == ms) || (word2 == sm)))
        {
            return 1;
        }
    }

    return 0;
}


int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int nr_of_occurences{0};
    std::vector<std::string> input;
    std::string line;

    while (std::getline(input_file, line))
    {
        input.push_back(line);
    }

    input_file.close();

    // assuming non-empty input and that each line has the same length
    const auto rows = input.size();
    const auto cols = input[0].length();

    for (auto i{1U}; i < (rows - 1U); ++i)
    {
        for (auto j{1U}; j < (cols - 1U); ++j)
        {
            nr_of_occurences += GetNumberOfOccurencesAtPosition(input, i, j);
        }
    }

    std::cout << "Number of occurences: " << nr_of_occurences << "\n";

    return 0;
}
