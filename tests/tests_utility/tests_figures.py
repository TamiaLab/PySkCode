"""
SkCode figures utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    FigureDeclarationTreeNode,
    TextTreeNode
)
from skcode.utility.figures import extract_figures


class CustomFigureDeclarationTreeNode(FigureDeclarationTreeNode):
    """
    Custom ``FigureDeclarationTreeNode`` subclass for tests.
    """
    pass


class FiguresUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the figures utility module. """

    def test_extract_figures(self):
        """ Test the ``extract_figures`` utility. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('figure', FigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a2 = document_tree.new_child('figure', FigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('figure', FigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a4 = document_tree.new_child('figure', FigureDeclarationTreeNode)
        figures = extract_figures(document_tree)
        self.assertEqual([a1, a2, a3, a4], figures)

    def test_extract_figures_no_figures(self):
        """ Test the ``extract_figures`` utility with no figure. """
        document_tree = RootTreeNode()
        figures = extract_figures(document_tree)
        self.assertEqual([], figures)

    def test_extract_figures_custom_class(self):
        """ Test the ``extract_figures`` utility with a custom figure options class. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('figure', CustomFigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('figure', FigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('figure', CustomFigureDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('figure', FigureDeclarationTreeNode)
        figures = extract_figures(document_tree, figure_node_cls=CustomFigureDeclarationTreeNode)
        self.assertEqual([a1, a3], figures)
