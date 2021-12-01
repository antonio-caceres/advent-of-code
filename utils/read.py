
RELATIVE_INPUT_FILE = "data/day{}.txt"


def puzzle_input(day):
    """Location of the puzzle input file for `day`, relative to the year directory."""
    return RELATIVE_INPUT_FILE.format(day)


def read_ints(file_name):
    """Read integers from a file, with one integer per line."""
    with open(file_name) as f:
        return [int(line) for line in f.readlines()]
