"""Array utility functions."""

from enum import Enum
from typing import Iterable
import itertools

from numpy.typing import NDArray


def adjacent(index: tuple[int],
             shape: tuple[int],
             max_deltas: int | None = None,
             include_index: bool = False) -> Iterable[tuple[int]]:
    """Iterate over valid adjacent indices of ``index``, within the given array shape.

    Does not check if the given index is invalid for the array shape.
    This is because indices just outside the shape could still yield useful results.

    Adjacent indices are indices that are different by exactly 1 from ``index``
    in 1 or more dimensions (0 or more dimensions if ``include_index`` is ``True``).

    Args:
        index: Tuple of integers that index each dimension of the array.
        shape: Tuple with the length of each dimension of the array.
        max_deltas: Constrains which indices are considered adjacent.
            Represents the maximum number of dimensions in which the adjacent index can be
            different from ``index`` and still be considered adjacent.
            If ``None``, ``max_deltas`` is set to the length of ``shape``,
            i.e., the number of dimensions of the target array.
            If ``max_deltas`` is ``len(shape) - n``, then an adjacent index must
            be the same in at least ``n`` dimensions to be considered adjacent.
            E.g., if ``max_deltas`` is 1, only directly adjacent indices are considered
            adjacent (no diagonal indices are considered).
        include_index: If ``index`` should be considered adjacent to itself.

    Returns:
        Iterator over all the adjacent indices of ``index`` within ``shape``.
    """
    if len(index) != len(shape):
        raise ValueError(f"index and array shape have different dimensions: "
                         f"{len(index)} != {len(shape)}")
    if max_deltas is None:
        max_deltas = len(shape)

    for deltas in itertools.product([-1, 0, 1], repeat=len(shape)):
        num_diff_dims = len(shape) - deltas.count(0)

        if (num_diff_dims == 0 and not include_index) or (num_diff_dims > max_deltas):
            # not considered as an adjacent index
            continue

        adj_coords = tuple(coord + delta for coord, delta in zip(index, deltas))
        if all(0 <= coord < dim_shape for coord, dim_shape in zip(adj_coords, shape)):
            # the adjacent coordinates are valid
            yield adj_coords


class _Comparisons(Enum):
    LT = "<"
    LT_EQ = "<="
    GT = ">"
    GT_EQ = ">="

    def compare(self, a, b):
        match self:
            case self.LT:
                return a < b
            case self.LT_EQ:
                return a <= b
            case self.GT:
                return a > b
            case self.GT_EQ:
                return a >= b


def _adj_comparison(array: NDArray,
                    index: tuple[int],
                    comparison: _Comparisons,
                    max_deltas: int | None = None):
    """Perform a comparison between a value in an array and its adjacent values."""
    adj_indices = adjacent(index, array.shape, max_deltas)
    return all(comparison.compare(array[index], array[adj]) for adj in adj_indices)


def is_local_min(array: NDArray,
                 index: tuple[int],
                 equality: bool = False,
                 max_deltas: int | None = None):
    """If ``index`` is a local minimum (> adjacent indices, or >= if ``equality) of ``array``."""
    comparison = _Comparisons.LT_EQ if equality else _Comparisons.LT
    return _adj_comparison(array, index, comparison, max_deltas)


def is_local_max(array: NDArray,
                 index: tuple[int],
                 equality: bool = False,
                 max_deltas: int | None = None):
    """If ``index`` is a local maximum (> adjacent indices, or >= if ``equality) of ``array``."""
    comparison = _Comparisons.GT_EQ if equality else _Comparisons.GT
    return _adj_comparison(array, index, comparison, max_deltas)
