"""
SkCode internal tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TextTagOptions,
                         ErroneousTextTagOptions,
                         NewlineTagOptions,
                         HardNewlineTagOptions)


class RootTagTestCase(unittest.TestCase):
    """ Tests suite for the root tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = RootTagOptions()
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
        opts = RootTagOptions()
        root_tree_node = RootTreeNode(opts)
        output_result = opts.render_html(root_tree_node, 'test')
        self.assertEqual('test', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = RootTagOptions()
        root_tree_node = RootTreeNode(opts)
        output_result = opts.render_text(root_tree_node, 'test')
        self.assertEqual('test', output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = RootTagOptions()
        root_tree_node = RootTreeNode(opts)
        output_result = opts.render_skcode(root_tree_node, 'test')
        self.assertEqual('test', output_result)


class TextTagTestCase(unittest.TestCase):
    """ Tests suite for the text tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TextTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='test')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('test', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='<test>')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('&lt;test&gt;', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='&lt;test&gt;')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('&lt;test&gt;', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='test')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('test', output_result)

    def test_render_text_with_html_entities(self):
        """ Test the ``render_text`` method with HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='<test>')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('<test>', output_result)

    def test_render_text_with_encoded_html_entities(self):
        """ Test the ``render_text`` method with encoded HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='&lt;test&gt;')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('<test>', output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='test')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('test', output_result)

    def test_render_skcode_with_html_entities(self):
        """ Test the ``render_skcode`` method with HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='<test>')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('<test>', output_result)

    def test_render_skcode_with_encoded_html_entities(self):
        """ Test the ``render_skcode`` method with encoded HTML entities. """
        opts = TextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='&lt;test&gt;')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('<test>', output_result)


class ErroneousTextTagTestCase(unittest.TestCase):
    """ Tests suite for the erroneous text tag module. """

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(ErroneousTextTagOptions, TextTagOptions))

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ErroneousTextTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = ErroneousTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='test')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<span style="font-weight: bold; color: red;">test</span>', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        opts = ErroneousTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='<test>')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<span style="font-weight: bold; color: red;">&lt;test&gt;</span>', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        opts = ErroneousTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, content='&lt;test&gt;')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<span style="font-weight: bold; color: red;">&lt;test&gt;</span>', output_result)


class NewlineTagTestCase(unittest.TestCase):
    """ Tests suite for the newline tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = NewlineTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = NewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('\n', opts.render_html(tree_node, ''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = NewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual(' ', opts.render_text(tree_node, ''))

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = NewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('\n', opts.render_skcode(tree_node, ''))


class HardNewlineTagTestCase(unittest.TestCase):
    """ Tests suite for the (hard) newline tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = HardNewlineTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = HardNewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('<br>\n', opts.render_html(tree_node, ''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = HardNewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('\n', opts.render_text(tree_node, ''))

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = HardNewlineTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('\n', opts.render_text(tree_node, ''))
