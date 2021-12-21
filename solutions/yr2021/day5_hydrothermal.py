"""(2021) Day 5: Hydrothermal Venture"""

from __future__ import annotations

# noinspection PyPep8Naming
from collections import defaultdict as DefaultDict
from dataclasses import dataclass
from typing import Sequence

from utils import read


@dataclass(frozen=True)
class DiscretePoint:
    """Discrete/integer-valued point."""
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"


class DiscreteLineSegment:
    """Line segment defined by integer points, restricted to a slope of +1, -1, 0, or undefined.

    For these line segments, on the domain of integer-valued x-coordinates,
    all the y-coordinates must also be integer-valued.

    Attributes:
        x_range: Range of x-coordinates from lowest to highest value.
        y_range: Range of y-coordinates that map to the range of x-coordinates.
    """
    x_range: Sequence[int]
    y_range: Sequence[int]

    def __init__(self, pt1: DiscretePoint, pt2: DiscretePoint):
        """Initialize a line segment from two points."""
        slope = (pt2.y - pt1.y) / (pt2.x - pt1.x) if pt2.x != pt1.x else None
        if slope not in {1.0, -1.0, 0, None}:
            raise ValueError(f"line segment should be +1, -1, 0, or undefined: {slope}")
        low_pt, high_pt = (pt1, pt2) if pt1.x <= pt2.x else (pt2, pt1)
        self.x_range = range(low_pt.x, high_pt.x + 1)
        y_step = +1 if low_pt.y <= high_pt.y else -1
        self.y_range = range(low_pt.y, high_pt.y + y_step, y_step)
        # enforce invariant
        assert any((
            len(self.x_range) == len(self.y_range),
            len(self.x_range) == 1,
            len(self.y_range) == 1,
        )), f"{list(self.x_range)}, {list(self.y_range)}"

    @classmethod
    def from_puzzle_line(cls, line: str):
        """Initialize a line segment from a line from the puzzle."""
        coords = [int(num) for pt_str in line.split(" -> ") for num in pt_str.split(',')]
        return cls(DiscretePoint(coords[0], coords[1]), DiscretePoint(coords[2], coords[3]))

    def is_horizontal(self):
        return len(self.y_range) == 1

    def is_vertical(self):
        return len(self.x_range) == 1

    def integer_pts(self):
        """Iterate over the points of the line segment that have integer values."""
        if self.is_horizontal():
            return (DiscretePoint(x, self.y_range[0]) for x in self.x_range)
        elif self.is_vertical():
            return (DiscretePoint(self.x_range[0], y) for y in self.y_range)
        else:
            return (DiscretePoint(x, y) for x, y in zip(self.x_range, self.y_range))


def num_discrete_overlaps(line_segments):
    """Count the number of discrete points covered by two or more line segments.

    From an iterable of line segments, return the number of discrete/integer-valued
    points that are contained in more than one of the line segments.
    """
    point_ct = DefaultDict(int)
    num_overlaps = 0
    for line_segment in line_segments:
        for pt in line_segment.integer_pts():
            point_ct[pt] += 1
            if point_ct[pt] == 2:  # only count when the first overlap occurs.
                num_overlaps += 1
    return num_overlaps


if __name__ == "__main__":
    segments = read.dayta(day=5, line_parser=DiscreteLineSegment.from_puzzle_line)
    horiz_vert_segments = [seg for seg in segments if seg.is_horizontal() or seg.is_vertical()]
    print(f"Part One: {num_discrete_overlaps(horiz_vert_segments)}")
    print(f"Part Two: {num_discrete_overlaps(segments)}")
