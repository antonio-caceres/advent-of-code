
from .read import parse_lines
from .data import data_file


def parse_lines_for_day(day, parser=str):
    return parse_lines(data_file(day), parser)
