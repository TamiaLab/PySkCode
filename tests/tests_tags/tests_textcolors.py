"""
SkCode coloured text tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags.textcolors import RGB_COLOR_RE
from skcode.tags import (RootTagOptions,
                         ColorTextTagOptions,
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
        self.assertEqual('color', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual(('aqua', 'black', 'blue',
                          'fuchsia', 'gray', 'green',
                          'lime', 'maroon', 'navy',
                          'olive', 'orange', 'purple',
                          'red', 'silver', 'teal',
                          'white', 'yellow'), opts.known_colors)
        self.assertEqual('<span style="color: {color_value}">{inner_html}</span>', opts.html_render_template)

    def test_get_color_value_with_hex_code(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': '#FFFFFF'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('#ffffff', color)

    def test_get_color_value_with_named_color(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': 'black'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('black', color)

    def test_get_color_value_with_named_color_uppercase(self):
        """ Test the ``get_color_value`` method (ignore case). """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': 'BLAck'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('black', color)

    def test_get_color_value_with_no_value(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={})
        color = opts.get_color_value(tree_node)
        self.assertEqual('', color)

    def test_get_color_value_with_invalid_color(self):
        """ Test the ``get_color_value`` method. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': 'foobar'})
        color = opts.get_color_value(tree_node)
        self.assertEqual('', color)

    def test_render_html(self):
        """ Test the ``render_html`` method with a valid color. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<span style="color: #ffffff">Hello World!</span>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_invalid_color(self):
        """ Test the ``render_html`` method with an invalid color. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': 'foobar'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method with a valid color. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method with a valid color. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': '#FFFFFF'})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'color': '#ffffff'}, 'color')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_invalid_color(self):
        """ Test the ``get_skcode_attributes`` method with an invalid color. """
        opts = ColorTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': 'foobar'})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'color': ''}, 'color')
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
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={'color': '#FFFFFF'})
        self.assertEqual('test', opts.get_color_value(tree_node))

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method with a valid color. """
        opts = FixedColorTextTagOptions('test')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('color', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)
