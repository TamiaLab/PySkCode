"""
SkCode specials tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         NoParseTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class NoParseTagTestCase(unittest.TestCase):
    """ Tests suite for the special "no parse" tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('noparse', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['noparse'], NoParseTagOptions)
        self.assertIn('nobbc', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['nobbc'], NoParseTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = NoParseTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertFalse(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... some text[/u]')
        rendered_output = opts.render_html(tree_node, '')
        expected_output = '[u]... some text[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities(self):
        """ Test HTML rendering with HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... <some text>[/u]')
        rendered_output = opts.render_html(tree_node, '')
        expected_output = '[u]... &lt;some text&gt;[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_encoded_html_entities(self):
        """ Test HTML rendering with encoded HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = opts.render_html(tree_node, '')
        expected_output = '[u]... &lt;some text&gt;[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... some text[/u]')
        rendered_output = opts.render_text(tree_node, '')
        expected_output = '[u]... some text[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities(self):
        """ Test text rendering with HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... <some text>[/u]')
        rendered_output = opts.render_text(tree_node, '')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_encoded_html_entities(self):
        """ Test text rendering with encoded HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = opts.render_text(tree_node, '')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_inner_content(self):
        """ Test the ``get_skcode_inner_content`` method. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... some text[/u]')
        rendered_output = opts.get_skcode_inner_content(tree_node, '')
        expected_output = '[u]... some text[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_inner_content_with_html_entities(self):
        """ Test the ``get_skcode_inner_content`` method with HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = opts.get_skcode_inner_content(tree_node, '')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_inner_content_with_encoded_html_entities(self):
        """ Test the ``get_skcode_inner_content`` method with encoded HTML entities. """
        opts = NoParseTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('noparse', opts, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = opts.get_skcode_inner_content(tree_node, '')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)
