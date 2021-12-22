"""Graph utility functions."""


class GraphDict(dict):
    """Graph represented by a dictionary.

    The top-level dictionary (this class) has a key for each node in the graph.
    The values are some data structure used to represent edges and (optionally) weights;
    by default, this data structure is a dictionary mapping other nodes to the edge weight.

    When using this class, changing the `edge_factory` function or
    modifying the dictionary values directly will likely cause undefined behavior.
    Please read the source code before choosing to do this.

    The `edge_factory` function exists (and is mutable) because it can provide a
    useful alternative to modifying the dictionary values directly (which should almost
    always be avoided).

    Modifying the dictionary is an option because dictionaries are mutable, so
    providing a read-only dictionary access would require essentially a wrapper
    around the entire dictionary interface except a couple of methods, and even then,
    the underlying dictionary would still be mutable with some effort (such is Python).

    In addition, sometimes modifying the dictionary can be useful (especially for
    a set of faster initializations, such as additions of many isolated nodes).
    """

    def __init__(self, *args, edge_factory=dict, **kwargs):
        """Initialize a graph edge dictionary.

        Args:
            *args: Positional arguments passed to the `dict` constructor.

        Keyword Args:
            edge_factory: Factory function that creates the values for new node keys.
                In general, `edge_factory` should be left as its default value, ``dict``.
                See class documentation for more information.
            **kwargs: Keyword arguments passed to the `dict` constructor.
        """
        super().__init__(*args, **kwargs)
        self.edge_factory = edge_factory

    def add_node(self, node):
        """Add a node to the graph (do nothing if the node already exists).

        Args:
            node: Hashable object that acts as a node or node identifier.
        """
        if node not in self:
            self[node] = self.edge_factory()

    def remove_node(self, node):
        """Remove a node from the graph."""
        if node in self:
            del self[node]
            for edge_dict in self.values():
                if node in edge_dict:
                    del edge_dict[node]

    def add_edge(self, source, dest, weight=True, bidirectional=False):
        """Add an edge to the graph.

        This function will override existing edges in the graph.

        Args:
            source: Hashable node identifier, source of the edge.
            dest: Hashable node identifier, destination of the edge.
            weight: Weight of the edge, by default ``True``.
            bidirectional: If the edge in the reverse direction should be added as well.
        """
        self.add_node(source)
        self.add_node(dest)
        self[source][dest] = weight
        if bidirectional:
            self[dest][source] = weight

    def remove_edge(self, source, dest, bidirectional=False):
        """Remove an edge from the graph."""
        if source in self and dest in self[source]:
            del self[source][dest]
        if bidirectional:
            self.remove_edge(dest, source)
