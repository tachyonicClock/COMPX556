#include <stdexcept>
#include "packing.h"

/**
 * @brief The neighbourhoods are defined by using iterators. This is a bit
 * overkill given that I used LNS instead.
 * 
 */
class NeighbourhoodIterator {
public:
    virtual UnplacedItems Next() = 0;
    virtual bool HasNext() = 0;
};


/**
 * @brief Our neighbourhood is constructed by swapping any two elements in the
 * vector.
 */
class SwapNeighbourhood : public NeighbourhoodIterator {
private:
    const UnplacedItems items;
    int element_i = 0;
    int element_j = 1;
    int n = 0;
    int i = 0;
public:
    SwapNeighbourhood(const UnplacedItems& items): items(items){
        n = items.size();
    };

    UnplacedItems Next()
    {
        if (element_j < n)
        {
            UnplacedItems neighbour(items);
            std::swap(neighbour[element_i], neighbour[element_j]);
            element_j++;
            return neighbour;
        }

        element_i += 1;
        element_j = element_i+1;

        if (element_j >= n)
            throw std::runtime_error("No more neighbours");
        return Next();
    }

    bool HasNext()
    {
        return element_i < n-2;
    }
};

class CompositeNeighbourhood : public NeighbourhoodIterator {
private:
    std::vector<NeighbourhoodIterator*> iterators;
    int current_iterator = 0;
public:
    CompositeNeighbourhood(std::vector<NeighbourhoodIterator*> iterators): iterators(iterators){
        current_iterator = 0;
    };
    UnplacedItems Next()
    {
        if (!iterators[current_iterator]->HasNext()){
            current_iterator += 1;
        }

        return iterators[current_iterator]->Next();
    }
    bool HasNext()
    {
        return iterators[current_iterator]->HasNext() ||
               (current_iterator+1 < iterators.size());
    }
};


class RotateNeighbourhood : public NeighbourhoodIterator {
private:
    const UnplacedItems items;
    int element_i = 0;
    int n = 0;
public:
    RotateNeighbourhood(const UnplacedItems& items): items(items){
        n = items.size();
    };
    UnplacedItems Next()
    {
        if (element_i > n)
            throw std::runtime_error("No more neighbours");

        UnplacedItems neighbour(items);
        neighbour[element_i].rotate();
        element_i++;
        return neighbour;
    }

    bool HasNext()
    {
        return element_i < n;
    }
};
