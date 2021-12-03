"""For reading Advent of Code's puzzle input files into data structures."""


def parse_lines(file_name, parser=str):
    """Read integers from a file, with one integer per line."""
    with open(file_name) as f:
        return [parser(line) for line in f.readlines()]
