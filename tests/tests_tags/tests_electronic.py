"""
SkCode electronic tag test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (NotNotationTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class NotNotationTagtestCase(unittest.TestCase):
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
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = NotNotationTagOptions()
        tree_node = TreeNode(None, 'not', opts)
        rendered_output = opts.render_html(tree_node, 'RESET')
        expected_output = '<span style="text-decoration:overline; text-transform: uppercase;">RESET</span>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = NotNotationTagOptions()
        tree_node = TreeNode(None, 'not', opts)
        rendered_output = opts.render_text(tree_node, 'RESET')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_auto_upper(self):
        """ Test text rendering. """
        opts = NotNotationTagOptions()
        tree_node = TreeNode(None, 'not', opts)
        rendered_output = opts.render_text(tree_node, 'reset')
        expected_output = '/RESET'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        opts = NotNotationTagOptions()
        tree_node = TreeNode(None, 'not', opts)
        rendered_output = opts.render_skcode(tree_node, 'RESET')
        expected_output = '[not]RESET[/not]'
        self.assertEqual(expected_output, rendered_output)
