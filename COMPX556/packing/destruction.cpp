#include <algorithm>
#include <limits>
#include <cmath>
#include "packing.h"
#include "lns.h"

/// @brief Create a sequence e.g 1, 2, 3, ..., n
inline SortIndicies Sequence(int n) {
    std::vector<int> v(n);
    for (int i = 0; i < n; i++)
        v[i] = i;
    return v;
}

SortIndicies SortByArea(const UnplacedItems &items) {
    SortIndicies indices = Sequence(items.size());
    std::sort(indices.begin(), indices.end(), [&items](int i1, int i2) {
        return items[i1].area() > items[i2].area();
    });
    return indices;
}

SortIndicies SortByAspectRatio(const UnplacedItems &items) {
    SortIndicies indices = Sequence(items.size());
    std::sort(indices.begin(), indices.end(), [&items](int i1, int i2) {
        return items[i1].aspect_ratio() > items[i2].aspect_ratio();
    });
    return indices;
}

SortIndicies SortByHeight(const UnplacedItems &items) {
    SortIndicies indices = Sequence(items.size());
    std::sort(indices.begin(), indices.end(), [&items](int i1, int i2) {
        return items[i1].height() > items[i2].height();
    });
    return indices;
}

SortIndicies SortByWidth(const UnplacedItems &items) {
    SortIndicies indices = Sequence(items.size());
    std::sort(indices.begin(), indices.end(), [&items](int i1, int i2) {
        return items[i1].width() > items[i2].width();
    });
    return indices;
}

SortIndicies Random(const UnplacedItems &items) {
    SortIndicies indices = Sequence(items.size());
    std::random_shuffle(indices.begin(), indices.end());
    return indices;
}

/// @brief Return some fraction of the given vector
SortIndicies SomeFraction(float fraction, const SortIndicies &indicies) {
    int n = indicies.size();
    int n_to_keep = (int)(fraction * n);       
    return SortIndicies(indicies.begin(), indicies.begin() + n_to_keep);
}

/// @brief Reverse the order of the given vector
SortIndicies Reverse(const SortIndicies &items) {
    return SortIndicies(items.rbegin(), items.rend());
}

/**
 * @brief Return a list of indicies to be 'destroyed' and then 'repaired'
 * @param method The method to use for destruction.
 * @param fraction The fraction of items to destroy.
 * @param items The list of items to destroy.
 * @return The list of items that were destroyed.
 */
std::vector<int> Destroy(DestructionMethod method, float fraction, const UnplacedItems &items)
{
    switch (method) {
        case AREA_ASC:
            return SomeFraction(fraction, SortByArea(items));
        case AREA_DESC:
            return SomeFraction(fraction, Reverse(SortByArea(items)));
        case ASPECT_RATIO_ASC:
            return SomeFraction(fraction, SortByAspectRatio(items));
        case ASPECT_RATIO_DESC:
            return SomeFraction(fraction, Reverse(SortByAspectRatio(items)));
        case HEIGHT_ASC:
            return SomeFraction(fraction, SortByHeight(items));
        case HEIGHT_DESC:
            return SomeFraction(fraction, Reverse(SortByHeight(items)));
        case WIDTH_ASC:
            return SomeFraction(fraction, SortByWidth(items));
        case WIDTH_DESC:
            return SomeFraction(fraction, Reverse(SortByWidth(items)));
        case RANDOM:
            // return Random(items);
            return SomeFraction(fraction, Random(items));
        default:
            throw std::runtime_error("Unknown destruction method");
    }
}