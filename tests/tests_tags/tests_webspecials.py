"""
SkCode web special tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    HorizontalLineTreeNode,
    LineBreakTreeNode,
    CutHereTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class HorizontalLineTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the horizontal line tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(HorizontalLineTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(HorizontalLineTreeNode.newline_closes)
        self.assertFalse(HorizontalLineTreeNode.same_tag_closes)
        self.assertFalse(HorizontalLineTreeNode.weak_parent_close)
        self.assertTrue(HorizontalLineTreeNode.standalone)
        self.assertTrue(HorizontalLineTreeNode.parse_embedded)
        self.assertFalse(HorizontalLineTreeNode.inline)
        self.assertTrue(HorizontalLineTreeNode.close_inlines)
        self.assertEqual('hr', HorizontalLineTreeNode.canonical_tag_name)
        self.assertEqual((), HorizontalLineTreeNode.alias_tag_names)
        self.assertFalse(HorizontalLineTreeNode.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('hr', HorizontalLineTreeNode)
        self.assertEqual('<hr>\n', tree_node.render_html(''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('hr', HorizontalLineTreeNode)
        self.assertEqual('----------\n', tree_node.render_text(''))


class LineBreakTagTestCase(unittest.TestCase):
    """ Tests suite for the line break tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(LineBreakTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(LineBreakTreeNode.newline_closes)
        self.assertFalse(LineBreakTreeNode.same_tag_closes)
        self.assertFalse(LineBreakTreeNode.weak_parent_close)
        self.assertTrue(LineBreakTreeNode.standalone)
        self.assertTrue(LineBreakTreeNode.parse_embedded)
        self.assertTrue(LineBreakTreeNode.inline)
        self.assertFalse(LineBreakTreeNode.close_inlines)
        self.assertEqual('br', LineBreakTreeNode.canonical_tag_name)
        self.assertEqual((), LineBreakTreeNode.alias_tag_names)
        self.assertFalse(LineBreakTreeNode.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('br', LineBreakTreeNode)
        self.assertEqual('<br>\n', tree_node.render_html(''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('br', LineBreakTreeNode)
        self.assertEqual('\n', tree_node.render_text(''))


class CutHereTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the "cut here" tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(CutHereTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(CutHereTreeNode.newline_closes)
        self.assertFalse(CutHereTreeNode.same_tag_closes)
        self.assertFalse(CutHereTreeNode.weak_parent_close)
        self.assertTrue(CutHereTreeNode.standalone)
        self.assertTrue(CutHereTreeNode.parse_embedded)
        self.assertFalse(CutHereTreeNode.inline)
        self.assertTrue(CutHereTreeNode.close_inlines)
        self.assertEqual('cuthere', CutHereTreeNode.canonical_tag_name)
        self.assertEqual((), CutHereTreeNode.alias_tag_names)
        self.assertFalse(CutHereTreeNode.make_paragraphs_here)
        self.assertEqual('<!-- Cut Here -->', CutHereTreeNode.delimiter_string_html)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('cuthere', CutHereTreeNode)
        self.assertEqual('\n<!-- Cut Here -->\n', tree_node.render_html(''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('cuthere', CutHereTreeNode)
        self.assertEqual('', tree_node.render_text(''))
