"""
SkCode figures utility code.
"""

from .walketree import walk_tree_for_cls
from ..tags.figures import FigureDeclarationTagOptions


def extract_figures(document_tree,
                    figure_ops_cls=FigureDeclarationTagOptions):
    """
    Extract all figures present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param figure_ops_cls: The options class used for figure declarations.
    :return: A list of all figures node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    # TODO Replace *_cls with the new categories based system

    # List of figures found
    figures = []

    # For each figure declaration
    for tree_node in walk_tree_for_cls(document_tree, figure_ops_cls):

        # Store the figure
        figures.append(tree_node)

    # Return the list
    return figures
