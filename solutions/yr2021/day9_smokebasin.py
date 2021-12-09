"""Day 9: Smoke Basin"""

import heapq

import numpy as np

from utils import read


def adjacent_indices(index, shape):
    """Iterate over all the valid adjacent indices of a given index within a given array shape.

    Does not check that index is a valid index for shape.
    """
    for dim, dim_size in enumerate(shape):
        if index[dim] > 0:
            yield *index[:dim], index[dim] - 1, *index[dim+1:]
        if index[dim] < dim_size - 1:
            yield *index[:dim], index[dim] + 1, *index[dim+1:]


def is_local_min(nums, index):
    """If the index is a local minimum of the array ``nums``.

    Considers the (``dim * 2``) adjacent heights, where ``dim`` is the dimension of ``heightmap``
    """
    return all((nums[index] < nums[adjacent] for adjacent in adjacent_indices(index, nums.shape)))


def sum_risk_levels(heightmap):
    """Sum the risk levels of the local minimums in an array of integers.

    The risk level of a given height is ``height + 1``.
    A height is only considered to have a risk level if it is a local minimum of ``heightmap``.
    """
    risk_level_sum = 0
    for index, height in np.ndenumerate(heightmap):
        if is_local_min(heightmap, index):
            risk_level_sum += height + 1
    return risk_level_sum


MAX_FLOW_HEIGHT = 8


def basin_size(heightmap, index):
    """Find the total number of heightmap indices that "flow downward" to the given index.

    A height "flows downward" to itself.
    If any of the adjacent heights are greater than or equal to the height at ``index``,
    they are considered to "flow downward" to the index.
    Any height that is adjacent to a height that "flows downward" to ``index``, with a
    height that is greater than or equal to the adjacent index in question,
    is also considered to "flow downward" to the index.

    If an index has a height > 8, it is not considered to "flow downward" to any index other than itself,
    even if it has a height that is greater than or equal to an adjacent height.

    Args:
        heightmap: 2D array of heights
        index: index of the 2D array of heights to calculate the basin size for

    Returns:
        total number of indices that "flow downward"
    """
    visited = set()
    index_queue = [index]

    while len(index_queue) > 0:
        if (cur := index_queue.pop()) in visited:
            continue
        visited.add(cur)
        for adjacent in adjacent_indices(cur, heightmap.shape):
            if heightmap[cur] <= heightmap[adjacent] <= MAX_FLOW_HEIGHT:
                index_queue.append(adjacent)

    return len(visited)


def multiply_large_risk_basins(heightmap, n_largest=None):
    """Multiply the size of the ``n_largest`` "risk basins" from ``heightmap``.

    A basin is a "risk basin" if it is the basin of a local minimum of ``heightmap``.
    This function finds the size of all disjoint basins in ``heightmap`` if (converse false)
    adjacent heights are never equal and basins are separated by "walls" of height >8.

    Note that this function does not consider basins where the lowest height level forms a
    "plateau" of equal heights, because those indices are not considered local minimums.

    Args:
        heightmap: n-dimensional array of heights
        n_largest: number of the largest risk basins to consider
            If ``None``, considered all the largest risk basins.
    """
    largest_sizes = []
    for index, height in np.ndenumerate(heightmap):
        if is_local_min(heightmap, index):
            risk_basin_size = basin_size(heightmap, index)
            if n_largest is not None and len(largest_sizes) == n_largest:
                heapq.heappushpop(largest_sizes, risk_basin_size)
            else:
                heapq.heappush(largest_sizes, risk_basin_size)
    return np.prod(largest_sizes)


if __name__ == "__main__":
    cave_height_lists = read.dayta(day=9, line_parser=lambda line: [int(num) for num in line])
    cave_heights = np.array(cave_height_lists)
    print(f"Part 1: {sum_risk_levels(cave_heights)}")
    print(f"Part 2: {multiply_large_risk_basins(cave_heights, n_largest=3)}")
