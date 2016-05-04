"""
SkCode base tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TagOptions,
                         WrappingTagOptions,
                         InlineWrappingTagOptions)


class TestTagOptions(TagOptions):
    """ Test tag declaration class """

    canonical_tag_name = 'test'


class TagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``TagOptions`` base class. """

    def test_no_canonical_name_set_error(self):
        """ Test the constructor of the tag options class """
        with self.assertRaises(AssertionError) as e:
            opts = TagOptions()
            self.assertIsNone(opts)
        self.assertEqual('Canonical tag name is mandatory', str(e.exception))

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TestTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.weak_parent_close)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('test', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)

    def test_init_kwargs_setter(self):
        """ Test modification of constants at constructor. """
        opts = TestTagOptions(newline_closes=True)
        self.assertTrue(opts.newline_closes)
        opts = TestTagOptions(same_tag_closes=True)
        self.assertTrue(opts.same_tag_closes)
        opts = TestTagOptions(standalone=True)
        self.assertTrue(opts.standalone)
        opts = TestTagOptions(parse_embedded=False)
        self.assertFalse(opts.parse_embedded)
        opts = TestTagOptions(swallow_trailing_newline=True)
        self.assertTrue(opts.swallow_trailing_newline)
        opts = TestTagOptions(inline=True)
        self.assertTrue(opts.inline)
        opts = TestTagOptions(close_inlines=False)
        self.assertFalse(opts.close_inlines)
        opts = TestTagOptions(canonical_tag_name='foobar')
        self.assertEqual('foobar', opts.canonical_tag_name)
        opts = TestTagOptions(alias_tag_names=('foo', 'bar'))
        self.assertEqual(('foo', 'bar'), opts.alias_tag_names)
        opts = TestTagOptions(make_paragraphs_here=True)
        self.assertTrue(opts.make_paragraphs_here)
        opts = TestTagOptions(custom_value='foobar')
        self.assertEqual('foobar', getattr(opts, 'custom_value'))

    def test_default_sanitize_node_policy(self):
        """ Test the default ``sanitize_node`` method policy. """
        opts = TestTagOptions()
        opts.sanitize_node(None, None, None, False)
        self.assertTrue(True)
        # TODO Implement sanitize_node and test it

    def test_default_post_process_node_implementation(self):
        """ Test the default ``post_process_node`` method implementation. """
        opts = TestTagOptions()
        self.assertTrue(opts.post_process_node(None))

    def test_default_render_html_implementation(self):
        """ Test the default ``render_html`` method implementation. """
        opts = TestTagOptions()
        with self.assertRaises(NotImplementedError) as e:
            opts.render_html(None, '', custom_value='foobar')
        self.assertEqual('render_html() need to be implemented in subclass', str(e.exception))

    def test_default_render_text_implementation(self):
        """ Test the default ``render_text`` method implementation. """
        opts = TestTagOptions()
        with self.assertRaises(NotImplementedError) as e:
            opts.render_text(None, '', custom_value='foobar')
        self.assertEqual('render_text() need to be implemented in subclass', str(e.exception))

    def test_default_render_skcode_implementation(self):
        """ Test the default ``render_skcode`` method implementation. """
        opts = TestTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output = opts.render_skcode(tree_node, 'Hello world!')
        expected_output = '[test]Hello world![/test]'
        self.assertEqual(expected_output, output)

    def test_default_render_skcode_implementation_standalone(self):
        """ Test the default ``render_skcode`` method implementation with a standalone tag. """
        opts = TestTagOptions(standalone=True)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output = opts.render_skcode(tree_node, '')
        expected_output = '[test]'
        self.assertEqual(expected_output, output)

    def test_default_get_skcode_tag_name(self):
        """ Test the default ``get_skcode_tag_name`` method implementation. """
        opts = TestTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('test', opts.get_skcode_tag_name(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_tag_name_canonical(self):
        """ Test the default ``get_skcode_tag_name`` method implementation. """
        opts = TestTagOptions(alias_tag_names=('foobar', ))
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('foobar', opts)
        self.assertEqual('test', opts.get_skcode_tag_name(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_tag_name_fallback(self):
        """ Test the default ``get_skcode_tag_name`` method implementation. """
        opts = TestTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('unknown', opts)
        self.assertEqual('unknown', opts.get_skcode_tag_name(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_attributes(self):
        """ Test the default ``get_skcode_attributes`` method implementation. """
        opts = TestTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual(({}, None), opts.get_skcode_attributes(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_non_ignored_empty_attributes(self):
        """ Test the default ``get_skcode_non_ignored_empty_attributes`` method implementation. """
        opts = TestTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual((), opts.get_skcode_non_ignored_empty_attributes(tree_node, 'foo', custom_value='bar'))

    def test_default_get_skcode_inner_content(self):
        """ Test the default ``get_skcode_inner_content`` method implementation. """
        opts = TestTagOptions()
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
        opts = WrappingTagOptions('%s', canonical_tag_name='dummy')
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
        opts = WrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        self.assertEqual('foo %s bar', opts.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = WrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_html(tree_node, 'wrapped')
        self.assertEqual('foo wrapped bar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = WrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_text(tree_node, 'wrapped')
        self.assertEqual('wrapped', output_result)


class InlineWrappingTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``InlineWrappingTagOptions`` class. """

    def test_constructor_assertion(self):
        """ Test assertions at ``__init__`` """
        with self.assertRaises(AssertionError) as e:
            InlineWrappingTagOptions(None)
        self.assertEqual('The wrapping format string is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            InlineWrappingTagOptions('test')
        self.assertEqual('The wrapping format string must contain %s for inner content place holding.',
                         str(e.exception))

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = InlineWrappingTagOptions('%s', canonical_tag_name='dummy')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_wrapping_format_set(self):
        """ Test if the wrapping format is correctly set by the constructor. """
        opts = InlineWrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        self.assertEqual('foo %s bar', opts.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = InlineWrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_html(tree_node, 'wrapped')
        self.assertEqual('foo wrapped bar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = InlineWrappingTagOptions('foo %s bar', canonical_tag_name='dummy')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        output_result = opts.render_text(tree_node, 'wrapped')
        self.assertEqual('wrapped', output_result)
