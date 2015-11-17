"""
SkCode spoiler tag test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (SpoilerTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class HorizontalLineTagTestCase(unittest.TestCase):
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

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = SpoilerTagOptions()
        self.assertEqual('<div class="spoiler">test</div>\n', opts.render_html(None, 'test'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = SpoilerTagOptions()
        self.assertEqual('!!! SPOILER !!!\n! test\n!!!\n', opts.render_text(None, 'test'))

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = SpoilerTagOptions()
        tree_node = TreeNode(None, 'spoiler', opts)
        self.assertEqual('[spoiler]test[/spoiler]', opts.render_skcode(tree_node, 'test'))
