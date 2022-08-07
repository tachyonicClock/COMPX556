#pragma once
#include <utility>
#include "packing.h"

/// @brief Indicies of the items in the given vector, sorted by some method
typedef std::vector<int> SortIndicies;

/// @brief The initial temperature of the simulated annealing
static const float kInitialTemperature = 1.0;
/// @brief Score given to a destruction/repair for a new global best
static const int kGlobalBestPoints = 2;
/// @brief Score given to a destruction/repair for an accepted solution
static const int kAcceptPoints = 1;

enum DestructionMethod {
    AREA_ASC,
    ASPECT_RATIO_ASC,
    HEIGHT_ASC,
    WIDTH_ASC,
    AREA_DESC,
    ASPECT_RATIO_DESC,
    HEIGHT_DESC,
    WIDTH_DESC,
    RANDOM,
    DESTROY_NUM_METHODS
};

enum RepairMethod {
    INSERT,
    ROTATE,
    SWAP,
    REPAIR_NUM_METHODS
};

SortIndicies Destroy(DestructionMethod method, float fraction, const UnplacedItems &items);
UnplacedItems Repair(RepairMethod method, const SortIndicies &destroyed_items, const UnplacedItems &items);
PlacedItems LargeNeighborhoodSearch(
    const UnplacedItems &items, 
    float fraction_to_destroy,
    int max_iterations,
    bool simulated_annealing = false
);
PlacedItems AdaptiveLargeNeighborhoodSearch(
    const UnplacedItems &items, 
    float fraction_to_destroy,
    int max_iterations,
    bool simulated_annealing = false
);