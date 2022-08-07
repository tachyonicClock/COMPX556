#include <algorithm>
#include <limits>
#include <cmath>
#include "packing.h"
#include "lns.h"

float AttemptSwap(UnplacedItems items, int item_a, int item_b) {
    std::swap(items[item_a], items[item_b]);
    PlacedItems placed_items = BLPackItems(items);
    return Fitness(placed_items);
}


/**
 * @brief Repair the given list of items by swapping the destroyed items with other items.
 * Such that the resulting packing is the best possible.
 * 
 * @param destroyed_items 
 * @param items 
 * @return UnplacedItems 
 */
UnplacedItems RepairWithSwap(const SortIndicies &destroyed_items, UnplacedItems items)
{
    for (int i = 0; i < destroyed_items.size(); i++) {

        float best_fitness = 0;
        int best_item_a = -1;
        int best_item_b = -1;

        for (int j = 0; j < items.size(); j++) {
            // Don't swap with itself
            if (i == j)
                continue;

            // Dont swap with destroyed items
            // TODO Might be a faster way to do this
            if (std::find(destroyed_items.begin(), destroyed_items.end(), j) != destroyed_items.end())
                continue;

            int item_a = destroyed_items[i];
            int item_b = j;
    
            float fitness = AttemptSwap(items, item_a, item_b);
            if (fitness > best_fitness) {
                best_fitness = fitness;
                best_item_a = item_a;
                best_item_b = item_b;
            }
        }

        // Perform swap
        if (best_item_a != -1 && best_item_b != -1) 
            std::swap(items[best_item_a], items[best_item_b]);
        else
            throw std::runtime_error("Could not repair with swap!");
    }
    return items;
}

UnplacedItems RepairWithRotate(const SortIndicies &destroyed_items, UnplacedItems items){
    float current_fitness = Fitness(BLPackItems(items));

    for (int i = 0; i < destroyed_items.size(); i++) {
        items[destroyed_items[i]].rotate();

        // If the fitness improves we keep the rotate else we revert it
        float new_fitness = Fitness(BLPackItems(items));
        if (new_fitness > current_fitness) {
            current_fitness = new_fitness;
        } else {
            items[destroyed_items[i]].rotate();
        }
    }
    return items;
}

int BestInsert(Item to_insert, UnplacedItems items) {
    float best_fitness = std::numeric_limits<float>::lowest();
    int best_insert = 0;

    // Try inserting into all positions
    for (int i = 0; i < items.size(); i++) {
        items.insert(items.begin() + i, Item(to_insert));
        float fitness = Fitness(BLPackItems(items));
        if (fitness > best_fitness) {
            best_fitness = fitness;
            best_insert = i;
        }
        items.erase(items.begin() + i);
    }

    return best_insert;
}

UnplacedItems RepairWithInsert(const SortIndicies &destroyed_items, UnplacedItems items){
    // Remove the destroyed items from the list
    UnplacedItems remaining(items.begin(), items.end());
    // Sort destroy items
    SortIndicies destroyed_items_sorted = destroyed_items;
    std::sort(destroyed_items_sorted.begin(), destroyed_items_sorted.end(), std::greater<int>());
    // Remove the destroyed items from the list
    for (int i = 0; i < destroyed_items_sorted.size(); i++) {
        remaining.erase(remaining.begin() + destroyed_items_sorted[i]);
    }

    // Attempt to insert the destroyed items into the remaining items
    for (int i = 0; i < destroyed_items.size(); i++) {
        Item item = items[destroyed_items[i]];
        int position = BestInsert(item, remaining);
        remaining.insert(remaining.begin() + position, item);
    }


    return remaining;
}


UnplacedItems Repair(RepairMethod method, 
    const SortIndicies &destroyed_items, 
    const UnplacedItems &items) {
    switch (method) {
        case SWAP:
            return RepairWithSwap(destroyed_items, items);
        case ROTATE:
            return RepairWithRotate(destroyed_items, items);
        case INSERT:
            return RepairWithInsert(destroyed_items, items);
        default:
            throw std::runtime_error("Unknown repair method");
    }
}

