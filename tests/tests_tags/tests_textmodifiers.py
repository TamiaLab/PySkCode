"""
SkCode text modifiers tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    LowerCaseTextTreeNode,
    UpperCaseTextTreeNode,
    CapitalizeTextTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class TextModifierTagsTestCase(unittest.TestCase):
    """ Tests suite for text modifier tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(LowerCaseTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(UpperCaseTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(CapitalizeTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(LowerCaseTextTreeNode.newline_closes)
        self.assertFalse(LowerCaseTextTreeNode.same_tag_closes)
        self.assertFalse(LowerCaseTextTreeNode.standalone)
        self.assertTrue(LowerCaseTextTreeNode.parse_embedded)
        self.assertTrue(LowerCaseTextTreeNode.inline)
        self.assertFalse(LowerCaseTextTreeNode.close_inlines)
        self.assertEqual((), LowerCaseTextTreeNode.alias_tag_names)
        self.assertFalse(LowerCaseTextTreeNode.make_paragraphs_here)
        self.assertEqual('<span class="text-{text_modifier}">{inner_html}</span>\n',
                         LowerCaseTextTreeNode.html_render_template)

    def test_render_html_lowercase(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('lowercase', LowerCaseTextTreeNode)
        self.assertEqual('<span class="text-lowercase">test</span>\n', tree_node.render_html('test'))

    def test_render_html_uppercase(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('uppercase', UpperCaseTextTreeNode)
        self.assertEqual('<span class="text-uppercase">test</span>\n', tree_node.render_html('test'))

    def test_render_html_capitalize(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('capitalize', CapitalizeTextTreeNode)
        self.assertEqual('<span class="text-capitalize">test</span>\n', tree_node.render_html('test'))

    def test_render_text_lowercase(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('lowercase', LowerCaseTextTreeNode)
        self.assertEqual('test', tree_node.render_text('teST'))

    def test_render_text_uppercase(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('uppercase', UpperCaseTextTreeNode)
        self.assertEqual('TEST', tree_node.render_text('teST'))

    def test_render_text_capitalize(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('capitalize', CapitalizeTextTreeNode)
        self.assertEqual('Test', tree_node.render_text('test'))
