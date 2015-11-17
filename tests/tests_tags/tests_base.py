"""
SkCode base tag test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (TagOptions,
                         WrappingTagOptions,
                         InlineWrappingTagOptions)


class TagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``TagOptions`` base cass. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)


    def test_init_kwargs_setter(self):
        """ Test modification of constants at constructor. """
        opts = TagOptions(newline_closes=True)
        self.assertTrue(opts.newline_closes)
        opts = TagOptions(same_tag_closes=True)
        self.assertTrue(opts.same_tag_closes)
        opts = TagOptions(standalone=True)
        self.assertTrue(opts.standalone)
        opts = TagOptions(parse_embedded=False)
        self.assertFalse(opts.parse_embedded)
        opts = TagOptions(swallow_trailing_newline=True)
        self.assertTrue(opts.swallow_trailing_newline)
        opts = TagOptions(inline=True)
        self.assertTrue(opts.inline)
        opts = TagOptions(close_inlines=False)
        self.assertFalse(opts.close_inlines)
        opts = TagOptions(make_paragraphs_here=True)
        self.assertTrue(opts.make_paragraphs_here)

    def test_default_sanitize_node_policy(self):
        """ Test default ``sanitize_node`` method policy. """
        # TODO
        pass

    def test_default_postprocess_node_implementation(self):
        """ Test default ``postprocess_node`` method implementation. """
        opts = TagOptions()
        self.assertFalse(opts.postprocess_node(None, None))

    def test_default_render_html_implementation(self):
        """ Test default ``render_html`` method implementation. """
        opts = TagOptions()
        with self.assertRaises(NotImplementedError):
            opts.render_html(None, '')

    def test_default_render_text_implementation(self):
        """ Test default ``render_text`` method implementation. """
        opts = TagOptions()
        with self.assertRaises(NotImplementedError):
            opts.render_html(None, '')

    def test_default_render_skcode_implementation(self):
        """ Test default ``render_skcode`` method implementation. """
        opts = TagOptions()
        with self.assertRaises(NotImplementedError):
            opts.render_html(None, '')


class WrappingTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``WrappingTagOptions`` class. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = WrappingTagOptions('%s')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_wrapping_format_set(self):
        """ Test if the wrapping format is correctly set at constructor. """
        opts = WrappingTagOptions('foo %s bar')
        self.assertEqual('foo %s bar', opts.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = WrappingTagOptions('foo %s bar')
        output_result = opts.render_html(None, 'test')
        self.assertEqual('foo test bar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = WrappingTagOptions('foo %s bar')
        output_result = opts.render_text(None, 'test')
        self.assertEqual('test', output_result)

    def test_render_skcode(self):
        """ Test the ``render_text`` method. """
        opts = WrappingTagOptions('foo %s bar')
        tree_node = TreeNode(None, 'test', opts)
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        self.assertEqual('[test]Hello World![/test]', output_result)


class InlineWrappingTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``InlineWrappingTagOptions`` class. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = InlineWrappingTagOptions('%s')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_wrapping_format_set(self):
        """ Test if the wrapping format is correctly set at constructor. """
        opts = InlineWrappingTagOptions('foo %s bar')
        self.assertEqual('foo %s bar', opts.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = InlineWrappingTagOptions('foo %s bar')
        output_result = opts.render_html(None, 'test')
        self.assertEqual('foo test bar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = InlineWrappingTagOptions('foo %s bar')
        output_result = opts.render_text(None, 'test')
        self.assertEqual('test', output_result)

    def test_render_skcode(self):
        """ Test the ``render_text`` method. """
        opts = InlineWrappingTagOptions('foo %s bar')
        tree_node = TreeNode(None, 'test', opts)
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        self.assertEqual('[test]Hello World![/test]', output_result)
