"""(2021) Day 11: Dumbo Octopus"""

import numpy as np

from utils import arr, read


def _increment_energy(energy_array, index, flashed_stack):
    """Increase an octopus's energy, appending to the stack if necessary and returning if it flashed."""
    energy_array[index] += 1
    if energy_array[index] == 10:
        energy_array[index] = 0
        flashed_stack.extend(arr.adjacent(index, energy_array.shape))
        return True
    return False


def octopus_flashes(energy_array):
    """Simulate octopus energy growths in-place and return flashes (for a single time step).

    Octopus energy growth is incremental from energy 0-9.
    If an octopus has energy 9, the next energy increment causes its energy to return to 0,
    and triggers a flash, incrementing the energy of all adjacent octopuses.

    In a given time step, once an octopus has flashed, it cannot gain any more energy.
    In other words, if an octopus is at energy 0, it cannot gain any energy unless this
    is its first energy increment of the time step (contrapositively, if this gain is not
    the octopus's first increment, and the octopus is at energy level 0,
    then it must have flashed in this time step).

    Because every octopus gains 1 energy at the beginning of the time step,
    if an octopus is at energy 0 at *any* point during the time step after the first gain,
    it must have flashed during this time step, and then must stay at energy level 0.
    As an implementation detail, this means I can separate flashes into two categories (per time step).

    1. The initial increment, when all octopuses gain 1 energy.
    2. The flashed increments, when only adjacent octopuses that have >0 energy gain energy.
    """
    num_flashes = 0
    flashed_stack = []

    # Increment all octopuses by 1 and initialize the first flash-triggered increments.
    for index in np.ndindex(energy_array.shape):
        num_flashes += _increment_energy(energy_array, index, flashed_stack)

    # Increment octopuses that have not already flashed from the triggers.
    while len(flashed_stack) > 0:
        if energy_array[index := flashed_stack.pop()] > 0:
            num_flashes += _increment_energy(energy_array, index, flashed_stack)

    return num_flashes


if __name__ == "__main__":
    init_octopuses = np.array(read.dayta(day=11, line_parser=read.iter_parser(int)))

    octopuses = init_octopuses.copy()
    total_flashes = sum(octopus_flashes(octopuses) for _ in range(100))
    print(f"Part One: {total_flashes}")

    octopuses = init_octopuses.copy()
    step_counter = 1  # at least one flash step happens every time
    while octopus_flashes(octopuses) != len(octopuses):
        step_counter += 1
    print(f"Part Two: {step_counter}")
