"""Day 2: Dive!"""

from dataclasses import dataclass
from enum import Enum

from utils import read


class Direction(Enum):
    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


@dataclass
class Instruction:
    dir: Direction
    val: int

    @classmethod
    def from_data_line(cls, line):
        inst, val = line.split(' ')
        return cls(Direction(inst), int(val))


@dataclass
class Submarine:
    horiz: int = 0
    depth: int = 0
    aim: int = 0

    def __iter__(self):
        yield from [self.horiz, self.depth]

    def naive_move(self, inst):
        """Move the submarine without accounting for aiming."""
        match inst.dir:
            case Direction.FORWARD:
                self.horiz += inst.val
            # for "up" and "down", submarine depth is inverted/negated
            case Direction.UP:
                self.depth -= inst.val
            case Direction.DOWN:
                self.depth += inst.val

    def move(self, inst):
        """Move the submarine."""
        match inst.dir:
            case Direction.FORWARD:
                self.horiz += inst.val
                self.depth += self.aim * inst.val
            # for "up" and "down", submarine depth is inverted/negated
            case Direction.UP:
                self.aim -= inst.val
            case Direction.DOWN:
                self.aim += inst.val


if __name__ == "__main__":
    instructions = read.dayta(day=2, line_parser=Instruction.from_data_line)

    sub_one, sub_two = Submarine(), Submarine()
    for instruct in instructions:
        sub_one.naive_move(instruct)
        sub_two.move(instruct)

    print(f"Part One: {sub_one.horiz * sub_one.depth}")
    print(f"Part Two: {sub_two.horiz * sub_two.depth}")
