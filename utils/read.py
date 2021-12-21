"""For reading Advent of Code's puzzle input files into data structures."""

from typing import Any, Callable

_PUZZLE_INPUT_FILE = "data/day{}.txt"


def data_file(day: int):
    """Puzzle input file object for `day`."""
    return open(_PUZZLE_INPUT_FILE.format(day))


def dayta(day: int, line_parser: Callable[[str], Any] = str):
    """Parse the lines (with stripped '\n') from a data file for a given day."""
    with data_file(day) as f:
        return [line_parser(line) for line in f.read().splitlines(keepends=False)]


def iter_parser(parser: Callable[[str], Any] = str, sep: str | None = None):
    """Return a line parsing function that splits and parses a string into a list.

    Built to easily create list-comprehension parsers for use with ``read.lines``.

    Args:
        parser: Function to call on the individual components of the split string.
        sep: String to split the string on. If ``None``, parses character-by-character.

    Returns:
        Callable[[str], list]. Function that splits a string on ``sep`` and parses into a list.
    """
    def iterating_parser(line):
        iter_s = line if sep is None else line.split(sep)
        return [parser(part) for part in iter_s]
    return iterating_parser
