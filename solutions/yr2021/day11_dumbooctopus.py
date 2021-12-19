"""(2021) Day 11: Dumbo Octopus"""

import numpy as np

from utils import arr, read


def _increment_energy(energy_array, index, flashed_stack):
    """Increase an octopus's energy, appending to the stack if necessary and returning if it flashed."""
    energy_array[index] += 1
    if energy_array[index] == 10:
        energy_array[index] = 0
        flashed_stack.extend(arr.adjacent(index, energy_array.shape))


def octopus_flashes(energy_array):
    """Simulate octopus energy growths and flashes in-place (for a single time step).

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
    # After the initial universal +1 energy increase, every flash is equivalent.
    # (+1 if the octopus is at >0 energy, +0 if the octopus is at 0 energy).
    flashed_stack = []

    # Increment all octopuses by 1 and initialize the first flash-triggered increments.
    for index in np.ndindex(energy_array.shape):
        _increment_energy(energy_array, index, flashed_stack)

    # Increment octopuses that have not already flashed from the triggers.
    while len(flashed_stack) > 0:
        if energy_array[index := flashed_stack.pop()] > 0:
            _increment_energy(energy_array, index, flashed_stack)


def total_flashes(energy_array, time_steps=1):
    """Get the total number of octopus flashes after a number of time steps.

    Modifies ``energy_array`` in-place.
    """
    flashes = 0

    for _ in range(time_steps):
        octopus_flashes(energy_array)
        # counts the number of energies in the array where the value is == 0
        flashes += np.count_nonzero(energy_array == 0)

    return flashes


def first_complete_flash(energy_array):
    """Get the first step where ``energy_array`` completely flashes (i.e. is all zeros after the step).

    Modifies ``energy_array`` in-place.

    If ``energy_array`` is initially all zeros, return 0.
    """
    step_counter = 0

    while np.any(energy_array != 0):
        step_counter += 1
        octopus_flashes(energy_array)

    return step_counter


if __name__ == "__main__":
    octopuses = np.array(read.dayta(day=11, line_parser=read.iter_parser(int)))
    n_flashes = total_flashes(octopuses.copy(), time_steps=100)
    print(f"Part One: {n_flashes}")
    first_step = first_complete_flash(octopuses.copy())
    print(f"Part Two: {first_step}")
