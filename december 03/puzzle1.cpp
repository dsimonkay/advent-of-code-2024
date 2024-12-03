#include <cassert>
#include <fstream>
#include <iostream>
#include <regex>
#include <string>

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int result{0};
    std::string line;

    while (std::getline(input_file, line))
    {
        std::regex multiplication_regex("(mul\\(\\d+,\\d+\\))");
        auto mul_begin = std::sregex_iterator(line.begin(), line.end(), multiplication_regex);
        auto mul_end = std::sregex_iterator();
     
        for (std::sregex_iterator i{mul_begin}; i != mul_end; ++i)
        {
            std::smatch match = *i;
            std::string match_str = match.str();

            std::regex digit_regex("mul\\((\\d+),(\\d+)\\)");
            std::smatch matches;

            assert(std::regex_search(match_str, matches, digit_regex));
            const int operand_1{std::stoi(matches[1].str())};
            const int operand_2{std::stoi(matches[2].str())};

            result += operand_1 * operand_2;
        }
    }

    input_file.close();
    std::cout << "Result of multiplications: " << result << "\n";

    return 0;
}
