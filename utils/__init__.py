
from .read import parse_lines
from .data import data_file


def parse_dayta(day, line_parser=str):
    """Parses the lines from a data file for a given day."""
    return parse_lines(data_file(day), line_parser)
