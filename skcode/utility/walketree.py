"""
SkCode utility for walking across a document tree.
"""


def walk_tree_for_cls(tree_node, opts_cls):
    """
    Walk the tree and yield any tree node matching the given options class.
    :param tree_node: The current tree node instance.
    :param opts_cls: The options class to search for.
    """

    # Check the current tree node first
    if isinstance(tree_node.opts, opts_cls):
        yield tree_node

    # Check all children nodes
    for child in tree_node.children:
        for node in walk_tree_for_cls(child, opts_cls):
            yield node
