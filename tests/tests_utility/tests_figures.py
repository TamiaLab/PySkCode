"""
SkCode figures utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         FigureDeclarationTagOptions,
                         TextTagOptions)
from skcode.utility import extract_figures


class CustomFigureDeclarationTagOptions(FigureDeclarationTagOptions):
    """
    Custom ``FigureDeclarationTagOptions`` subclass for tests.
    """
    pass


class FiguresUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the figures utility module. """

    def test_extract_figures(self):
        """ Test the ``extract_figures`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('figure', FigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a2 = document_tree.new_child('figure', FigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('figure', FigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a4 = document_tree.new_child('figure', FigureDeclarationTagOptions())
        figures = extract_figures(document_tree)
        self.assertEqual([a1, a2, a3, a4], figures)

    def test_extract_figures_no_figures(self):
        """ Test the ``extract_figures`` utility with no figure. """
        document_tree = RootTreeNode(RootTagOptions())
        figures = extract_figures(document_tree)
        self.assertEqual([], figures)

    def test_extract_figures_custom_class(self):
        """ Test the ``extract_figures`` utility with a custom figure options class. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('figure', CustomFigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('figure', FigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('figure', CustomFigureDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('figure', FigureDeclarationTagOptions())
        figures = extract_figures(document_tree, figure_ops_cls=CustomFigureDeclarationTagOptions)
        self.assertEqual([a1, a3], figures)
