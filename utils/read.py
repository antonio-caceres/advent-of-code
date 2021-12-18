"""For reading Advent of Code's puzzle input files into data structures."""

from utils.data import data_file


def lines(file_name, parser=str):
    """Parse the lines from a file with a function.

    Strips new lines from the end.
    """
    with open(file_name) as f:
        # remove '\n' from lines using splitlines
        return [parser(line) for line in f.read().splitlines(keepends=False)]


def dayta(day, line_parser=str):
    """Parses the lines from a data file for a given day."""
    return lines(data_file(day), line_parser)


def iter_parser(parser=str, sep=None):
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
