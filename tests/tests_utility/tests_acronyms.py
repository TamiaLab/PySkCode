"""
SkCode acronyms utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         AcronymTagOptions,
                         TextTagOptions)
from skcode.utility import extract_acronyms


class CustomAcronymTagOption(AcronymTagOptions):
    """
    Custom ``AcronymTagOptions`` subclass for tests.
    """
    pass


class AcronymsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the acronyms utility module. """

    def test_extract_acronyms(self):
        """ Test the ``extract_acronyms`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('acronym', AcronymTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a2 = document_tree.new_child('acronym', AcronymTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('acronym', AcronymTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a4 = document_tree.new_child('acronym', AcronymTagOptions())
        acronyms = extract_acronyms(document_tree)
        self.assertEqual([a1, a2, a3, a4], acronyms)

    def test_extract_acronyms_no_acronyms(self):
        """ Test the ``extract_acronyms`` utility with no acronym. """
        document_tree = RootTreeNode(RootTagOptions())
        acronyms = extract_acronyms(document_tree)
        self.assertEqual([], acronyms)

    def test_extract_acronyms_custom_class(self):
        """ Test the ``extract_acronyms`` utility with a custom acronym options class. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('acronym', CustomAcronymTagOption())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('acronym', AcronymTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('acronym', CustomAcronymTagOption())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('acronym', AcronymTagOptions())
        acronyms = extract_acronyms(document_tree, acronym_ops_cls=CustomAcronymTagOption)
        self.assertEqual([a1, a3], acronyms)
