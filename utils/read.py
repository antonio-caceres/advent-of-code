"""For reading Advent of Code's puzzle input files into data structures."""

from utils.data import data_file


def lines(file_name, parser=str):
    """Parse the lines from a file with a function.

    Strips new lines from the end."""
    with open(file_name) as f:
        # remove new lines using splitlines
        return [parser(line) for line in f.read().splitlines(keepends=False)]


def dayta(day, line_parser=str):
    """Parses the lines from a data file for a given day."""
    return lines(data_file(day), line_parser)
