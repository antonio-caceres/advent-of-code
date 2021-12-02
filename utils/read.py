"""For reading Advent of Code's puzzle input files into data structures."""


def int_lines(file_name):
    """Read integers from a file, with one integer per line."""
    with open(file_name) as f:
        return [int(line) for line in f.readlines()]
