"""
SkCode text direction tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         DirectionTextTagOptions,
                         FixedDirectionTextTagOptions,
                         TEXT_DIR_LEFT_TO_RIGHT,
                         TEXT_DIR_RIGHT_TO_LEFT,
                         DEFAULT_RECOGNIZED_TAGS)


class DirectionTextTagTestCase(unittest.TestCase):
    """ Tests suite for the text direction tag module. """

    def test_module_constants(self):
        """ Test module level constants """
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, 1)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, 2)

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('bdo', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['bdo'], DirectionTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = DirectionTextTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertEqual('bdo', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)

        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, opts.default_text_direction)
        self.assertEqual({
            'ltr': TEXT_DIR_LEFT_TO_RIGHT,
            'rtl': TEXT_DIR_RIGHT_TO_LEFT,
        }, opts.text_direction_map)
        self.assertEqual({
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        }, opts.reverse_text_direction_map)
        self.assertEqual({
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        }, opts.bdo_html_attr_value_map)
        self.assertEqual('dir', opts.text_direction_attr_name)
        self.assertEqual('<bdo dir="{text_direction}">{inner_html}</bdo>', opts.html_render_template)

    def test_get_text_direction_with_tagname_set(self):
        """ Test the ``get_text_direction`` with the tag name attribute set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'bdo': 'rtl'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the "dir" attribute set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'rtl'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_tagname_and_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the tag name and "dir" attribute  set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'rtl', 'bdo': 'ltr'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, text_direction)

    def test_get_text_direction_with_default_value(self):
        """ Test the ``get_text_direction`` without any value set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(opts.default_text_direction, text_direction)

    def test_get_text_direction_with_uppercase(self):
        """ Test the ``get_text_direction`` with the "dir" attribute set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'RtL'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_invalid_value(self):
        """ Test the ``get_text_direction`` with an invalid/unknown value set. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'foobar'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(opts.default_text_direction, text_direction)

    def test_render_html_ltr(self):
        """ Test the ``render_html`` method in LTR mode. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.render_html(tree_node, 'john doe')
        expected_result = '<bdo dir="ltr">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_rtl(self):
        """ Test the ``render_html`` method in RTL mode. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'rtl'})
        output_result = opts.render_html(tree_node, 'john doe')
        expected_result = '<bdo dir="rtl">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_ltr(self):
        """ Test the ``render_text`` method in LTR mode. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.render_text(tree_node, 'john doe')
        expected_result = 'john doe'
        self.assertEqual(expected_result, output_result)

    def test_render_text_rtl(self):
        """ Test the ``render_text`` method in RTL mode. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'rtl'})
        output_result = opts.render_text(tree_node, 'john doe')
        expected_result = 'eod nhoj'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = DirectionTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.get_skcode_attributes(tree_node, 'john doe')
        expected_result = ({'dir': 'ltr'}, 'dir')
        self.assertEqual(expected_result, output_result)


class FixedDirectionTextTagTestCase(unittest.TestCase):
    """ Tests suite for the fixed text direction tag module. """

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(FixedDirectionTextTagOptions, DirectionTextTagOptions))

    def test_assertion_constructor(self):
        """ Test assertion at ``__init__`` """
        with self.assertRaises(AssertionError) as e:
            FixedDirectionTextTagOptions(None)
        self.assertEqual('The text direction is mandatory.', str(e.exception))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('rtl', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['rtl'], FixedDirectionTextTagOptions)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, DEFAULT_RECOGNIZED_TAGS['rtl'].text_direction)
        self.assertIn('ltr', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ltr'], FixedDirectionTextTagOptions)
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, DEFAULT_RECOGNIZED_TAGS['ltr'].text_direction)

    def test_get_text_direction(self):
        """ Test the ``get_text_direction``. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('rtl', opts, attrs={'dir': 'test'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('rtl', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, 'john doe')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, opts.text_direction)
        self.assertEqual('rtl', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT, canonical_tag_name='foobar')
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, opts.text_direction)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
