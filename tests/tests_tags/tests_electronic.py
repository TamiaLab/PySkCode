"""
SkCode electronic special tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    NotNotationTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class NotNotationTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the NOT notation tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(NotNotationTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(NotNotationTreeNode.newline_closes)
        self.assertFalse(NotNotationTreeNode.same_tag_closes)
        self.assertFalse(NotNotationTreeNode.weak_parent_close)
        self.assertFalse(NotNotationTreeNode.standalone)
        self.assertTrue(NotNotationTreeNode.parse_embedded)
        self.assertTrue(NotNotationTreeNode.inline)
        self.assertFalse(NotNotationTreeNode.close_inlines)
        self.assertEqual('not', NotNotationTreeNode.canonical_tag_name)
        self.assertEqual((), NotNotationTreeNode.alias_tag_names)
        self.assertFalse(NotNotationTreeNode.make_paragraphs_here)
        self.assertEqual('<span style="text-decoration:overline; '
                         'text-transform: uppercase;">{inner_html}</span>', NotNotationTreeNode.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_html('RESET')
        expected_output = '<span style="text-decoration:overline; text-transform: uppercase;">RESET</span>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_text('RESET')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_auto_upper(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_text('reset')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_no_text(self):
        """ Test text rendering with no text. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_text('')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_only_whitespaces(self):
        """ Test text rendering with no text. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_text('    ')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespace(self):
        """ Test text rendering with trailing whitespaces. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('not', NotNotationTreeNode)
        rendered_output = tree_node.render_text('   RESET ')
        expected_output = ' /RESET '
        self.assertEqual(expected_output, rendered_output)
