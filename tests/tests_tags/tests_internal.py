"""
SkCode internal tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (TextTreeNode,
                         NewlineTreeNode,
                         HardNewlineTreeNode)


class TextTagTestCase(unittest.TestCase):
    """ Tests suite for the text tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TextTreeNode.newline_closes)
        self.assertFalse(TextTreeNode.same_tag_closes)
        self.assertFalse(TextTreeNode.standalone)
        self.assertTrue(TextTreeNode.parse_embedded)
        self.assertTrue(TextTreeNode.inline)
        self.assertFalse(TextTreeNode.close_inlines)
        self.assertIsNone(TextTreeNode.canonical_tag_name)
        self.assertEqual((), TextTreeNode.alias_tag_names)
        self.assertFalse(TextTreeNode.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='test')
        output_result = tree_node.render_html('')
        self.assertEqual('test', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='<test>')
        output_result = tree_node.render_html('')
        self.assertEqual('&lt;test&gt;', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='&lt;test&gt;')
        output_result = tree_node.render_html('')
        self.assertEqual('&lt;test&gt;', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='test')
        output_result = tree_node.render_text('')
        self.assertEqual('test', output_result)

    def test_render_text_with_html_entities(self):
        """ Test the ``render_text`` method with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='<test>')
        output_result = tree_node.render_text('')
        self.assertEqual('<test>', output_result)

    def test_render_text_with_encoded_html_entities(self):
        """ Test the ``render_text`` method with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TextTreeNode, content='&lt;test&gt;')
        output_result = tree_node.render_text('')
        self.assertEqual('<test>', output_result)


class NewlineTagTestCase(unittest.TestCase):
    """ Tests suite for the newline tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(NewlineTreeNode.newline_closes)
        self.assertFalse(NewlineTreeNode.same_tag_closes)
        self.assertFalse(NewlineTreeNode.standalone)
        self.assertTrue(NewlineTreeNode.parse_embedded)
        self.assertTrue(NewlineTreeNode.inline)
        self.assertFalse(NewlineTreeNode.close_inlines)
        self.assertIsNone(NewlineTreeNode.canonical_tag_name)
        self.assertEqual((), NewlineTreeNode.alias_tag_names)
        self.assertFalse(NewlineTreeNode.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', NewlineTreeNode)
        self.assertEqual('\n', tree_node.render_html(''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', NewlineTreeNode)
        self.assertEqual(' ', tree_node.render_text(''))


class HardNewlineTagTestCase(unittest.TestCase):
    """ Tests suite for the (hard) newline tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(HardNewlineTreeNode.newline_closes)
        self.assertFalse(HardNewlineTreeNode.same_tag_closes)
        self.assertFalse(HardNewlineTreeNode.standalone)
        self.assertTrue(HardNewlineTreeNode.parse_embedded)
        self.assertTrue(HardNewlineTreeNode.inline)
        self.assertFalse(HardNewlineTreeNode.close_inlines)
        self.assertIsNone(HardNewlineTreeNode.canonical_tag_name)
        self.assertEqual((), HardNewlineTreeNode.alias_tag_names)
        self.assertFalse(HardNewlineTreeNode.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', HardNewlineTreeNode)
        self.assertEqual('<br>\n', tree_node.render_html(''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', HardNewlineTreeNode)
        self.assertEqual('\n', tree_node.render_text(''))
