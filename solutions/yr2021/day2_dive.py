"""Day 2: Dive!"""

from dataclasses import dataclass
from enum import Enum

import utils


@dataclass
class Position:
    horiz: int = 0
    depth: int = 0
    aim: int | None = 0

    def __iter__(self):
        yield from [self.horiz, self.depth]


class Directions(Enum):
    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


def _parse_instructions(lines):
    instructs = []
    for line in lines:
        instruct, val = line.split()
        instructs.append((Directions(instruct), int(val)))
    return instructs


def calc_position(instructs):
    pos = Position(aim=None)
    for direction, val in instructs:
        match direction:
            case Directions.FORWARD:
                pos.horiz += val
            # for "up" and "down", submarine depth is inverted/negated
            case Directions.UP:
                pos.depth -= val
            case Directions.DOWN:
                pos.depth += val
    return pos


def calc_aimed_position(instructs):
    pos = Position()
    for direction, val in instructs:
        match direction:
            case Directions.FORWARD:
                pos.horiz += val
                pos.depth += pos.aim * val
            # for "up" and "down", submarine aim is inverted/negated
            case Directions.UP:
                pos.aim -= val
            case Directions.DOWN:
                pos.aim += val
    return pos


if __name__ == "__main__":
    with open(utils.data_file(day=2)) as f:
        dive_instructs = _parse_instructions(f.readlines())

    for part, func in [("1", calc_position), ("2", calc_aimed_position)]:
        horiz, depth = func(dive_instructs)
        print(f"Part {part}: {horiz * depth}")
