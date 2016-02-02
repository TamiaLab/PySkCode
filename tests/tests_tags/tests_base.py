"""
SkCode base tag test code.
"""

import unittest

from skcode.etree import (RootTreeNode,
                          TreeNode)
from skcode.tags import (RootTagOptions,
                         TagOptions,
                         WrappingTagOptions,
                         InlineWrappingTagOptions)


class TagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``TagOptions`` base class. """

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
        opts = TagOptions(custom_value='foobar')
        self.assertEqual('foobar', opts.custom_value)

    def test_default_sanitize_node_policy(self):
        """ Test the default ``sanitize_node`` method policy. """
        opts = TagOptions()
        opts.sanitize_node(None, None, None, False)
        # TODO Implement sanitize_node and test it

    def test_default_post_process_node_implementation(self):
        """ Test the default ``post_process_node`` method implementation. """
        opts = TagOptions()
        self.assertTrue(opts.post_process_node(None))

    def test_default_render_html_implementation(self):
        """ Test the default ``render_html`` method implementation. """
        opts = TagOptions()
        with self.assertRaises(NotImplementedError):
            opts.render_html(None, '', custom_value='foobar')

    def test_default_render_text_implementation(self):
        """ Test the default ``render_text`` method implementation. """
        opts = TagOptions()
        with self.assertRaises(NotImplementedError):
            opts.render_text(None, '', custom_value='foobar')

    def test_default_render_skcode_implementation(self):
        """ Test the default ``render_skcode`` method implementation. """
        opts = TagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output = opts.render_skcode(tree_node, 'Hello world!')
        expected_output = '[test]Hello world![/test]'
        self.assertEqual(expected_output, output)

    def test_default_render_skcode_implementation_standalone(self):
        """ Test the default ``render_skcode`` method implementation with a standalone tag. """
        opts = TagOptions(standalone=True)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output = opts.render_skcode(tree_node, '')
        expected_output = '[test]'
        self.assertEqual(expected_output, output)

    def test_default_get_skcode_tag_name(self):
        """ Test the default ``get_skcode_tag_name`` method implementation. """
        opts = TagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('test', opts.get_skcode_tag_name(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_attributes(self):
        """ Test the default ``get_skcode_attributes`` method implementation. """
        opts = TagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual(({}, None), opts.get_skcode_attributes(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_non_ignored_empty_attributes(self):
        """ Test the default ``get_skcode_non_ignored_empty_attributes`` method implementation. """
        opts = TagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual((), opts.get_skcode_non_ignored_empty_attributes(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_inner_content(self):
        """ Test the default ``get_skcode_inner_content`` method implementation. """
        opts = TagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('foo', opts.get_skcode_inner_content(tree_node, 'foo', custom_value='bar'))


class WrappingTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``WrappingTagOptions`` class. """

    def test_constructor_assertion(self):
        """ Test assertions at ``__init__`` """
        with self.assertRaises(AssertionError) as e:
            WrappingTagOptions(None)
        self.assertEqual('The wrapping format string is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            WrappingTagOptions('test')
        self.assertEqual('The wrapping format string must contain %s for inner content place holding.',
                         str(e.exception))

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
        """ Test if the wrapping format is correctly set by the constructor. """
        opts = WrappingTagOptions('foo %s bar')
        self.assertEqual('foo %s bar', opts.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = WrappingTagOptions('foo %s bar')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_html(tree_node, 'wrapped')
        self.assertEqual('foo wrapped bar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = WrappingTagOptions('foo %s bar')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_text(tree_node, 'wrapped')
        self.assertEqual('wrapped', output_result)


class InlineWrappingTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``InlineWrappingTagOptions`` class. """

    def test_subclassing(self):
        """ Test the ``InlineWrappingTagOptions`` super class. """
        self.assertTrue(issubclass(InlineWrappingTagOptions, WrappingTagOptions))

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
