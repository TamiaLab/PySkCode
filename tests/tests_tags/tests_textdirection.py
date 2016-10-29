"""
SkCode text direction tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    DirectionTextTreeNode,
    LTRFixedDirectionTextTreeNode,
    RTLFixedDirectionTextTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.tags.textdirection import (
    TEXT_DIR_LEFT_TO_RIGHT,
    TEXT_DIR_RIGHT_TO_LEFT
)


class DirectionTextTagTestCase(unittest.TestCase):
    """ Tests suite for the text direction tag module. """

    def test_module_constants(self):
        """ Test module level constants """
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, 1)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, 2)

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(DirectionTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(LTRFixedDirectionTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        self.assertIn(RTLFixedDirectionTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(DirectionTextTreeNode.newline_closes)
        self.assertFalse(DirectionTextTreeNode.same_tag_closes)
        self.assertFalse(DirectionTextTreeNode.weak_parent_close)
        self.assertFalse(DirectionTextTreeNode.standalone)
        self.assertTrue(DirectionTextTreeNode.parse_embedded)
        self.assertTrue(DirectionTextTreeNode.inline)
        self.assertFalse(DirectionTextTreeNode.close_inlines)
        self.assertEqual('bdo', DirectionTextTreeNode.canonical_tag_name)
        self.assertEqual((), DirectionTextTreeNode.alias_tag_names)
        self.assertFalse(DirectionTextTreeNode.make_paragraphs_here)
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, DirectionTextTreeNode.default_text_direction)
        self.assertEqual({
            'ltr': TEXT_DIR_LEFT_TO_RIGHT,
            'rtl': TEXT_DIR_RIGHT_TO_LEFT,
        }, DirectionTextTreeNode.text_direction_map)
        self.assertEqual({
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        }, DirectionTextTreeNode.reverse_text_direction_map)
        self.assertEqual({
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        }, DirectionTextTreeNode.bdo_html_attr_value_map)
        self.assertEqual('dir', DirectionTextTreeNode.text_direction_attr_name)
        self.assertEqual('<bdo dir="{text_direction}">{inner_html}</bdo>', DirectionTextTreeNode.html_render_template)

    def test_get_text_direction_with_tagname_set(self):
        """ Test the ``get_text_direction`` with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'bdo': 'rtl'})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the "dir" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'rtl'})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_tagname_and_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the tag name and "dir" attribute  set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'rtl', 'bdo': 'ltr'})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, text_direction)

    def test_get_text_direction_with_default_value(self):
        """ Test the ``get_text_direction`` without any value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(tree_node.default_text_direction, text_direction)

    def test_get_text_direction_with_uppercase(self):
        """ Test the ``get_text_direction`` with the "dir" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'RtL'})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_invalid_value(self):
        """ Test the ``get_text_direction`` with an invalid/unknown value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'foobar'})
        text_direction = tree_node.get_text_direction()
        self.assertEqual(tree_node.default_text_direction, text_direction)

    def test_render_html_ltr(self):
        """ Test the ``render_html`` method in LTR mode. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'ltr'})
        output_result = tree_node.render_html('john doe')
        expected_result = '<bdo dir="ltr">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_rtl(self):
        """ Test the ``render_html`` method in RTL mode. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'rtl'})
        output_result = tree_node.render_html('john doe')
        expected_result = '<bdo dir="rtl">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_ltr(self):
        """ Test the ``render_text`` method in LTR mode. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'ltr'})
        output_result = tree_node.render_text('john doe')
        expected_result = 'john doe'
        self.assertEqual(expected_result, output_result)

    def test_render_text_rtl(self):
        """ Test the ``render_text`` method in RTL mode. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('bdo', DirectionTextTreeNode, attrs={'dir': 'rtl'})
        output_result = tree_node.render_text('john doe')
        expected_result = 'eod nhoj'
        self.assertEqual(expected_result, output_result)

    def test_get_text_direction_method(self):
        """ Test the ``get_text_direction`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('rtl', RTLFixedDirectionTextTreeNode, attrs={})
        color_value = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, color_value)
        tree_node = root_tree_node.new_child('rtl', LTRFixedDirectionTextTreeNode, attrs={})
        color_value = tree_node.get_text_direction()
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, color_value)
