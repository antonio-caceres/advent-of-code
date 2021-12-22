"""Array utility functions."""

import itertools
from enum import Enum
from typing import Iterable

from numpy.typing import NDArray


def adjacent(index: tuple[int],
             shape: tuple[int],
             max_deltas: int | None = None,
             include_index: bool = False) -> Iterable[tuple[int]]:
    """Iterate over valid adjacent indices of `index`, within the given array shape.

    Does not fail if `index` is an invalid index of `shape`.
    This is because indices just outside the array shape could still yield useful results.

    Adjacent indices are indices that are different by exactly 1 from `index` in 1 or more dimensions
    (0 or more dimensions if `include_index` is ``True``).

    Args:
        index (tuple[int]): Index of an array, where each integer indexes each array dimension.
        shape (tuple[int]): Dimensions of the target array.
        max_deltas (int | None): Maximum number of dimensions in which an adjacent index can differ from `index`.
            If ``None``, `max_deltas` is set to the length of `shape`.
            If 1, for example, only directly adjacent indices,
            and no diagonal indices, are considered
            If ``len(shape) - n``, then an adjacent index must be the same  as `index` in
            at least ``n`` dimensions to be considered adjacent.
        include_index (bool): If ``index`` should be considered adjacent to itself.

    Yields:
        Index of an array with the given shape that is adjacent to ``index``.

    Raises:
        ValueError: If ``index`` is not the same length as ``shape``.
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
    """Enum class representing the six Python value comparison operators."""

    EQ = "=="
    NOT_EQ = "!="
    LT = "<"
    LT_EQ = "<="
    GT = ">"
    GT_EQ = ">="

    def compare(self, a, b):
        """Compare two values using the comparison represented by an instance of this class."""
        # could be replaced with a call to eval, but that hurts readability
        match self:
            case self.EQ:
                return a == b
            case self.NOT_EQ:
                return a != b
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
    """If `index` is a local minimum (< adjacent indices, or <= if `equality`) of `array`."""
    comparison = _Comparisons.LT_EQ if equality else _Comparisons.LT
    return _adj_comparison(array, index, comparison, max_deltas)


def is_local_max(array: NDArray,
                 index: tuple[int],
                 equality: bool = False,
                 max_deltas: int | None = None):
    """If `index` is a local maximum (> adjacent indices, or >= if `equality`) of `array`."""
    comparison = _Comparisons.GT_EQ if equality else _Comparisons.GT
    return _adj_comparison(array, index, comparison, max_deltas)
