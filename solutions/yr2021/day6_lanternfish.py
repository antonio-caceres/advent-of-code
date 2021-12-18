"""(2021) Day 6: Lanternfish"""

from collections import deque, Counter

from utils import read


class LanternfishSim:
    """A population simulation of immortal, asexually reproducing lanternfish.

    In this context, their "cycle" is the number of time iterations until the fish reproduces.
    Each fish produces a new fish on the time step when their "cycle" is equal to 0
    (i.e. two time steps from cycle 1 to reproduction, one to decrease to 0, and one to reproduce),
    and this does not depend on the state of the rest of the fish in the population.

    For additional information, see attribute getter documentation.
    """
    _adult_fish: deque[int]
    _baby_fish: deque[int]
    _birth_cycle: int
    _growth_cycle: int

    def __init__(self, cycle_dist: list[int], birth_cycle: int, growth_cycle: int):
        """Initialize a lanternfish simulation.

        Args:
            cycle_dist: initial distribution of the fish by their cycle
                baby fish should have cycle times of ``birth_cycle`` plus the number of cycles until adulthood
                fish with cycle times greater than ``birth_cycle + growth_cycle`` are ignored
            birth_cycle: number of time steps an adult fish takes to reproduce
            growth_cycle: number of time steps a baby fish takes to become an adult
                i.e. after being born, a fish takes ``birth_cycle + growth_cycle`` time steps to reproduction
        """
        self._birth_cycle, self._growth_cycle = birth_cycle, growth_cycle
        self._adult_fish = deque(cycle_dist[:birth_cycle], maxlen=birth_cycle)
        self._baby_fish = deque(cycle_dist[birth_cycle:birth_cycle + growth_cycle], maxlen=growth_cycle)

    @classmethod
    def from_fish_cycles(cls, fish_cycles: list[int], birth_cycle: int, growth_cycle: int):
        """Initialize a lanternfish population from a list of the fish cycles."""
        cycle_counts = Counter(fish_cycles)
        cycle_dist = [cycle_counts[i] for i in range(birth_cycle + growth_cycle)]
        return cls(cycle_dist, birth_cycle, growth_cycle)

    @property
    def birth_cycle(self):
        """Number of time steps for an adult fish to reproduce."""
        return self._birth_cycle

    @property
    def growth_cycle(self):
        """Number of time steps for a newly born fish to become an adult."""
        return self._growth_cycle

    @property
    def num_fish(self):
        """Total number of fish in the lanternfish population."""
        return sum(self._adult_fish) + sum(self._baby_fish)

    @property
    def fish_cycle_dist(self):
        """Distribution of fish by the number of cycles until they birth, as a list.

        A "cycle" of 0 indicates the fish will birth during the next time step.
        """
        return list(self._adult_fish) + list(self._baby_fish)

    def simulate(self, time_steps: int = 1):
        """Simulate the growth of the population for a number of time steps."""
        for _ in range(time_steps):
            parent_fish = self._adult_fish.popleft()
            new_adults = self._baby_fish.popleft()
            self._adult_fish.append(parent_fish + new_adults)
            self._baby_fish.append(parent_fish)


if __name__ == "__main__":
    parsed_lines = read.dayta(day=6, line_parser=lambda line: [int(x) for x in line.split(",")])
    for init_lanternfish in parsed_lines:
        simulation = LanternfishSim.from_fish_cycles(init_lanternfish, birth_cycle=7, growth_cycle=2)
        time_steps_a = 80
        simulation.simulate(time_steps=time_steps_a)
        print(f"Part One: {simulation.num_fish}")
        time_steps_b = 256
        simulation.simulate(time_steps=time_steps_b-time_steps_a)
        print(f"Part Two: {simulation.num_fish}")

