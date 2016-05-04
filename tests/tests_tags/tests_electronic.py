"""
SkCode electronic special tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         NotNotationTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class NotNotationTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the NOT notation tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('not', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['not'], NotNotationTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = NotNotationTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertEqual('not', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('<span style="text-decoration:overline; '
                         'text-transform: uppercase;">{inner_html}</span>', opts.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_html(tree_node, 'RESET')
        expected_output = '<span style="text-decoration:overline; text-transform: uppercase;">RESET</span>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_text(tree_node, 'RESET')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_auto_upper(self):
        """ Test text rendering. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_text(tree_node, 'reset')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_no_text(self):
        """ Test text rendering with no text. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_text(tree_node, '')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_only_whitespaces(self):
        """ Test text rendering with no text. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_text(tree_node, '    ')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespace(self):
        """ Test text rendering with trailing whitespaces. """
        opts = NotNotationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('not', opts)
        rendered_output = opts.render_text(tree_node, '   RESET ')
        expected_output = ' /RESET '
        self.assertEqual(expected_output, rendered_output)
