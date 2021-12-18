"""(2021) Day 10: Syntax Scoring"""

from enum import Enum

from utils import read

BRACKETS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CORRUPTED_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

INCOMPLETE_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


class BracketsStatus(Enum):
    VALID = "valid"
    CORRUPTED = "corrupted"
    INCOMPLETE = "incomplete"


def check_brackets(bracket_string):
    """Check if a string containing brackets is valid ordering of opening and closing brackets.

    Bracket pairs are '()', '[]', '{}', and '<>'.
    A string with interposing non-bracket characters are supported.

    Args:
        bracket_string: string of brackets to check

    Returns:
        Status, error of the bracket check.
        BracketsStatus.VALID for a valid string; ``error`` is ``None``.
        BracketsStatus.CORRUPTED for an unexpected closing bracket; ``error`` is the corrupted character.
        BracketsStatus.INCOMPLETE for opening brackets that were not closed; error is the list of unclosed brackets.
            The unclosed brackets should be closed in the reverse order of the list provided
            (i.e., first in the returned list is also first in the string, and should be closed last).
    """
    opening_stack = []
    for c in bracket_string:
        if c in BRACKETS.keys():
            opening_stack.append(c)
        elif c in BRACKETS.values():
            if len(opening_stack) == 0 or BRACKETS[opening_stack.pop()] != c:
                return BracketsStatus.CORRUPTED, c
    if len(opening_stack) > 0:
        return BracketsStatus.INCOMPLETE, opening_stack
    return BracketsStatus.VALID, None


def sum_corrupted_errors(bracket_strings):
    """Sum the corrupted scores for all corrupted lines.

    Syntax error scores are given by ``CORRUPTED_SCORES``, where the key
    represents the **actual** closing bracket in the corrupted line.
    """
    syntax_error_sum = 0
    for b_string in bracket_strings:
        status, error = check_brackets(b_string)
        if status == BracketsStatus.CORRUPTED and error is not None:
            syntax_error_sum += CORRUPTED_SCORES[error]
    return syntax_error_sum


def get_incomplete_score(bracket_string):
    """Get the incomplete scores for a bracket string.

    The incomplete score is 0 if the string is valid or corrupted.
    Otherwise, for each closing bracket that must be appended (in that order) to validate the string,
    the following two-step algorithm is performed to calculate the incomplete score:

    1. Multiply the current score by 5. (For the first closing bracket, begin with a score of 0.)
    2. Add the score of the closing bracket, according to ``INCOMPLETE_SCORES``, to the total score.
    """
    status, error = check_brackets(bracket_string)
    if status != BracketsStatus.INCOMPLETE:
        return 0
    incomplete_score = 0
    for opening in error[::-1]:
        incomplete_score *= 5
        incomplete_score += INCOMPLETE_SCORES[BRACKETS[opening]]
    return incomplete_score


def median_incomplete_score(bracket_strings):
    """Get the median non-zero incomplete score for an iterable of bracket strings."""
    incomplete_scores = []
    for b_string in bracket_strings:
        if (score := get_incomplete_score(b_string)) > 0:
            incomplete_scores.append(score)
    if len(incomplete_scores) == 0:
        return None

    incomplete_scores.sort()
    median_idx = (len(incomplete_scores) - 1) // 2
    if len(incomplete_scores) % 2 == 0:
        return (incomplete_scores[median_idx] + incomplete_scores[median_idx + 1]) / 2
    else:
        return incomplete_scores[median_idx]


if __name__ == "__main__":
    puzzle_strings = read.dayta(day=10)
    print(f"Part One: {sum_corrupted_errors(puzzle_strings)}")
    print(f"Part Two: {median_incomplete_score(puzzle_strings)}")
