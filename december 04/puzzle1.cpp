#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

void CheckWord(const std::string& word, int& nr_of_occurences)
{
    static const std::string xmas{"XMAS"};
    static const std::string samx{"SAMX"};

    if ((word == xmas) || (word == samx))
    {
        nr_of_occurences++;
    }
}

int GetNumberOfOccurencesAtPosition(const std::vector<std::string>& input, const std::size_t row, const std::size_t col)
{
    std::string word;

    const auto rows{input.size()};
    const auto cols{input[0].length()};
    int nr_of_occurences{0};

    // Horizontal: forward
    if (col <= (cols - 4U))
    {
        word = input[row].substr(col, 4U);
        CheckWord(word, nr_of_occurences);
    }

    // Vertical: downwards
    if (row <= (rows - 4U))
    {
        word = input[row].substr(col, 1U) + input[row + 1U].substr(col, 1U) + input[row + 2U].substr(col, 1U) + input[row + 3U].substr(col, 1U);
        CheckWord(word, nr_of_occurences);
    }

    // Diagonal: bottom-left
    if ((row <= (rows - 4U)) && (col >= 3U))
    {
        word = input[row].substr(col, 1U) + input[row + 1U].substr(col - 1U, 1U) + input[row + 2U].substr(col - 2U, 1U) + input[row + 3U].substr(col - 3U, 1U);
        CheckWord(word, nr_of_occurences);
    }

    // Diagonal: bottom-right
    if ((row <= (rows - 4U)) && (col <= (cols - 3U)))
    {
        word = input[row].substr(col, 1U) + input[row + 1U].substr(col + 1U, 1U) + input[row + 2U].substr(col + 2U, 1U) + input[row + 3U].substr(col + 3U, 1U);
        CheckWord(word, nr_of_occurences);
    }

    return nr_of_occurences;
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

    for (auto i{0U}; i < rows; ++i)
    {
        for (auto j{0U}; j < cols; ++j)
        {
            nr_of_occurences += GetNumberOfOccurencesAtPosition(input, i, j);
        }
    }

    std::cout << "Number of occurences: " << nr_of_occurences << "\n";

    return 0;
}
