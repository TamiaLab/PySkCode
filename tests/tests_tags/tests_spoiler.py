"""
SkCode spoiler tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         SpoilerTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class SpoilerTagTestCase(unittest.TestCase):
    """ Tests suite for the spoiler tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('spoiler', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['spoiler'], SpoilerTagOptions)
        self.assertIn('hide', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['hide'], SpoilerTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = SpoilerTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('spoiler', opts.css_class_name)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = SpoilerTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('spoiler', opts)
        self.assertEqual('<div class="spoiler">test</div>\n', opts.render_html(tree_node, 'test'))

    def test_render_html_custom_css(self):
        """ Test the ``render_html`` method with a custom CSS class name. """
        opts = SpoilerTagOptions(css_class_name='custom_css')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('spoiler', opts)
        self.assertEqual('<div class="custom_css">test</div>\n', opts.render_html(tree_node, 'test'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = SpoilerTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('spoiler', opts)
        self.assertEqual('!!! SPOILER !!!\n! test\n!!!\n', opts.render_text(tree_node, 'test'))
