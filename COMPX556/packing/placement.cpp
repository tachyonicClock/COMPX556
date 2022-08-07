#include "packing.h"
#include <vector>
#include <iostream>
#include <limits>

inline bool DoRangesOverlap(int a_start, int a_end, int b_start, int b_end)
{
    return (a_start < b_end) && (b_start < a_end);
}

/**
 * @brief BLHeuristic is a heuristic for placing a rectangle towards the bottom 
 * left
 * 
 * The rectangle starts in the top left infinitely far away and is moved down
 * until it hits another rectangle or the edge. The rectangle is then slid
 * right until it hits another rectangle or the edge. The process is repeated
 * until the rectangle cannot be moved.
 * 
 * @param to_place A rectangle to be placed in the strip.
 * @param placed_rects A vector of already placed rectangles to work around
 * @return Rectangle The placed rectangle.
 */
Item BLHeuristic(Item to_place, const std::vector<Item> &placed_rects)
{
    // Move placement to the far right of the strip
    to_place.set_right(kStripWidth);
    to_place.set_top(100000);

    // std::cout << "Placing rectangle " << to_place.id << " at " << to_place.left() << ", " << to_place.top() << std::endl;

    while(true)
    {

        // 'drop' the rectangle until it hits something
        int closest_y = 0;
        int min_distance = std::numeric_limits<int>::max();
        for (const Item &other_rect : placed_rects)
        {
            if (!DoRangesOverlap(to_place.left(), to_place.right(), other_rect.left(), other_rect.right()))
                continue;

            int distance = to_place.top() - other_rect.top();
            if (distance < min_distance && distance >= 0)
            {
                min_distance = distance;
                closest_y = other_rect.top();
                // std::cout << "Dropped onto rectangle " << other_rect.id << " at " << other_rect.left() << ", " << other_rect.top() << std::endl;
                if (distance == 0)
                    break;
            }
        }
        if(to_place.bottom() == closest_y)
            break;
        to_place.set_bottom(closest_y);
        
        // 'slide' the rectangle left until it hits something
        int closest_x = 0;
        min_distance = std::numeric_limits<int>::max();
        for (const Item &other_rect : placed_rects)
        {
            if (!DoRangesOverlap(to_place.bottom(), to_place.top(), other_rect.bottom(), other_rect.top()))
                continue;

            int distance = to_place.left() - other_rect.right();
            if (distance < min_distance && distance >= 0)
            {
                min_distance = distance;
                closest_x = other_rect.right();
                // std::cout << "Slid onto rectangle " << other_rect.id << " at " << other_rect.left() << ", " << other_rect.top() << std::endl;
                if (distance == 0)
                    break;
            }
        }
        if(to_place.right() == closest_x)
            break;
        to_place.set_left(closest_x);
    }

    return to_place;
}

// Pack the given items using the bottom left heuristic
PlacedItems BLPackItems(const UnplacedItems &items){
    std::vector<Item> placed_rects;

    // Place initial rectangle in the bottom right corner of the strip
    Item initial_rect = items[0];
    initial_rect.set_left(0);
    initial_rect.set_bottom(0);
    placed_rects.push_back(initial_rect);

    // Place the rest of the rectangles
    for(int i = 1; i < items.size(); i++){
        // Initialize the rectangle in the right top
        Item new_rect = BLHeuristic(items[i], placed_rects);
        placed_rects.push_back(new_rect);
    }
    return placed_rects;
}
