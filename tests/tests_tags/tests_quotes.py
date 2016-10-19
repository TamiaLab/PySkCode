"""
SkCode quote tag definitions test code.
"""

import unittest
from unittest import mock

from datetime import datetime

from skcode.etree import RootTreeNode
from skcode.tags import (
    QuoteTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class QuotesTagTestCase(unittest.TestCase):
    """ Tests suite for the quotes tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(QuoteTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(QuoteTreeNode.newline_closes)
        self.assertFalse(QuoteTreeNode.same_tag_closes)
        self.assertFalse(QuoteTreeNode.standalone)
        self.assertTrue(QuoteTreeNode.parse_embedded)
        self.assertFalse(QuoteTreeNode.inline)
        self.assertTrue(QuoteTreeNode.close_inlines)
        self.assertEqual('quote', QuoteTreeNode.canonical_tag_name)
        self.assertEqual(('blockquote', ), QuoteTreeNode.alias_tag_names)
        self.assertTrue(QuoteTreeNode.make_paragraphs_here)
        self.assertEqual(QuoteTreeNode.author_attr_name, 'author')
        self.assertEqual(QuoteTreeNode.link_attr_name, 'link')
        self.assertEqual(QuoteTreeNode.date_attr_name, 'date')
        self.assertEqual(QuoteTreeNode.datetime_format, '%d/%m/%Y %H:%M:%S')

    def test_get_quote_author_name_with_tagname_set(self):
        """ Test the ``get_quote_author_name`` when the tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'quote': 'test'})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('test', author_name)

    def test_get_quote_author_name_with_author_set(self):
        """ Test the ``get_quote_author_name`` when the "author" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': 'test'})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('test', author_name)

    def test_get_quote_author_name_with_tagname_and_author_set(self):
        """ Test the ``get_quote_author_name`` when the tag name and "author" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'quote': 'test', 'author': 'test2'})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('test', author_name)

    def test_get_quote_author_name_with_no_value_set(self):
        """ Test the ``get_quote_author_name`` when no value is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('', author_name)

    def test_get_quote_author_name_with_html_entities(self):
        """ Test the ``get_quote_author_name`` when author name contain HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': '<test>'})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('<test>', author_name)

    def test_get_quote_author_name_with_encoded_html_entities(self):
        """ Test the ``get_quote_author_name`` when author name contain encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': '&lt;test&gt;'})
        author_name = tree_node.get_quote_author_name()
        self.assertEqual('<test>', author_name)

    def test_get_quote_link(self):
        """ Test the ``get_quote_link`` when the "link" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'link': 'https://github.com/TamiaLab/PySkCode'})
        src_link = tree_node.get_quote_link()
        self.assertEqual('https://github.com/TamiaLab/PySkCode', src_link)

    def test_get_quote_link_without_value(self):
        """ Test the ``get_quote_link`` when the "link" attribute is not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={})
        src_link = tree_node.get_quote_link()
        self.assertEqual('', src_link)

    def test_get_quote_link_call_sanitize_url(self):
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'link': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.quotes.sanitize_url') as mock_sanitize_url:
            tree_node.get_quote_link()
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='')

    def test_get_quote_link_call_sanitize_url_with_relative_url_conversion(self):
        root_tree_node = RootTreeNode()
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'link': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.quotes.sanitize_url') as mock_sanitize_url:
            tree_node.get_quote_link()
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='http://example.com/')

    def test_get_quote_date(self):
        """ Test the ``get_quote_date`` when the "date" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'date': '1356048000'})
        src_date = tree_node.get_quote_date()
        self.assertEqual(datetime(2012, 12, 21, 0, 0), src_date)

    def test_get_quote_date_no_value(self):
        """ Test the ``get_quote_date`` when the "date" attribute is not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={})
        src_date = tree_node.get_quote_date()
        self.assertIsNone(src_date)

    def test_get_quote_date_with_non_number(self):
        """ Test the ``get_quote_date`` when the "date" attribute value is not valid. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'date': 'azerty'})
        src_date = tree_node.get_quote_date()
        self.assertIsNone(src_date)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<blockquote>Hello World!</blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_author_name(self):
        """ Test the ``render_html`` method with an author name. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': 'John Doe'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<blockquote>Hello World!\n<footer><cite>John Doe</cite></footer></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_author_name_containing_html_entities(self):
        """ Test the ``render_html`` method with an author name containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': '<John Doe>'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<blockquote>Hello World!\n<footer><cite>&lt;John Doe&gt;</cite></footer></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link(self):
        """ Test the ``render_html`` method with a source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'author': 'John Doe', 'link': 'http://example.com/'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<blockquote>Hello World!\n<footer><a href="http://example.com/" ' \
                          'rel="nofollow"><cite>John Doe</cite></a></footer></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link_nofollow_disabled(self):
        """ Test the ``render_html`` method with a source link and force_nofollow option disabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'author': 'John Doe', 'link': 'http://example.com/'})
        output_result = tree_node.render_html('Hello World!', force_rel_nofollow=False)
        expected_result = '<blockquote>Hello World!\n<footer><a href="http://example.com/">' \
                          '<cite>John Doe</cite></a></footer></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_date(self):
        """ Test the ``render_html`` method with a source date. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'author': 'John Doe', 'link': 'http://example.com/',
                                                    'date': '1356048000'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<blockquote>Hello World!\n<footer><a href="http://example.com/" ' \
                          'rel="nofollow"><cite>John Doe</cite></a> - <time datetime="2012-12-21T00:00:00">' \
                          '21/12/2012 00:00:00</time></footer></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '> Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_author_name(self):
        """ Test the ``render_text`` method with an author name. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode, attrs={'author': 'John Doe'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '> Hello World!\n>\n> -- John Doe\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link(self):
        """ Test the ``render_text`` method with a source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'author': 'John Doe', 'link': 'http://example.com/'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '> Hello World!\n>\n> -- John Doe (http://example.com/)\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_date(self):
        """ Test the ``render_text`` method with a source date. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('quote', QuoteTreeNode,
                                             attrs={'author': 'John Doe',
                                                    'link': 'http://example.com/', 'date': '1356048000'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = '> Hello World!\n>\n> -- John Doe (http://example.com/) - 21/12/2012 00:00:00\n'
        self.assertEqual(expected_result, output_result)
