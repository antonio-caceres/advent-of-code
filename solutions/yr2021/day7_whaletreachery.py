"""Day 7: The Treachery of Whales"""

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

    min_distance = 0
    min_center = round(sum(nums) / len(nums) - 0.25)
    for num in nums:
        dist = abs(num - min_center)
        # (dist + 1) * dist is always even because even * odd (floor div is just converting to int)
        min_distance += ((dist + 1) * dist) // 2
    return min_distance


if __name__ == "__main__":
    parsed_lines = read.dayta(day=7, line_parser=lambda line: [int(x) for x in line.split(",")])
    for crab_locs in parsed_lines:
        print(f"Part 1: {min_abs_distance(crab_locs)}")
        print(f"Part 2: {min_scaling_distance(crab_locs)}")
