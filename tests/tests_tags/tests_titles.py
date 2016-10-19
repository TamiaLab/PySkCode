"""
SkCode title tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags.titles import TitleBaseTreeNode, generate_title_cls


class TitleTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the titles tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TitleBaseTreeNode.newline_closes)
        self.assertFalse(TitleBaseTreeNode.same_tag_closes)
        self.assertFalse(TitleBaseTreeNode.standalone)
        self.assertTrue(TitleBaseTreeNode.parse_embedded)
        self.assertFalse(TitleBaseTreeNode.inline)
        self.assertTrue(TitleBaseTreeNode.close_inlines)
        self.assertIsNone(TitleBaseTreeNode.canonical_tag_name)
        self.assertEqual((), TitleBaseTreeNode.alias_tag_names)
        self.assertFalse(TitleBaseTreeNode.make_paragraphs_here)
        self.assertEqual('id', TitleBaseTreeNode.slug_id_attr_name)
        self.assertEqual('<{title_tagname}><a id="{slug_id}">{inner_html}</a></{title_tagname}>\n',
                         TitleBaseTreeNode.html_render_template)
        self.assertEqual('{title_level}[{slug_id}] {inner_text}\n', TitleBaseTreeNode.text_render_template)
        self.assertEqual('<{title_tagname}>{inner_html}</{title_tagname}>\n',
                         TitleBaseTreeNode.html_render_no_permalink_template)
        self.assertEqual('{title_level} {inner_text}\n', TitleBaseTreeNode.text_render_no_permalink_template)

    def test_constructor(self):
        """ Test if the constructor set the title level and HTML tag name correctly. """
        for level in range(1, 7):
            opts = generate_title_cls(level)
            self.assertEqual(opts.title_level, level)
            self.assertEqual(opts.html_tagname, 'h%d' % level)
            self.assertEqual('h%d' % level, opts.canonical_tag_name)

    def test_get_permalink_slug_with_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'h1': 'test'})
        permalink_slug = tree_node.get_permalink_slug()
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_set(self):
        """ Test the ``get_permalink_slug`` when the "id" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'id': 'test'})
        permalink_slug = tree_node.get_permalink_slug()
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_and_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name and "id" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'h1': 'test', 'id': 'test2'})
        permalink_slug = tree_node.get_permalink_slug()
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_without_value(self):
        """ Test the ``get_permalink_slug`` when no value is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={})
        permalink_slug = tree_node.get_permalink_slug()
        self.assertEqual('', permalink_slug)

    def test_get_permalink_slug_call_slugify(self):
        """ Test the ``get_permalink_slug`` method call the ``slugify`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.titles.slugify') as mock_slugify:
            tree_node.get_permalink_slug()
        mock_slugify.assert_called_once_with('test')

    def test_render_html_with_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'id': 'test'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<h1><a id="test">Hello World!</a></h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<h1>Hello World!</h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={'id': 'test'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '#[test] Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('h1', generate_title_cls(1), attrs={})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '# Hello World!\n'
        self.assertEqual(expected_result, output_result)
