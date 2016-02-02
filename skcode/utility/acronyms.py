"""
SkCode acronyms utility code.
"""

from .walketree import walk_tree_for_cls
from ..tags.acronyms import AcronymTagOptions


def extract_acronyms(document_tree,
                     acronym_ops_cls=AcronymTagOptions):
    """
    Extract all acronyms present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param acronym_ops_cls: The options class used for acronym declarations.
    :return: A list of all acronyms node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    # TODO Replace *_cls with the new categories based system

    # List of acronyms found
    acronyms = []

    # For each acronym declaration
    for tree_node in walk_tree_for_cls(document_tree, acronym_ops_cls):

        # Store the acronym entry
        acronyms.append(tree_node)

    # Return the list
    return acronyms
