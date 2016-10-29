"""
SkCode text align tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags.textalign import TextAlignBaseTreeNode
from skcode.tags import (
    CenterTextTreeNode,
    LeftTextTreeNode,
    RightTextTreeNode,
    JustifyTextTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class TextAlignTagsTestCase(unittest.TestCase):
    """ Tests suite for text align tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(CenterTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(LeftTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(RightTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(JustifyTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(CenterTextTreeNode.newline_closes)
        self.assertFalse(CenterTextTreeNode.same_tag_closes)
        self.assertFalse(CenterTextTreeNode.weak_parent_close)
        self.assertFalse(CenterTextTreeNode.standalone)
        self.assertTrue(CenterTextTreeNode.parse_embedded)
        self.assertFalse(CenterTextTreeNode.inline)
        self.assertTrue(CenterTextTreeNode.close_inlines)
        self.assertEqual('center', CenterTextTreeNode.canonical_tag_name)
        self.assertEqual((), CenterTextTreeNode.alias_tag_names)
        self.assertFalse(CenterTextTreeNode.make_paragraphs_here)
        self.assertEqual('<p class="text-{text_alignment}">{inner_html}</p>\n', CenterTextTreeNode.html_render_template)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('center', CenterTextTreeNode)
        self.assertEqual('<p class="text-center">test</p>\n', tree_node.render_html('test'))
        tree_node = root_tree_node.new_child('center', LeftTextTreeNode)
        self.assertEqual('<p class="text-left">test</p>\n', tree_node.render_html('test'))
        tree_node = root_tree_node.new_child('center', RightTextTreeNode)
        self.assertEqual('<p class="text-right">test</p>\n', tree_node.render_html('test'))
        tree_node = root_tree_node.new_child('center', JustifyTextTreeNode)
        self.assertEqual('<p class="text-justify">test</p>\n', tree_node.render_html('test'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('center', CenterTextTreeNode)
        self.assertEqual('test', tree_node.render_text('test'))
        tree_node = root_tree_node.new_child('center', LeftTextTreeNode)
        self.assertEqual('test', tree_node.render_text('test'))
        tree_node = root_tree_node.new_child('center', RightTextTreeNode)
        self.assertEqual('test', tree_node.render_text('test'))
        tree_node = root_tree_node.new_child('center', JustifyTextTreeNode)
        self.assertEqual('test', tree_node.render_text('test'))

    def test_center_subclass(self):
        """ Test the center subclass """
        self.assertTrue(issubclass(CenterTextTreeNode, TextAlignBaseTreeNode))
        self.assertEqual('center', CenterTextTreeNode.canonical_tag_name)
        self.assertEqual('center', CenterTextTreeNode.text_alignment)

    def test_left_subclass(self):
        """ Test the left subclass """
        self.assertTrue(issubclass(LeftTextTreeNode, TextAlignBaseTreeNode))
        self.assertEqual('left', LeftTextTreeNode.canonical_tag_name)
        self.assertEqual('left', LeftTextTreeNode.text_alignment)

    def test_right_subclass(self):
        """ Test the right subclass """
        self.assertTrue(issubclass(RightTextTreeNode, TextAlignBaseTreeNode))
        self.assertEqual('right', RightTextTreeNode.canonical_tag_name)
        self.assertEqual('right', RightTextTreeNode.text_alignment)

    def test_justify_subclass(self):
        """ Test the justify subclass """
        self.assertTrue(issubclass(JustifyTextTreeNode, TextAlignBaseTreeNode))
        self.assertEqual('justify', JustifyTextTreeNode.canonical_tag_name)
        self.assertEqual('justify', JustifyTextTreeNode.text_alignment)
