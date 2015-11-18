"""
SkCode titles tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import TreeNode
from skcode.tags import (TitleTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TitlesTagTestCase(unittest.TestCase):
    """ Tests suite for the titles tag module. """

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
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual(opts.slug_id_attr_name, 'id')

    def test_constructor(self):
        """ Test if the constructor set the title level and HTML tag name correctly. """
        for level in range(1, 7):
            opts = TitleTagOptions(level)
            self.assertEqual(opts.title_level, level)
            self.assertEqual(opts.title_tagname, 'h%d' % level)

    def test_get_permalink_slug_with_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'h1': 'test'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_set(self):
        """ Test the ``get_permalink_slug`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'id': 'test'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test', permalink_slug)

    def test_get_permalink_slug_with_id_and_tagname_set(self):
        """ Test the ``get_permalink_slug`` when the tag name and "id" attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'h1': 'test2', 'id': 'test'})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('test2', permalink_slug)

    def test_get_permalink_slug_without_value(self):
        """ Test the ``get_permalink_slug`` when no value is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={})
        permalink_slug = opts.get_permalink_slug(tree_node)
        self.assertEqual('', permalink_slug)

    def test_get_permalink_slug_call_slugify(self):
        """ Test the ``get_permalink_slug`` method call the ``slugify`` function. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.titles.slugify') as mock:
            opts.get_permalink_slug(tree_node)
        mock.assert_called_once_with('test')

    def test_render_html_with_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'id': 'test'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<h1><a id="test">Hello World!</a></h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_permalink(self):
        """ Test the ``render_html`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<h1>Hello World!</h1>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'id': 'test'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '#[test] Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_permalink(self):
        """ Test the ``render_text`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '# Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_permalink(self):
        """ Test the ``render_skcode`` when the "id" attribute is set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={'id': 'test'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[h1 id="test"]Hello World![/h1]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_without_permalink(self):
        """ Test the ``render_skcode`` when the "id" attribute is not set. """
        opts = TitleTagOptions(1)
        tree_node = TreeNode(None, 'h1', opts, attrs={})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[h1]Hello World![/h1]'
        self.assertEqual(expected_result, output_result)
