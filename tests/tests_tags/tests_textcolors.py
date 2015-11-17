"""
SkCode text colors tags test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags.textcolors import RGB_COLOR_RE
from skcode.tags import (ColorTextTagOptions,
                         FixedColorTextTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class W3CHexColorsTestCase(unittest.TestCase):
    """ Tests suite for the color regex (W3C compliant). """

    def test_rgb_hex_full(self):
        """ Test #RRGGBB format. """
        self.assertTrue(RGB_COLOR_RE.match('#000000'))
        self.assertFalse(RGB_COLOR_RE.match('000000'))
        self.assertTrue(RGB_COLOR_RE.match('#ffffff'))
        self.assertFalse(RGB_COLOR_RE.match('ffffff'))
        self.assertTrue(RGB_COLOR_RE.match('#FFFFFF'))
        self.assertFalse(RGB_COLOR_RE.match('FFFFFF'))

    def test_rgb_hex_half(self):
        """ Test #RGB format. """
        self.assertTrue(RGB_COLOR_RE.match('#000'))
        self.assertFalse(RGB_COLOR_RE.match('000'))
        self.assertTrue(RGB_COLOR_RE.match('#fff'))
        self.assertFalse(RGB_COLOR_RE.match('fff'))
        self.assertTrue(RGB_COLOR_RE.match('#FFF'))
        self.assertFalse(RGB_COLOR_RE.match('FFF'))


class TextColorTagsTestCase(unittest.TestCase):
    """ Tests suite for text color tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('color', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['color'], ColorTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ColorTextTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual(opts.known_colors, (
            'aqua', 'black', 'blue',
            'fuchsia', 'gray', 'green',
            'lime', 'maroon', 'navy',
            'olive', 'orange', 'purple',
            'red', 'silver', 'teal',
            'white', 'yellow'
        ))

    def test_get_color_value_with_hex_code(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': '#FFFFFF'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('#FFFFFF', color)

    def test_get_color_value_with_named_color(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': 'black'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('black', color)

    def test_get_color_value_with_no_value(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={})
        color = opts.get_color_value(tree_node)
        self.assertEqual('', color)

    def test_get_color_value_with_invalid_color(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': 'foobar'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('', color)

    def test_render_html(self):
        """ Test the ``render_html`` method with a valid color. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<span style="color: #FFFFFF">Hello World!</span>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_invalid_color(self):
        """ Test the ``render_html`` method with an invalid color. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': 'foobar'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method with a valid color. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method with a valid color. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[color="#FFFFFF"]Hello World![/color]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_invalid_color(self):
        """ Test the ``render_skcode`` method with an invalid color. """
        opts = ColorTextTagOptions()
        tree_node = TreeNode(None, 'color', opts, attrs={'color': 'foobar'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)


class FixedTextColorTagsTestCase(unittest.TestCase):
    """ Tests suite for fixed text color tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('black', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['black'], FixedColorTextTagOptions)
        self.assertEqual('black', DEFAULT_RECOGNIZED_TAGS['black'].color_value)
        self.assertIn('blue', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['blue'], FixedColorTextTagOptions)
        self.assertEqual('blue', DEFAULT_RECOGNIZED_TAGS['blue'].color_value)
        self.assertIn('gray', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['gray'], FixedColorTextTagOptions)
        self.assertEqual('gray', DEFAULT_RECOGNIZED_TAGS['gray'].color_value)
        self.assertIn('green', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['green'], FixedColorTextTagOptions)
        self.assertEqual('green', DEFAULT_RECOGNIZED_TAGS['green'].color_value)
        self.assertIn('orange', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['orange'], FixedColorTextTagOptions)
        self.assertEqual('orange', DEFAULT_RECOGNIZED_TAGS['orange'].color_value)
        self.assertIn('purple', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['purple'], FixedColorTextTagOptions)
        self.assertEqual('purple', DEFAULT_RECOGNIZED_TAGS['purple'].color_value)
        self.assertIn('red', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['red'], FixedColorTextTagOptions)
        self.assertEqual('red', DEFAULT_RECOGNIZED_TAGS['red'].color_value)
        self.assertIn('white', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['white'], FixedColorTextTagOptions)
        self.assertEqual('white', DEFAULT_RECOGNIZED_TAGS['white'].color_value)
        self.assertIn('yellow', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['yellow'], FixedColorTextTagOptions)
        self.assertEqual('yellow', DEFAULT_RECOGNIZED_TAGS['yellow'].color_value)

    def test_get_color_value(self):
        """ Test the ``get_color_value`` method. """
        opts = FixedColorTextTagOptions('test')
        self.assertEqual('test', opts.get_color_value(None))

    def test_render_skcode(self):
        opts = FixedColorTextTagOptions('black')
        tree_node = TreeNode(None, 'black', opts)
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[black]Hello World![/black]'
        self.assertEqual(expected_result, output_result)
