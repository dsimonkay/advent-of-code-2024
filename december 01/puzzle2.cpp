#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>

int main()
{
    std::ifstream input_file{"input.txt"};
    assert(input_file.is_open());

    std::vector<int> left_ids{};
    std::unordered_map<int, int> right_id_frequencies{};
    int left_id;
    int right_id;

    // Assuming the file structure: each line constists of two integers, separated by a space
    while (input_file >> left_id >> right_id)
    {
        left_ids.push_back(left_id);
        right_id_frequencies[right_id] += 1;
    }

    long long int similarity_score{0}; 
    for (const auto id : left_ids)
    {
        similarity_score += (id * right_id_frequencies[id]);
    }

    input_file.close();
    std::cout << "similarity_score = " << similarity_score  << "\n";

    return 0;
}