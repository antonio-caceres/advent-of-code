"""Day 3: Binary Diagnostic"""

from dataclasses import dataclass

from utils import read


@dataclass
class BoolCounter:
    num_true: int = 0
    total: int = 0

    def count(self, boolean: bool):
        self.num_true += boolean
        self.total += 1

    def mode(self, tie_val: bool | None = None) -> bool | None:
        """Return the boolean that has been counted more, or ``tie_val`` in the case of a tie."""
        if self.num_true * 2 == self.total:
            return tie_val
        return self.num_true * 2 > self.total


def bools_to_int(bools):
    """Convert a list of booleans to an integer by treating it as a big-endian binary number."""
    result = 0
    for i, val in enumerate(bools[::-1]):
        result += (2 ** i) * val
    return result


def most_frequent_bools(bool_lists, tie_val = None):
    """Get the most frequent booleans per position from arrays of booleans.

    Args:
        bool_lists: lists of booleans to get the frequency from
        tie_val: boolean (or None) to use in the case of a tie in frequency

    Returns:
        list[bool], most frequent booleans per position, or ``tie_val`` in the case of a tie.
    """
    counters = []

    for bools in bool_lists:
        for idx, val in enumerate(bools):
            assert idx <= len(counters)  # enforce invariant
            if idx == len(counters):
                counters.append(BoolCounter())
            counters[idx].count(val)

    return [counter.mode(tie_val) for counter in counters]


def power_consumption(bool_lists):
    """Get the power consumption from binary lists, as defined by the puzzle.

    The power consumption is the product of gamma and epsilon values,
    where gamma is a binary number composed of the most frequent bits in the lists (per position),
    and epsilon is, similarly, a binary number composed of the least frequent bits.
    The numbers are treated as big-endian numbers.

    If the lists provided are of different lengths, the lists are compared index-wise.
    This design choice is intuitive from an algorithmic point of view, but could be a
    surprise if binary numbers of different representation sizes are used.

    Raise ``ValueError`` if any of the positional frequencies are ties.
    """
    gamma_list = most_frequent_bools(bool_lists)
    if None in gamma_list:
        raise ValueError(f"most common boolean was a tie at position: {gamma_list.index(None)}")
    # take the bitwise xor of the gamma string
    epsilon_list = [not x for x in gamma_list]
    return bools_to_int(gamma_list) * bools_to_int(epsilon_list)


def filtered_frequent_bool(bool_lists, tie_val=None, least_frequent=False):
    """Return a boolean list using the positional bit frequency counts and a filter.

    Given a list of boolean lists, count the most frequent bool in the first position.
    (Use the least frequent bool if ``least_frequent`` is ``True``.)
    In the case of a tie, use the bool indicated by ``tie_val``.
    Then, filter for only those strings that do not contain that bool in the first position.
    Repeat for all positions, and returns the resulting string.

    Args:
        bool_lists: list[list[bool]], boolean lists to generate the frequency string from
        tie_val: default bool to use in the case of a frequency tie
        least_frequent: if the least frequent bit should be used instead

    Returns:
        binary string according to the algorithm above
    """
    filtered = {False: [], True: []}

    for bools in bool_lists:
        if len(bools) > 0:
            filtered[bools[0]].append(bools[1:])

    match len(filtered[False]), len(filtered[True]):
        case 0, 0:
            return []
        # if there are no numbers for a given boolean, use the other
        case 0, _:
            result_bool = True
        case _, 0:
            result_bool = False
        case len_false, len_true if len_false == len_true:
            result_bool = tie_val
        case len_false, len_true:
            result_bool = (len_false < len_true) ^ least_frequent

    # noinspection PyUnboundLocalVariable
    # Pycharm is not smart enough at pattern matching (yet).
    return [result_bool] + filtered_frequent_bool(filtered[result_bool], tie_val, least_frequent)


def life_support(bool_lists):
    """Get the life support rating from binary lists, as defined by the puzzle.

    The life support rating is the product of oxygen generator and CO2 scrubber ratings.
    Both are calculated according to the algorithm run by ``filtered_frequent_bool``,
    where the oxygen generator rating has ``tie_val = True`` and ``least_frequent == False``,
    and the CO2 scrubber rating has ``tie_val = False`` and ``least_frequent == True``.

    The values are then treated as big-endian numbers, and multiplied to get the life support rating.
    """
    oxygen_rating = bools_to_int(filtered_frequent_bool(bool_lists, tie_val=True, least_frequent=False))
    co2_rating = bools_to_int(filtered_frequent_bool(bool_lists, tie_val=False, least_frequent=True))
    return oxygen_rating * co2_rating


if __name__ == "__main__":
    binary_report = read.dayta(day=3, line_parser=lambda s: [bool(int(c)) for c in s])
    print(f"Part One: {power_consumption(binary_report)}")
    print(f"Part Two: {life_support(binary_report)}")
