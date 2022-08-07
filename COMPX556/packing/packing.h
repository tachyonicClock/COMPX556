#pragma once
#include <vector>
#include <iostream>
#include <stdio.h>
#include <fstream>

static std::ofstream results_file;

/// @brief The width of the strip to pack items into
const int kStripWidth = 100;

/**
 * A euclidean point
 */
class Vector2 {
public:
    int x, y;
    Vector2(int x, int y) : x(x), y(y) {}
    Vector2(): x(0), y(0) {}
};

/**
 * A rectangular item to be packed
 */
class Item
{
private:
    Vector2 bottom_left = Vector2(0, 0);
    Vector2 top_right = Vector2(0, 0);
public:
    int id;
    bool is_rotated = false;

    Item(int id, int width, int height): id(id) {
        bottom_left.x = 0;
        bottom_left.y = 0;
        top_right.x = width;
        top_right.y = height;
    }

    void rotate() {
        int temp = bottom_left.x;
        bottom_left.x = bottom_left.y;
        bottom_left.y = temp;
        temp = top_right.x;
        top_right.x = top_right.y;
        top_right.y = temp;
        is_rotated = !is_rotated;
    }

    void set_left(int left) {
        top_right.x = left + width();
        bottom_left.x = left; 
    }
    
    void set_top(int top) {
        bottom_left.y = top - height();
        top_right.y = top;
    }

    void set_right(int right) {
        bottom_left.x = right - width();
        top_right.x = right;
    }

    void set_bottom(int bottom) {
        top_right.y = bottom + height();
        bottom_left.y = bottom;
    }

    int left()   const { return bottom_left.x; }
    int right()  const { return top_right.x; }
    int top()    const { return top_right.y; }
    int bottom() const { return bottom_left.y; }
    int width()  const { return top_right.x - bottom_left.x; }
    int height() const { return top_right.y - bottom_left.y; }
    int area()   const { return width() * height(); }
    float aspect_ratio() const { return (float)width() / (float)height(); }
};

/// A vector of placed items
typedef std::vector<Item> PlacedItems;
/// A vector of unplaced items
typedef std::vector<Item> UnplacedItems;


PlacedItems BLFillItems(const UnplacedItems &items);
PlacedItems BLPackItems(const UnplacedItems &items);
Item BLHeuristic(Item to_place, const std::vector<Item> &placed_rects);


float Fitness(const PlacedItems &items);

inline void LogIteration(
    int iteration, 
    int max_iteration,
    float fitness,
    float best_fitness,
    clock_t start_time) {
    printf("Iteration %d/%d Fitness: %.02f%% Global Best: %.02f%%\n", iteration, max_iteration, fitness*100, best_fitness*100);
    results_file << iteration << " " << fitness << " " << best_fitness << " " << (float)(clock() - start_time) / CLOCKS_PER_SEC << std::endl;
}

static void LogHeader(){
    results_file << "Iteration Fitness GlobalBest Time" << std::endl;
}
