"""Day 1: Sonar Sweep"""

import utils


def count_increasing_windows(nums, length):
    """
    Count the times the sum of a sliding window increases over an array.

    The sliding window is an interval of `length` integers;
    sum the numbers in the window and compare to the sum of the next window.

    Args:
        nums: iterable to compare the sliding windows of.
        length: length of the sliding window interval.

    Returns:
        number of times the sliding window sum (strictly) increases over `nums`.
        Returns 0 if the window length is larger than `nums`.
    """
    if len(nums) <= length:
        return 0
    # Ignore the intersection of the two windows because their contributions are equal.
    comparisons = [nums[i + length] > nums[i] for i in range(len(nums) - length)]
    return sum(comparisons)


if __name__ == "__main__":
    puzzle_input = utils.parse_dayta(day=1, line_parser=int)
    print(f"Part One: {count_increasing_windows(puzzle_input, length=1)}")
    print(f"Part Two: {count_increasing_windows(puzzle_input, length=3)}")
