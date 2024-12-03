#include <cassert>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>
#include <utility>

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    std::regex command_regex(R"((do|don't)\(\)|mul\((\d+),(\d+)\))");

    int total_sum = 0;
    bool mul_enabled = true;
    std::string line;
    while (std::getline(input_file, line))
    {
        int sum = 0;
        std::sregex_iterator it_begin(line.begin(), line.end(), command_regex);
        std::sregex_iterator end;

        for (std::sregex_iterator it{it_begin}; it != end; ++it)
        {
            std::smatch match = *it;
            if (match[1].matched)
            {
                mul_enabled = (match[1] != "don't");
            }
            else if (mul_enabled)
            {
                sum += std::stoi(match[2]) * std::stoi(match[3]);
            }
        }

        total_sum += sum;
    }

    input_file.close();
    std::cout << "Total sum of enabled multiplications: " << total_sum << std::endl;

    return 0;
}
