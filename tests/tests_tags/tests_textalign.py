"""
SkCode text align tags test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags.textalign import TextAlignBaseTagOptions
from skcode.tags import (CenterTextTagOptions,
                         LeftTextTagOptions,
                         RightTextTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TextAlignTagsTestCase(unittest.TestCase):
    """ Tests suite for text align tags module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('center', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['center'], CenterTextTagOptions)
        self.assertIn('left', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['left'], LeftTextTagOptions)
        self.assertIn('right', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['right'], RightTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TextAlignBaseTagOptions('center')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html_center(self):
        """ Test the ``render_html`` method. """
        opts = CenterTextTagOptions()
        tree_node = TreeNode(None, 'center', opts)
        self.assertEqual('<p class="text-center">test</p>\n', opts.render_html(tree_node, 'test'))

    def test_render_html_left(self):
        """ Test the ``render_html`` method. """
        opts = LeftTextTagOptions()
        tree_node = TreeNode(None, 'left', opts)
        self.assertEqual('<p class="text-left">test</p>\n', opts.render_html(tree_node, 'test'))

    def test_render_html_right(self):
        """ Test the ``render_html`` method. """
        opts = RightTextTagOptions()
        tree_node = TreeNode(None, 'right', opts)
        self.assertEqual('<p class="text-right">test</p>\n', opts.render_html(tree_node, 'test'))

    def test_render_text_center(self):
        """ Test the ``render_text`` method. """
        opts = CenterTextTagOptions()
        tree_node = TreeNode(None, 'center', opts)
        self.assertEqual('test', opts.render_text(tree_node, 'test'))

    def test_render_text_left(self):
        """ Test the ``render_text`` method. """
        opts = LeftTextTagOptions()
        tree_node = TreeNode(None, 'left', opts)
        self.assertEqual('test', opts.render_text(tree_node, 'test'))

    def test_render_text_right(self):
        """ Test the ``render_text`` method. """
        opts = RightTextTagOptions()
        tree_node = TreeNode(None, 'right', opts)
        self.assertEqual('test', opts.render_text(tree_node, 'test'))

    def test_render_skcode_center(self):
        """ Test the ``render_skcode`` method. """
        opts = CenterTextTagOptions()
        tree_node = TreeNode(None, 'center', opts)
        self.assertEqual('[center]test[/center]', opts.render_skcode(tree_node, 'test'))

    def test_render_skcode_left(self):
        """ Test the ``render_skcode`` method. """
        opts = LeftTextTagOptions()
        tree_node = TreeNode(None, 'left', opts)
        self.assertEqual('[left]test[/left]', opts.render_skcode(tree_node, 'test'))

    def test_render_skcode_right(self):
        """ Test the ``render_skcode`` method. """
        opts = RightTextTagOptions()
        tree_node = TreeNode(None, 'right', opts)
        self.assertEqual('[right]test[/right]', opts.render_skcode(tree_node, 'test'))
