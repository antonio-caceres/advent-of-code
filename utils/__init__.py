
from . import read

_PUZZLE_INPUT_FILE = "data/day{}.txt"


def data_file(day):
    """Location of the puzzle input file for `day`, relative to the year directory."""
    return _PUZZLE_INPUT_FILE.format(day)
