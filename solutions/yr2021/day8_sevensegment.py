"""(2021) Day 8: Seven Segment Search"""

from utils import read


def digit_pattern_parser(segment_words):
    """Parse an iterable of strings into an iterable of sets of their characters.

    In the context of this puzzle, the segment patterns (represented as strings)
    are turned into sets so set operations can be used to solve the puzzle.
    """
    return [{c for c in word} for word in segment_words]


def pattern_line_parser(line):
    """Parse a line of the puzzle input."""
    signal_str, output_str = line.split(" | ")
    signal_patterns = digit_pattern_parser(signal_str.split(" "))
    output_patterns = digit_pattern_parser(output_str.split(" "))
    return signal_patterns, output_patterns


def _display_step_one(patterns, digit_mapping):
    """Deduce patterns (1, 4, 7, 8) using only the numbers of segments."""
    for pattern in patterns:
        match len(pattern):
            case 2:  # 2 segments ==> digit == 1
                digit_mapping[1] = pattern
            case 4:  # 4 segments ==> digit == 4
                digit_mapping[4] = pattern
            case 3:  # 3 segments ==> digit == 7
                digit_mapping[7] = pattern
            case 7:  # 7 segments ==> digit == 8
                digit_mapping[8] = pattern


STEP_TWO_KNOWN = [1, 4, 7, 8]


def _display_step_two(patterns, digit_mapping):
    """Deduce patterns (2, 3, 6, 9) using set operation strategies with known patterns (1, 4, 7, 8)."""
    if None in {digit_mapping[x] for x in STEP_TWO_KNOWN}:
        raise ValueError(f"digits {STEP_TWO_KNOWN} did not all have valid patterns")

    for pattern in patterns:
        if len(pattern) == 5:  # possibly 2, 3, 5
            if pattern | digit_mapping[4] == digit_mapping[8]:
                digit_mapping[2] = pattern
            elif pattern & digit_mapping[7] == digit_mapping[7]:  # pattern contains all of 7
                digit_mapping[3] = pattern
            else:
                digit_mapping[5] = pattern
        if len(pattern) == 6:  # possibly 0, 6, 9
            if pattern | digit_mapping[1] == digit_mapping[8]:  # pattern + 1 -> 8
                digit_mapping[6] = pattern
            elif pattern & digit_mapping[4] == digit_mapping[4]:  # pattern contains all of 4
                digit_mapping[9] = pattern
            else:
                digit_mapping[0] = pattern


def digit_segment_mapping(patterns):
    """Deduce the mapping from a set of digit seven-segment patterns to the digits 0-9.

    A digit segment pattern is a string, where each character maps to a segment on a seven-segment display.
    Within a set of patterns, the patterns should be composed of at most 7 unique characters
    (corresponding to each of the seven segments).
    If more than 7 unique characters are present across the set of patterns,
    there does not exist a valid pattern-digit mapping for this set of patterns.

    The patterns given should be valid. If they are not valid, it is likely because
    there are patterns in the mapping that correspond to non-digit shapes (on the seven-segment display).
    The returned mapping in this case will likely be self-contradictory, because not all
    deduction strategies employed (set intersection or process of elimination) work
    if the set of patterns provided is arbitrary.

    Args:
        patterns: set (10-length iterable) of patterns to construct a mapping out of

    Returns:
        10-length list of patterns, where the pattern at index ``i`` maps to digit ``i``.
        If the pattern for digit ``i`` is not known, the pattern at index ``i`` is ``None``.
        (the fixed-length list acts like a bidirectional mapping using the ``.index`` function;
        because only 10 digits are ever used, the indexing is constant time.)
    """
    patterns = set(frozenset(pattern) for pattern in patterns)
    if len(patterns) != 10:
        raise ValueError(f"number of unique patterns was not 10: {len(patterns)}")

    digit_mapping = [None] * 10  # none of the patterns are known
    _display_step_one(patterns, digit_mapping)
    _display_step_two(patterns, digit_mapping)

    return digit_mapping


def count_digit_patterns(mapping, patterns, targets):
    """Count the number of target digits in a set of patterns, provided a mapping.

    Args:
        mapping: 10-length list mapping from digit segment patterns to digits
            The pattern at index ``i`` maps to digit ``i``, or is ``None`` if no pattern maps to digit ``i``.
        patterns: iterable of patterns to check for the target digits
        targets: target digits to check the patterns against

    Returns:
        total number of times the target digits were found in ``patterns``
    """
    num_target_digits = 0
    for pattern in patterns:
        if pattern in mapping and mapping.index(pattern) in targets:
            num_target_digits += 1
    return num_target_digits


def patterns_to_int(mapping, patterns):
    """Convert an iterable of seven-segment digit patterns into an integer.

    The first pattern in the iterable is the first digit in the integer, etc.

    Args:
        mapping: 10-length list mapping from digit segment patterns to digits
            The pattern at index ``i`` maps to digit ``i``, or is ``None`` if no pattern maps to digit ``i``.
        patterns: iterable of patterns to convert to an integer

    Returns:
        seven-segment digit patterns as an integer
    """
    result = 0
    for i, pattern in enumerate(patterns[::-1]):
        result += 10 ** i * mapping.index(pattern)
    return result


if __name__ == "__main__":
    puzzle_inputs = read.dayta(day=8, line_parser=pattern_line_parser)
    num_simple_digits = 0  
    simple_digits = {1, 4, 7, 8}
    sum_puzzle_patterns = 0
    for line_patterns, line_outputs in puzzle_inputs:
        line_mapping = digit_segment_mapping(line_patterns)
        num_simple_digits += count_digit_patterns(line_mapping, line_outputs, simple_digits)
        sum_puzzle_patterns += patterns_to_int(line_mapping, line_outputs)
    print(f"Part 1: {num_simple_digits}")
    print(f"Part 2: {sum_puzzle_patterns}")
