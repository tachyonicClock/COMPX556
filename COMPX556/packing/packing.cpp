#include <iostream>
#include <vector>
#include <limits>
#include <fstream>
#include <sstream>
#include <chrono>
#include "packing.h"
#include "lns.h"
#include "neighbourhood.h"

std::string StringifySolution(const UnplacedItems &items){
    std::stringstream ss;
    for (const Item &item : items)
    {
        ss << (item.is_rotated? "R":"") << item.id << " ";
    }
    return ss.str();
}

/**
 * @brief The top of the highest item in the given vector.
 * 
 * @param items A vector of items to evaluate
 * @return int The height in units
 */
int PackingHeight(const PlacedItems &items){
    int height = 0;
    for (const Item &item : items)
        height = std::max(height, item.top());
    return height;
}

/**
 * @brief A percentage representing the amount of wasted space in the given
 * solution.
 * 
 * @param items Items to judge the fitness of
 * @return float 1 is good 0 is bad
 */
float Fitness(const PlacedItems &items){
    float total_area = 0;
    int placement_height = 0;
    for (const Item &rect : items)
    {
        total_area += rect.area();
        placement_height = std::max(placement_height, rect.top());
    }
    return total_area/(placement_height*kStripWidth);
}

PlacedItems BestNeighbour(const UnplacedItems &items){
    std::vector<NeighbourhoodIterator*> component_neighbourhoods{
            new RotateNeighbourhood(items),
            new SwapNeighbourhood(items),
    };
    CompositeNeighbourhood neighbourhood(component_neighbourhoods);
    UnplacedItems best_neighbour;
    float best_fitness = 0;

    while (neighbourhood.HasNext())
    {
        // Get the next neighbour
        UnplacedItems neighbour = neighbourhood.Next();
        // Calculate the fitness of the neighbour
        neighbour = BLPackItems(neighbour);
        float fitness = Fitness(neighbour);
        // If the fitness is better than the best fitness, update the best fitness and best neighbour
        if (fitness > best_fitness)
        {
            best_fitness = fitness;
            best_neighbour = neighbour;
        }
    }

    return best_neighbour;
}

/**
 * @brief A local search algorithm that iteratively improves the fitness of a
 * solution by swapping items.
 * 
 * @param items The items to pack
 * @return PlacedItems The best solution found
 */
PlacedItems LocalSearch(const UnplacedItems &items) {
    PlacedItems best_solution = items;
    float best_fitness = 0;
    clock_t start = clock();
    for (int i = 0; i < 100; i++)
    {
        UnplacedItems neighbour = BestNeighbour(best_solution);
        float fitness = Fitness(neighbour);
        if (fitness > best_fitness)
        {
            best_fitness = fitness;
            best_solution = neighbour;
        }
        else
        {
            // We've found a local optimum
            break;
        }
        LogIteration(i, 100, fitness, best_fitness, start);
    }
    return best_solution;
}

void SerializePlacement(std::ostream &ostream, const PlacedItems &items){
    for (const Item &rect : items)
    {
        ostream << rect.id << " " << rect.left() << " " << rect.top() << " " << rect.right() << " " << rect.bottom() << std::endl;
    }
}

void ShowUsage(std::string name)
{
    std::cout << "Usage: " << name << " <algorithm> <infile> <outfile> <result file> --max-iterations <num> --annealing" << std::endl;
    std::cout << "Algorithm can be one of:" << std::endl;
    std::cout << "  BL  - Bottom left heuristic" << std::endl;
    std::cout << "  LS  - Local Search" << std::endl;
    std::cout << "  LNS - Large neighbourhood search" << std::endl;
    std::cout << "  ALNS - Adaptive Large neighbourhood search" << std::endl;
    std::cout << "Outfile is the file to write the solution to." << std::endl;
    std::cout << "Result file is the file to write the result to." << std::endl;
    std::cout << "Max iterations is the maximum number of iterations to run for." << std::endl;
    std::cout << "Annealing is a flag to enable simulated annealing." << std::endl;
}

int main(int argc, char const *argv[])
{
    // Seed random number generator
    srand(time(NULL));

    bool simulated_annealing = false;
    int max_iterations = 1000;

    for (int i = 1; i < argc; i++)
    {
        if (std::string(argv[i]) == "--annealing"){
            simulated_annealing = true;
        }
        else if (std::string(argv[i]) == "--max-iterations")
        {
            i++;
            max_iterations = std::stoi(argv[i]);
        }
        else if (std::string(argv[i]) == "--help")
        {
            ShowUsage(argv[0]);
            return 0;
        }
    }
    if (argc < 4)
    {
        ShowUsage(argv[0]);
        return 0;
    }

    std::string algorithm = argv[1];
    std::string in_file = argv[2];
    std::string out_file = argv[3];
    std::string result_filename = argv[4];
    results_file = std::ofstream(result_filename);
    LogHeader();

    // Create a vector of items that need to be placed
    UnplacedItems unplaced;
    // Load items from standard in
    std::ifstream shape_file;
    shape_file.open(in_file);
    int num_items;
    shape_file >> num_items;
    for (int i = 0; i < num_items; i++) {
        int id, width, height;
        shape_file >> id >> width >> height;
        unplaced.push_back(Item(id, width, height));
    }

    PlacedItems best_placement;
    auto start = std::chrono::system_clock::now();

    if (algorithm == "BL")
        best_placement = BLPackItems(unplaced);
    else if (algorithm == "LS")
        best_placement = LocalSearch(unplaced);
    else if (algorithm == "LNS")
        best_placement = LargeNeighborhoodSearch(unplaced, 0.1, max_iterations, simulated_annealing);
    else if (algorithm == "ALNS")
        best_placement = AdaptiveLargeNeighborhoodSearch(unplaced, 0.1, max_iterations, simulated_annealing);
    else
    {
        std::cout << "Unknown algorithm: " << algorithm << std::endl;
        ShowUsage(argv[0]);
        return 1;
    }

    // Evaluate Solution
    int duration = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now() - start).count();
    std::cout << "> Evaluation" << "\n";
    std::cout << "     Packing Efficiency: " << Fitness(best_placement) * 100 << "%" << std::endl;
    std::cout << "     Packing Height:     " << PackingHeight(best_placement) << std::endl;
    std::cout << "     Elapsed Time:       " << duration << "ms" << std::endl;
    std::cout << "     Solution:          '" << StringifySolution(best_placement) << "'\n";
    // Save solution
    std::ofstream solution_file;
    solution_file.open(out_file);

    // Output Score
    solution_file << "# " << in_file 
                  << " " << algorithm 
                  << " " << Fitness(best_placement) 
                  << " " << PackingHeight(best_placement) 
                  << " " << duration 
                  << std::endl; 
    SerializePlacement(solution_file, best_placement);

    solution_file.close();
    return 0;
}
