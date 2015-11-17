"""
SkCode text direction tags test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (DirectionTextTagOptions,
                         FixedDirectionTextTagOptions,
                         TEXT_DIR_LEFT_TO_RIGHT,
                         TEXT_DIR_RIGHT_TO_LEFT,
                         DEFAULT_RECOGNIZED_TAGS)


class DirectionTextTagTestCase(unittest.TestCase):
    """ Tests suite for the text direction tag module. """

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
        self.assertFalse(opts.make_paragraphs_here)

        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, opts.default_text_direction)
        self.assertEqual(opts.text_direction_map, {
            'ltr': TEXT_DIR_LEFT_TO_RIGHT,
            'rtl': TEXT_DIR_RIGHT_TO_LEFT,
        })
        self.assertEqual(opts.reverse_text_direction_map, {
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        })
        self.assertEqual(opts.bdo_html_attr_value_map, {
            TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
            TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
        })
        self.assertEqual('dir', opts.text_direction_attr_name)

    def test_get_text_direction_with_tagname_set(self):
        """ Test the ``get_text_direction`` with the tag name attribute set. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'bdo': 'rtl'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the "dir" attribute set. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'rtl'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_RIGHT_TO_LEFT, text_direction)

    def test_get_text_direction_with_tagname_and_dir_attr_set(self):
        """ Test the ``get_text_direction`` with the tag name and "dir" attribute  set. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'rtl', 'bdo': 'ltr'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(TEXT_DIR_LEFT_TO_RIGHT, text_direction)

    def test_get_text_direction_with_default_value(self):
        """ Test the ``get_text_direction`` without any value set. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(opts.default_text_direction, text_direction)

    def test_get_text_direction_with_invalid_value(self):
        """ Test the ``get_text_direction`` with an invalid/unknown value set. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'foobar'})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(opts.default_text_direction, text_direction)

    def test_render_html_ltr(self):
        """ Test the ``render_html`` method in LTR mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.render_html(tree_node, 'john doe')
        expected_result = '<bdo dir="ltr">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_rtl(self):
        """ Test the ``render_html`` method in RTL mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'rtl'})
        output_result = opts.render_html(tree_node, 'john doe')
        expected_result = '<bdo dir="rtl">john doe</bdo>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_ltr(self):
        """ Test the ``render_text`` method in LTR mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.render_text(tree_node, 'john doe')
        expected_result = 'john doe'
        self.assertEqual(expected_result, output_result)

    def test_render_text_rtl(self):
        """ Test the ``render_text`` method in RTL mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'rtl'})
        output_result = opts.render_text(tree_node, 'john doe')
        expected_result = 'eod nhoj'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_ltr(self):
        """ Test the ``render_skcode`` method in LTR mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'ltr'})
        output_result = opts.render_skcode(tree_node, 'john doe')
        expected_result = '[bdo dir="ltr"]john doe[/bdo]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_rtl(self):
        """ Test the ``render_skcode`` method in RTL mode. """
        opts = DirectionTextTagOptions()
        tree_node = TreeNode(None, 'bdo', opts, attrs={'dir': 'rtl'})
        output_result = opts.render_skcode(tree_node, 'john doe')
        expected_result = '[bdo dir="rtl"]john doe[/bdo]'
        self.assertEqual(expected_result, output_result)


class FixedDirectionTextTagtestCase(unittest.TestCase):
    """ Tests suite for the fixed text direction tag module. """

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
        opts = FixedDirectionTextTagOptions(2)
        tree_node = TreeNode(None, 'bdo', opts, attrs={})
        text_direction = opts.get_text_direction(tree_node)
        self.assertEqual(2, text_direction)

    def test_render_skcode_ltr(self):
        """ Test the ``render_skcode`` method in LTR mode. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_LEFT_TO_RIGHT)
        tree_node = TreeNode(None, 'ltr', opts, attrs={})
        output_result = opts.render_skcode(tree_node, 'john doe')
        expected_result = '[ltr]john doe[/ltr]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_rtl(self):
        """ Test the ``render_skcode`` method in RTL mode. """
        opts = FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT)
        tree_node = TreeNode(None, 'rtl', opts, attrs={})
        output_result = opts.render_skcode(tree_node, 'john doe')
        expected_result = '[rtl]john doe[/rtl]'
        self.assertEqual(expected_result, output_result)
