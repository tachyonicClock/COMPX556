#include <algorithm>
#include <limits>
#include <cmath>
#include "packing.h"
#include "lns.h"

/**
 * @brief Sometimes accept a worse solution to escape local minima if the temperature is high enough
 *
 * @param temperature How likely we are to accept a worse solution
 * @param fitness The fitness of the current solution
 * @param prev_fitness The fitness of the previous solution
 * @return true Accept the new solution
 * @return false Reject the new solution
 */
bool SimulatedAnnealing(float temperature, float fitness, float prev_fitness)
{
    if (fitness >= prev_fitness)
        return true;
    float accept_prob = exp(-(prev_fitness - fitness) / temperature);
    return accept_prob > (float)rand() / RAND_MAX;
}

/**
 * @brief Optimization by destroying and repairing a fraction of the items each iteration
 *
 * @param items The items to pack
 * @param fraction_to_destroy The fraction of items to destroy each iteration
 * @param max_iterations The maximum number of iterations to run
 * @param simulated_annealing Whether to use simulated annealing
 * @return PlacedItems
 */
PlacedItems LargeNeighborhoodSearch(
    const UnplacedItems &items,
    float fraction_to_destroy,
    int max_iterations,
    bool simulated_annealing)
{
    clock_t start = clock();
    float best_fitness = std::numeric_limits<float>::lowest();
    float prev_fitness = std::numeric_limits<float>::lowest();
    PlacedItems best_placement = items;
    PlacedItems prev_placement = items;

    for (int i = 0; i < max_iterations; i++)
    {
        float temperature = 1.0f - (float)i / max_iterations;
        temperature *= kInitialTemperature;

        SortIndicies destroyed_items = Destroy(RANDOM, fraction_to_destroy, prev_placement);
        UnplacedItems repaired_items = Repair(SWAP, destroyed_items, prev_placement);
        PlacedItems placed_items = BLPackItems(repaired_items);
        float fitness = Fitness(placed_items);

        // Accept
        if (SimulatedAnnealing(temperature, fitness, prev_fitness) && simulated_annealing)
        {
            prev_fitness = fitness;
            prev_placement = placed_items;
        }

        // Update best
        if (fitness > best_fitness)
        {
            best_fitness = fitness;
            best_placement = placed_items;
            prev_placement = placed_items;
        }

        // Print to stdout
        LogIteration(i, max_iterations, fitness, best_fitness, start);
    }

    return best_placement;
}

int RouletteWheelSelection(const std::vector<int> &probability_score)
{
    int total = 0;
    for (int i = 0; i < probability_score.size(); i++)
        total += probability_score[i];

    int r = rand() % total;
    // Roulette wheel selection
    for (int i = 0; i < probability_score.size(); i++)
    {
        r -= probability_score[i];
        if (r < 0)
            return i;
    }
    return -1;
}

PlacedItems AdaptiveLargeNeighborhoodSearch(
    const UnplacedItems &items,
    float fraction_to_destroy,
    int max_iterations,
    bool simulated_annealing)
{
    clock_t start = clock();

    // Initialize destruction/repair method scores
    std::vector<int> destruction_score(DestructionMethod::DESTROY_NUM_METHODS, 1);
    std::vector<int> repair_scores(RepairMethod::REPAIR_NUM_METHODS, 1);

    float best_fitness = std::numeric_limits<float>::lowest();
    float prev_fitness = std::numeric_limits<float>::lowest();
    PlacedItems best_placement = items;
    PlacedItems prev_placement = items;

    for (int i = 0; i < max_iterations; i++)
    {
        float temperature = 1.0f - (float)i / max_iterations;
        temperature *= kInitialTemperature;

        // Randomly select a destruction and repair method based on their scores
        DestructionMethod destroy = (DestructionMethod)RouletteWheelSelection(destruction_score);
        RepairMethod repair = (RepairMethod)RouletteWheelSelection(repair_scores);

        // Destroy and repair the items
        SortIndicies destroyed_items = Destroy(destroy, fraction_to_destroy, prev_placement);
        UnplacedItems repaired_items = Repair(repair, destroyed_items, prev_placement);
        PlacedItems placed_items = BLPackItems(repaired_items);
        float fitness = Fitness(placed_items);

        // Accept
        if (SimulatedAnnealing(temperature, fitness, prev_fitness) && simulated_annealing)
        {
            prev_fitness = fitness;
            prev_placement = placed_items;
            destruction_score[(int)destroy] += kAcceptPoints;
            repair_scores[(int)repair] += kAcceptPoints;
        }

        // New Global Best
        if (fitness > best_fitness)
        {
            best_fitness = fitness;
            best_placement = placed_items;
            prev_placement = placed_items;
            destruction_score[(int)destroy] += kGlobalBestPoints;
            repair_scores[(int)repair] += kGlobalBestPoints;
        }

        // Print to stdout
        LogIteration(i, max_iterations, fitness, best_fitness, start);
    }

    // Print Scores
    std::cout << "Destruction Scores: ";
    for (int i = 0; i < destruction_score.size(); i++)
        std::cout << destruction_score[i] << " ";
    std::cout << std::endl;
    std::cout << "Repair Scores: ";
    for (int i = 0; i < repair_scores.size(); i++)
        std::cout << repair_scores[i] << " ";
    std::cout << std::endl;
    return best_placement;
}