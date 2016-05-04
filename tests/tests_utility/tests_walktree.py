"""
SkCode walk tree utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TagOptions)
from skcode.utility.walketree import walk_tree_for_cls


class CustomTagOptions(TagOptions):
    """
    Custom ``TagOptions`` subclass for tests.
    """

    canonical_tag_name = 'test'
    alias_tag_names = ()


class WalkTreeUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the walk tree utility module. """

    def test_walk_tree_for_cls(self):
        """ Test the ``walk_tree_for_cls`` helper. """
        document_tree = RootTreeNode(RootTagOptions())
        node1 = document_tree.new_child('node', CustomTagOptions())
        l1_tree_node = document_tree.new_child('test_l1', TagOptions(canonical_tag_name='dummy'))
        node2 = l1_tree_node.new_child('node', CustomTagOptions())
        l2_tree_node = l1_tree_node.new_child('test_l2', TagOptions(canonical_tag_name='dummy'))
        node3 = l2_tree_node.new_child('node', CustomTagOptions())
        nodes = list(walk_tree_for_cls(document_tree, CustomTagOptions))
        self.assertEqual([node1, node2, node3], nodes)
