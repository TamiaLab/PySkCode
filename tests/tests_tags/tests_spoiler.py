"""
SkCode spoiler tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    SpoilerTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class CustomSpoilerTreeNode(SpoilerTreeNode):
    """ Custom spoiler class """
    css_class_name = 'custom_css'


class SpoilerTagTestCase(unittest.TestCase):
    """ Tests suite for the spoiler tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(SpoilerTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(SpoilerTreeNode.newline_closes)
        self.assertFalse(SpoilerTreeNode.same_tag_closes)
        self.assertFalse(SpoilerTreeNode.weak_parent_close)
        self.assertFalse(SpoilerTreeNode.standalone)
        self.assertTrue(SpoilerTreeNode.parse_embedded)
        self.assertFalse(SpoilerTreeNode.inline)
        self.assertTrue(SpoilerTreeNode.close_inlines)
        self.assertEqual('spoiler', SpoilerTreeNode.canonical_tag_name)
        self.assertEqual(('hide', ), SpoilerTreeNode.alias_tag_names)
        self.assertTrue(SpoilerTreeNode.make_paragraphs_here)
        self.assertEqual('spoiler', SpoilerTreeNode.css_class_name)
        self.assertEqual('<div class="{class_name}">{inner_html}</div>\n', SpoilerTreeNode.html_render_template)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('spoiler', SpoilerTreeNode)
        self.assertEqual('<div class="spoiler">test</div>\n', tree_node.render_html('test'))

    def test_render_html_custom_css(self):
        """ Test the ``render_html`` method with a custom CSS class name. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('spoiler', CustomSpoilerTreeNode)
        self.assertEqual('<div class="custom_css">test</div>\n', tree_node.render_html('test'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('spoiler', SpoilerTreeNode)
        self.assertEqual('!!! SPOILER !!!\n! test\n!!!\n', tree_node.render_text('test'))
