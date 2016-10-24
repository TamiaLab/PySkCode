"""
SkCode acronyms utility code.
"""

from ..tags.acronyms import AcronymTreeNode


def extract_acronyms(document_tree,
                     acronym_node_cls=AcronymTreeNode):
    """
    Extract all acronyms present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param acronym_node_cls: The tree node class used for acronym declarations.
    :return: A list of all acronyms node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    return list([tree_node for tree_node in document_tree.search_in_tree(acronym_node_cls)])
