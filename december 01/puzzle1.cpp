#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    std::vector<int> left_ids{};
    std::vector<int> right_ids{};
    int left_id;
    int right_id;

    while (input_file >> left_id >> right_id)
    {
        left_ids.push_back(left_id);
        right_ids.push_back(right_id);
    }

    std::sort(left_ids.begin(), left_ids.end());
    std::sort(right_ids.begin(), right_ids.end());

    int total_distance{0};
    for (auto i{0U}; i < left_ids.size(); ++i)
    {
        total_distance += std::abs(left_ids[i] - right_ids[i]);
    }

    input_file.close();
    std::cout << "Total_distance: " << total_distance << "\n";

    return 0;
}