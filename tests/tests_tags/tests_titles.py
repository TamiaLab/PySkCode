"""
SkCode title tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TitleTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TitleTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the titles tag module. """

    def test_assertions_constructor(self):
        """ Test assertions at ``__init__`` """
        with self.assertRaises(AssertionError) as e:
            TitleTagOptions(0)
        self.assertEqual('Title level must be between zero and 6 (included).', str(e.exception))
        with self.assertRaises(AssertionError) as e:
            TitleTagOptions(7)
        self.assertEqual('Title level must be between zero and 6 (included).', str(e.exception))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('h1', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h1'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h1'].title_level, 1)
        self.assertIn('h2', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h2'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h2'].title_level, 2)
        self.assertIn('h3', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h3'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h3'].title_level, 3)
        self.assertIn('h4', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h4'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h4'].title_level, 4)
        self.assertIn('h5', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h5'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h5'].title_level, 5)
        self.assertIn('h6', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['h6'], TitleTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['h6'].title_level, 6)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TitleTagOptions(1)
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('h1', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('id', opts.slug_id_attr_name)
        self.assertEqual('<{title_tagname}><a id="{slug_id}">{inner_html}</a></{title_tagname}>\n', opts.html_render_template)
        self.assertEqual('{title_level}[{slug_id}] {inner_text}\n', opts.text_render_template)
        self.assertEqual('<{title_tagname}>{inner_html}</{title_tagname}>\n', opts.html_render_no_permalink_template)
        self.assertEqual('{title_level} {inner_text}\n', opts.text_render_no_permalink_template)

    def test_constructor(self):
        """ Test if the constructor set the title level and HTML tag name correctly. """
        for level in range(1, 7):
            opts = TitleTagOptions(level)
            self.assertEqual(opts.title_level, level)
            self.assertEqual(opts.title_tagname, 'h%d' % level)
            self.assertEqual('h%d' % level, opts.canonical_tag_name)

    def test_get_permalink_slug_with_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'h1': 'test'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_set(self):
        """ Test the ``get_permalink_slug`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'id': 'test'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_and_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name and "id" attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'h1': 'test', 'id': 'test2'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_without_value(self):
        """ Test the ``get_permalink_slug`` when no value is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('', permalink_slug)

    def test_get_permalink_slug_call_slugify(self):
        """ Test the ``get_permalink_slug`` method call the ``slugify`` function. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.titles.slugify') as mock_slugify:
            opts.get_permalink_slug(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_render_html_with_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'id': 'test'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<h1><a id="test">Hello World!</a></h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<h1>Hello World!</h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'id': 'test'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '#[test] Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '# Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_permalink(self):
        """ Test the ``get_skcode_attributes`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={'id': 'test'})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'id': 'test'}, 'id')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_without_permalink(self):
        """ Test the ``get_skcode_attributes`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('h1', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'id': ''}, 'id')
        self.assertEqual(expected_result, output_result)
