"""(2021) Day 12: Passage Pathing"""

from utils import read, graph

STARTING_NODE = "start"
ENDING_NODE = "end"


def _cave_visitor(cave_graph, cur_path, all_paths, extra_time):
    """Recursive helper functions for traversing the cave graph to the ending node."""
    for next_node in cave_graph[cur_path[-1]]:
        if next_node == ENDING_NODE:
            all_paths.append(cur_path + [next_node])
        if next_node == ENDING_NODE or next_node == STARTING_NODE:
            continue

        # to visit, cave must have not been visited or cave must not be small
        if next_node not in cur_path or not next_node.islower():
            _cave_visitor(cave_graph, cur_path + [next_node], all_paths, extra_time)
        elif extra_time:  # use the one time
            _cave_visitor(cave_graph, cur_path + [next_node], all_paths, extra_time=False)


def all_cave_paths(cave_graph, extra_time=False):
    """Find all paths in the graph from "start" to "end" that visit small caves at most once.

    Large caves have uppercase string identifiers, and small caves have lowercase string identifiers.
    Caves with identifiers that are not uppercase or lowercase are treated without restrictions.

    If `extra_time` is ``True``, then one small cave that is not "start" or "end" can be visited twice.
    """
    cave_paths = []
    _cave_visitor(cave_graph, [STARTING_NODE], cave_paths, extra_time)
    return cave_paths


if __name__ == "__main__":
    caves = graph.GraphDict()
    read.dayta(day=12, line_parser=lambda line: caves.add_edge(*line.split("-"), bidirectional=True))
    print(f"Part One: {len(all_cave_paths(caves))}")
    print(f"Part Two: {len(all_cave_paths(caves, extra_time=True))}")
