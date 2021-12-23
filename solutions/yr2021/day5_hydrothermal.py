"""(2021) Day 5: Hydrothermal Venture"""

from __future__ import annotations

# noinspection PyPep8Naming
from collections import defaultdict as DefaultDict

from utils import read, plot


def line_segment_parser(line: str):
    """Initialize a line segment from a line from the puzzle."""
    coords = [int(num) for pt_str in line.split(" -> ") for num in pt_str.split(',')]
    return plot.DiscreteLineSegment(plot.DiscretePoint(coords[0], coords[1]),
                                    plot.DiscretePoint(coords[2], coords[3]))


def num_discrete_overlaps(line_segments):
    """Count the number of discrete points covered by two or more line segments.

    From an iterable of line segments, return the number of discrete/integer-valued
    points that are contained in more than one of the line segments.
    """
    point_ct = DefaultDict(int)
    num_overlaps = 0
    for line_segment in line_segments:
        for pt in line_segment.discrete_pts():
            point_ct[pt] += 1
            if point_ct[pt] == 2:  # only count when the first overlap occurs.
                num_overlaps += 1
    return num_overlaps


if __name__ == "__main__":
    segments = read.dayta(day=5, line_parser=line_segment_parser)
    horiz_vert_segments = [seg for seg in segments if seg.is_horizontal() or seg.is_vertical()]
    print(f"Part One: {num_discrete_overlaps(horiz_vert_segments)}")
    print(f"Part Two: {num_discrete_overlaps(segments)}")
