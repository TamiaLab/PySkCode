"""
SkCode figures utility code.
"""

from ..tags.figures import FigureDeclarationTreeNode


def extract_figures(document_tree,
                    figure_node_cls=FigureDeclarationTreeNode):
    """
    Extract all figures present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param figure_node_cls: The tree node class used for figure declarations.
    :return: A list of all figures node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    return list([tree_node for tree_node in document_tree.search_in_tree(figure_node_cls)])
