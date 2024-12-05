#include <cassert>
#include <fstream>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <set>
#include <utility>
#include <vector>

int ProcessUpdates(const std::set<std::pair<int, int>>& rules, const std::vector<int>& updates)
{
    // Precondition
    assert((updates.size() % 2) == 1);

    for (auto i{0U}; i < (updates.size() - 1U); ++i)
    {
        for (auto j{i + 1U}; j < updates.size(); ++j)
        {
            const int preceding_page_number{updates[i]};
            const int succeding_page_number{updates[j]};
            if (rules.contains({succeding_page_number, preceding_page_number}))
            {
                // If we find a contradicting rule, then this series of updates can be ignored right away
                return 0;
            }
        }
    }

    // If we are here, the given series of updates comply to the rules.
    // Let's pick the middle element.
    return updates[(updates.size() - 1U) / 2];
}


int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    int middle_page_numbers_sum{0};
    std::string line;
    std::set<std::pair<int, int>> rules{};
    const std::regex rule_regex{R"((\d+)\|(\d+))"};

    bool reading_rules{true};
    while (std::getline(input_file, line))
    {
        if (line.empty())
        {
            reading_rules = false;
            continue;
        }

        if (reading_rules)
        {
            std::smatch rule_match;

            // Assuming valid input
            assert(std::regex_match(line, rule_match, rule_regex));
            int preceding_page_number{std::stoi(rule_match[1])};
            int succeding_page_number{std::stoi(rule_match[2])};

            rules.insert({preceding_page_number, succeding_page_number});
        }
        else // reading updates
        {
            std::vector<int> updates{};
            std::stringstream ss(line);
            std::string page_number;

            // Parse the string using getline with comma as delimiter
            while (std::getline(ss, page_number, ','))
            {
                updates.push_back(std::stoi(page_number));
            }

            // Process the updates
            middle_page_numbers_sum += ProcessUpdates(rules, updates);
        }
    }

    input_file.close();

    std::cout << "Middle page numbers sum: " << middle_page_numbers_sum << "\n";

    return 0;
}
