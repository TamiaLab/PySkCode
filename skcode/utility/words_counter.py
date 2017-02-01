"""
SkCode words counter utility code.
"""

from ..tags.internal import TextTreeNode


def count_words(document_tree,
                text_node_cls=TextTreeNode):
    """
    Count all words present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param text_node_cls: The tree node class used for text.
    :return: The number of words in the document.
    """
    assert document_tree, "Document tree is mandatory."
    words_count = 0
    for tree_node in document_tree.search_in_tree(text_node_cls):
        words_count += len(tree_node.content.split())
    return words_count
