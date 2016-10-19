"""
SkCode auto paragraphs utility test code.
"""

import unittest

from skcode.etree import RootTreeNode, TreeNode
from skcode.tags import (
    NewlineTreeNode,
    TextTreeNode
)
from skcode.utility.paragraphs import (
    ParagraphTreeNode,
    make_paragraphs
)


class CustomBlockTreeNode(TreeNode):
    """ Custom subclass of ``TreeNode`` for tests. """

    canonical_tag_name = 'test'
    alias_tag_names = ()


class CustomParagraphTreeNode(ParagraphTreeNode):
    """ Custom subclass of ``ParagraphTreeNode`` for tests. """

    html_text_class = 'custom_css'


class ParagraphTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the ``ParagraphTreeNode`` class. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(ParagraphTreeNode.newline_closes)
        self.assertFalse(ParagraphTreeNode.same_tag_closes)
        self.assertFalse(ParagraphTreeNode.standalone)
        self.assertTrue(ParagraphTreeNode.parse_embedded)
        self.assertFalse(ParagraphTreeNode.inline)
        self.assertTrue(ParagraphTreeNode.close_inlines)
        self.assertFalse(ParagraphTreeNode.make_paragraphs_here)
        self.assertEqual('text-justify', ParagraphTreeNode.html_text_class)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', ParagraphTreeNode)
        self.assertEqual('<p class="text-justify">Hello world!</p>\n', tree_node.render_html('Hello world!'))

    def test_render_html_custom_css(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', CustomParagraphTreeNode)
        self.assertEqual('<p class="custom_css">Hello world!</p>\n', tree_node.render_html('Hello world!'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', ParagraphTreeNode)
        self.assertEqual('Hello world!\n\n', tree_node.render_text('  Hello world!   '))


class ParagraphsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the paragraphs utility module. """

    def test_make_paragraphs(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        c = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        d = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 1)
        self.assertIsInstance(root_tree_node.children[0], ParagraphTreeNode)
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_custom_class(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        c = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        d = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node, paragraph_node_cls=CustomParagraphTreeNode)
        self.assertEqual(len(root_tree_node.children), 1)
        self.assertIsInstance(root_tree_node.children[0], CustomParagraphTreeNode)
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_ignore_empty_lines(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        root_tree_node.new_child(None, TextTreeNode, content='')
        root_tree_node.new_child(None, TextTreeNode, content='     ')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        c = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        d = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 1)
        self.assertIsInstance(root_tree_node.children[0], ParagraphTreeNode)
        self.assertEqual([a, b, c, d], root_tree_node.children[0].children)

    def test_make_paragraphs_multiple_newlines(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        root_tree_node.new_child(None, NewlineTreeNode)
        c = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        d = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 2)
        self.assertIsInstance(root_tree_node.children[0], ParagraphTreeNode)
        self.assertEqual([a, b], root_tree_node.children[0].children)
        self.assertIsInstance(root_tree_node.children[1], ParagraphTreeNode)
        self.assertEqual([c, d], root_tree_node.children[1].children)

    def test_make_paragraphs_trailing_newline(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        z = root_tree_node.new_child(None, NewlineTreeNode)
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 2)
        self.assertEqual(root_tree_node.children[0], z)
        self.assertIsInstance(root_tree_node.children[1], ParagraphTreeNode)
        self.assertEqual([a, b], root_tree_node.children[1].children)

    def test_make_paragraphs_mixed_inline_block(self):
        """ Test the ``make_paragraphs`` paragraph utility. """
        root_tree_node = RootTreeNode()
        a = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        b = root_tree_node.new_child(None, NewlineTreeNode)
        z = root_tree_node.new_child('block', CustomBlockTreeNode)
        c = root_tree_node.new_child(None, TextTreeNode, content='Text 1')
        d = root_tree_node.new_child(None, NewlineTreeNode)
        make_paragraphs(root_tree_node)
        self.assertEqual(len(root_tree_node.children), 3)
        self.assertIsInstance(root_tree_node.children[0], ParagraphTreeNode)
        self.assertEqual([a, b], root_tree_node.children[0].children)
        self.assertEqual(root_tree_node.children[1], z)
        self.assertIsInstance(root_tree_node.children[2], ParagraphTreeNode)
        self.assertEqual([c, d], root_tree_node.children[2].children)
