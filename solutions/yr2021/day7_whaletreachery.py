"""(2021) Day 7: The Treachery of Whales"""

import math
from collections import Counter

from utils import read


def min_abs_distance(nums):
    """Find the minimum sum of distances between ``nums`` and an integer.

    Minimizes, over ``N``, the sum of ``|n - N|`` for every ``n`` in ``nums``.
    The sum is clearly concave up over ``N``, and by taking the derivative to optimize,
    it's clear that the minimum ``N`` is an integer that divides ``nums`` in half.
    This minimum ``N`` is not always unique, but the minimum sum of distances is unique.
    """
    if len(nums) == 0:
        return 0

    num_counter = Counter(nums)
    num_counts = sorted(list(num_counter.items()), key=lambda tup: tup[0])
    count_sum = 0
    for num, count in num_counts:
        count_sum += count
        if count_sum * 2 >= len(nums):
            min_center = num
            break
    else:
        assert False, f"did not hit the halfway count: {count_sum} / {len(nums)}"
    min_distance = 0
    for num, count in num_counter.items():
        min_distance += count * abs(num - min_center)
    return min_distance


def min_scaling_distance(nums):
    """Find the minimum integer sum of linearly scaling distances between ``nums`` and an integer.

    Minimizes, over ``N``, the sum of ``|n - N - k|, for ``k`` between 0 and ``n - N``,
    and for every ``n`` in ``nums``.
    The sum is clearly concave up over ``N``, and by taking the derivative to optimize,
    it's clear that the minimum ``N`` is ``avg(n) - 0.25``.
    This could be a non-integer, but the sum must be an integer, so we round the solution
    to the nearest integer.
    """
    if len(nums) == 0:
        return 0

    def scaling_distance(dist):
        # (dist + 1) * dist is always even because even * odd (floor div is just converting to int)
        return ((dist + 1) * dist) // 2

    min_dist_floor, min_dist_ceil = 0, 0
    min_center = sum(nums) / len(nums) - 0.25
    min_floor, min_ceil = math.floor(min_center), math.ceil(min_center)
    for num in nums:
        dist_floor = abs(num - min_floor)
        dist_ceil = abs(num - min_ceil)
        min_dist_floor += scaling_distance(dist_floor)
        min_dist_ceil += scaling_distance(dist_ceil)

    return min(min_dist_floor, min_dist_ceil)


if __name__ == "__main__":
    parsed_lines = read.dayta(day=7, line_parser=read.iter_parser(int, ","))
    for crab_locs in parsed_lines:
        print(f"Part One: {min_abs_distance(crab_locs)}")
        print(f"Part Two: {min_scaling_distance(crab_locs)}")
