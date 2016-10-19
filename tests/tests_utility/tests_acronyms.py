"""
SkCode acronyms utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    AcronymTreeNode,
    TextTreeNode
)
from skcode.utility.acronyms import extract_acronyms


class CustomAcronymTreeNode(AcronymTreeNode):
    """
    Custom ``AcronymTreeNode`` subclass for tests.
    """
    pass


class AcronymsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the acronyms utility module. """

    def test_extract_acronyms(self):
        """ Test the ``extract_acronyms`` utility. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('acronym', AcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a2 = document_tree.new_child('acronym', AcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('acronym', AcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a4 = document_tree.new_child('acronym', AcronymTreeNode)
        acronyms = extract_acronyms(document_tree)
        self.assertEqual([a1, a2, a3, a4], acronyms)

    def test_extract_acronyms_no_acronyms(self):
        """ Test the ``extract_acronyms`` utility with no acronym. """
        document_tree = RootTreeNode()
        acronyms = extract_acronyms(document_tree)
        self.assertEqual([], acronyms)

    def test_extract_acronyms_custom_class(self):
        """ Test the ``extract_acronyms`` utility with a custom acronym options class. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('acronym', CustomAcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('acronym', AcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('acronym', CustomAcronymTreeNode)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('acronym', AcronymTreeNode)
        acronyms = extract_acronyms(document_tree, acronym_node_cls=CustomAcronymTreeNode)
        self.assertEqual([a1, a3], acronyms)
