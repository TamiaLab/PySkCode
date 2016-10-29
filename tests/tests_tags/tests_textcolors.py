"""
SkCode coloured text tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags.textcolors import RGB_COLOR_RE
from skcode.tags import (
    ColorTextTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST,
    generate_fixed_color_text_cls
)


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
        self.assertIn(ColorTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(ColorTextTreeNode.newline_closes)
        self.assertFalse(ColorTextTreeNode.same_tag_closes)
        self.assertFalse(ColorTextTreeNode.weak_parent_close)
        self.assertFalse(ColorTextTreeNode.standalone)
        self.assertTrue(ColorTextTreeNode.parse_embedded)
        self.assertTrue(ColorTextTreeNode.inline)
        self.assertFalse(ColorTextTreeNode.close_inlines)
        self.assertEqual('color', ColorTextTreeNode.canonical_tag_name)
        self.assertEqual((), ColorTextTreeNode.alias_tag_names)
        self.assertFalse(ColorTextTreeNode.make_paragraphs_here)
        self.assertEqual(('aqua', 'black', 'blue',
                          'fuchsia', 'gray', 'green',
                          'lime', 'maroon', 'navy',
                          'olive', 'orange', 'purple',
                          'red', 'silver', 'teal',
                          'white', 'yellow'), ColorTextTreeNode.known_colors)
        self.assertEqual('<span style="color: {color_value}">{inner_html}</span>',
                         ColorTextTreeNode.html_render_template)

    def test_get_color_value_with_hex_code(self):
        """ Test the ``get_color_value`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': '#FFFFFF'})
        color = tree_node.get_color_value()
        self.assertEqual('#ffffff', color)

    def test_get_color_value_with_named_color(self):
        """ Test the ``get_color_value`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': 'black'})
        color = tree_node.get_color_value()
        self.assertEqual('black', color)

    def test_get_color_value_with_named_color_uppercase(self):
        """ Test the ``get_color_value`` method (ignore case). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': 'BLAck'})
        color = tree_node.get_color_value()
        self.assertEqual('black', color)

    def test_get_color_value_with_no_value(self):
        """ Test the ``get_color_value`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={})
        color = tree_node.get_color_value()
        self.assertEqual('', color)

    def test_get_color_value_with_invalid_color(self):
        """ Test the ``get_color_value`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': 'foobar'})
        color = tree_node.get_color_value()
        self.assertEqual('', color)

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': 'blue'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': ''})
        tree_node.sanitize_node([])
        self.assertEqual('Missing color value', tree_node.error_message)

    def test_render_html(self):
        """ Test the ``render_html`` method with a valid color. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': '#FFFFFF'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<span style="color: #ffffff">Hello World!</span>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_invalid_color(self):
        """ Test the ``render_html`` method with an invalid color. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': 'foobar'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method with a valid color. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('color', ColorTextTreeNode, attrs={'color': '#FFFFFF'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)


class FixedTextColorTagTestCase(unittest.TestCase):
    """ Tests suite for the color tags module (fixed type color variants). """

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = generate_fixed_color_text_cls('customtype')
        self.assertEqual('customtype', opts.color_value)
        self.assertEqual('customtype', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = generate_fixed_color_text_cls('customtype', canonical_tag_name='foobar')
        self.assertEqual('customtype', opts.color_value)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_get_color_value_method(self):
        """ Test the ``get_color_value`` method. """
        opts = generate_fixed_color_text_cls('customtype')
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', opts, attrs={})
        color_value = opts.get_color_value(tree_node)
        self.assertEqual('customtype', color_value)
