"""
SkCode auto paragraphs utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         NewlineTagOptions,
                         TextTagOptions,
                         TagOptions)
from skcode.utility.paragraphs import (PARAGRAPH_NODE_NAME,
                                       ParagraphTagOptions,
                                       make_paragraphs)


class CustomBlockTagOptions(TagOptions):
    """ Custom subclass of ``TagOptions`` for tests. """


class CustomParagraphTagOptions(ParagraphTagOptions):
    """ Custom subclass of ``ParagraphTagOptions`` for tests. """


class ParagraphTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the ``ParagraphTagOptions`` class. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ParagraphTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('text-justify', opts.html_text_class)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = ParagraphTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('<p class="text-justify">Hello world!</p>\n', opts.render_html(tree_node, 'Hello world!'))

    def test_render_html_custom_css(self):
        """ Test the ``render_html`` method. """
        opts = ParagraphTagOptions(html_text_class='custom_css')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('<p class="custom_css">Hello world!</p>\n', opts.render_html(tree_node, 'Hello world!'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = ParagraphTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('Hello world!\n\n', opts.render_text(tree_node, '  Hello world!   '))

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = ParagraphTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts)
        self.assertEqual('Hello world!\n\n', opts.render_skcode(tree_node, '   Hello world!  '))


class ParagraphsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the paragraphs utility module. """

    def test_module_constants(self):
        """ Test the module level constants. """
        self.assertEqual('_paragraph', PARAGRAPH_NODE_NAME)

    def test_make_paragraphs(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        c = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        d = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 1)
        self.assertTrue(isinstance(root_tree_node.children[0].opts, ParagraphTagOptions))
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_custom_class(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        c = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        d = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node, paragraph_node_opts=CustomParagraphTagOptions())
        self.assertEqual(len(root_tree_node.children), 1)
        print(repr(root_tree_node.children[0].opts))
        self.assertTrue(isinstance(root_tree_node.children[0].opts, CustomParagraphTagOptions))
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_ignore_empty_lines(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        root_tree_node.new_child('_text', TextTagOptions(), content='')
        root_tree_node.new_child('_text', TextTagOptions(), content='     ')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        c = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        d = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 1)
        self.assertTrue(isinstance(root_tree_node.children[0].opts, ParagraphTagOptions))
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_multiple_newlines(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        root_tree_node.new_child('_newline', NewlineTagOptions())
        c = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        d = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 2)
        self.assertTrue(isinstance(root_tree_node.children[0].opts, ParagraphTagOptions))
        self.assertEqual([a, b], root_tree_node.children[0].children)
        self.assertTrue(isinstance(root_tree_node.children[1].opts, ParagraphTagOptions))
        self.assertEqual([c, d], root_tree_node.children[1].children)

    def test_make_paragraphs_trailing_newline(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        z = root_tree_node.new_child('_newline', NewlineTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 2)
        self.assertEqual(root_tree_node.children[0], z)
        self.assertTrue(isinstance(root_tree_node.children[1].opts, ParagraphTagOptions))
        self.assertEqual([a, b], root_tree_node.children[1].children)

    def test_make_paragraphs_mixed_inline_block(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode(RootTagOptions())
        a = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        b = root_tree_node.new_child('_newline', NewlineTagOptions())
        z = root_tree_node.new_child('block', CustomBlockTagOptions())
        c = root_tree_node.new_child('_text', TextTagOptions(), content='Text 1')
        d = root_tree_node.new_child('_newline', NewlineTagOptions())
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 3)
        self.assertTrue(isinstance(root_tree_node.children[0].opts, ParagraphTagOptions))
        self.assertEqual([a, b], root_tree_node.children[0].children)
        self.assertEqual(root_tree_node.children[1], z)
        self.assertTrue(isinstance(root_tree_node.children[2].opts, ParagraphTagOptions))
        self.assertEqual([c, d], root_tree_node.children[2].children)
