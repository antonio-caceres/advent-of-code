"""Utility functions for points and lines on a two-dimensional plot."""

import functools
import math
import numbers
from dataclasses import dataclass
from enum import Enum
from typing import Sequence


@dataclass(frozen=True)
class DiscretePoint:
    """Two-dimensional point that is integer-valued in both dimensions."""
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        if isinstance(other, DiscretePoint):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self == DiscretePoint(*other)
        else:
            return NotImplemented

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"


def sort_points(pts, by_y_coord=False, reverse=False):
    """Sort an iterable of discrete points. By default, from smallest to largest by x-coordinate first.

    This function returns `DiscretePoint` objects that are not the same objects as the
    original points passed in.
    This is an implementation detail since the `DiscretePoint` class is an immutable dataclass.

    Args:
        pts: Points to sort.
        by_y_coord: If the points should be sorted first by y-coordinate.
            If ``False``, sorts first by x-coordinate.
        reverse: If the points should be sorted from greatest to smallest.

    Returns:
        Sorted list of discrete points.
    """
    coord_pairs = [(x, y) if not by_y_coord else (y, x) for x, y in pts]
    sorted_pairs = sorted(coord_pairs, reverse=reverse)
    return [DiscretePoint(x, y) if not by_y_coord else DiscretePoint(y, x) for x, y in sorted_pairs]


@functools.total_ordering
class DiscreteSlope(Enum):
    """Possible slope values for the `DiscreteLine` class.

    For 2D lines with 0, -1, +1, or undefined/infinite slopes, if one of the points
    on the line is integer-valued in both dimensions, then all the points on the line
    that are integer-valued in one dimensions are integer-valued in the other.
    """
    ZERO = 0.0
    POSITIVE = +1.0
    NEGATIVE = -1.0
    INFINITE = math.inf

    def __float__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, (DiscreteSlope, numbers.Real)):
            return float(self) == float(other)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (DiscreteSlope, numbers.Real)):
            return float(self) < float(other)
        else:
            return NotImplemented


class DiscreteLine:
    """Line segment defined by integer points, restricted to a slope of +1, -1, 0, or infinite/undefined."""

    def __init__(self,
                 pt: DiscretePoint | tuple[int, int],
                 slope: DiscreteSlope | int | float | None):
        """Initialize a discrete line from a point and slope.

        Args:
            pt: Discrete point on the line.
            slope: Slope of the line. If ``None``, is considered to be infinite/undefined.
                Must be able to be converted into a `DiscreteSlope` if not ``None``.
        """
        self.pt = pt if isinstance(pt, DiscretePoint) else DiscretePoint(*pt)
        self.slope = DiscreteSlope.INFINITE if slope is None else DiscreteSlope(slope)

    @classmethod
    def horizontal_line(cls, y):
        return cls((0, y), 0)

    @classmethod
    def vertical_line(cls, x):
        return cls((x, 0), DiscreteSlope.INFINITE)

    def is_horizontal(self):
        return self.slope == 0

    def is_vertical(self):
        return self.slope == math.inf


class DiscreteLineSegment(DiscreteLine):
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
        super().__init__(pt1, slope)

        low_pt, high_pt = (pt1, pt2) if pt1.x <= pt2.x else (pt2, pt1)
        self.x_range = range(low_pt.x, high_pt.x + 1)
        # y_step is simply a parameter to the range call to capture all of y_range in order.
        # In the case low_py.y == high.pt_y, y_step should still be non-zero to ensure
        # y_range is not an empty generator (either +1 or -1 would work in this case).
        y_step = +1 if low_pt.y <= high_pt.y else -1
        self.y_range = range(low_pt.y, high_pt.y + y_step, y_step)

    def discrete_pts(self):
        """Iterate over the points of the line segment that have integer values."""
        if self.is_horizontal():
            return (DiscretePoint(x, self.y_range[0]) for x in self.x_range)
        elif self.is_vertical():
            return (DiscretePoint(self.x_range[0], y) for y in self.y_range)
        else:
            return (DiscretePoint(x, y) for x, y in zip(self.x_range, self.y_range))
