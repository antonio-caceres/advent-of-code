"""Array utility functions."""


def adjacent(index, shape):
    """Iterate over the valid adjacent indices of ``index``, within the array shape.

    Does not check that index is a valid index for shape.
    """
    for dim, dim_size in enumerate(shape):
        if index[dim] > 0:
            yield *index[:dim], index[dim] - 1, *index[dim+1:]
        if index[dim] < dim_size - 1:
            yield *index[:dim], index[dim] + 1, *index[dim+1:]


def is_local_min(array, index):
    """If the index is a local minimum of the array ``array``.

    Considers the (``dim * 2``) adjacent indices, where ``dim`` is the dimension of ``array``.
    """
    return all((array[index] < array[adj_idx] for adj_idx in adjacent(index, array.shape)))


