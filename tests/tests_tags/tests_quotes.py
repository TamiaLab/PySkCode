"""
SkCode quotes tag test code.
"""

import unittest
from unittest import mock

from datetime import datetime

from skcode.etree import TreeNode
from skcode.tags import (QuoteTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class QuotesTagTestCase(unittest.TestCase):
    """ Tests suite for the quotes tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('quote', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['quote'], QuoteTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = QuoteTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual(opts.author_attr_name, 'author')
        self.assertEqual(opts.link_attr_name, 'link')
        self.assertEqual(opts.date_attr_name, 'date')
        self.assertEqual(opts.write_by_word, 'par')
        self.assertEqual(opts.datetime_format, '%d/%m/%Y %H:%M:%S')

    def test_get_quote_author_name_with_tagname_set(self):
        """ Test the ``get_quote_author_name`` when the tag name attribute is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'quote': 'test'})
        author_name = opts.get_quote_author_name(tree_node)
        self.assertEqual('test', author_name)

    def test_get_quote_author_name_with_author_set(self):
        """ Test the ``get_quote_author_name`` when the "author" attribute is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'test'})
        author_name = opts.get_quote_author_name(tree_node)
        self.assertEqual('test', author_name)

    def test_get_quote_author_name_with_tagname_and_author_set(self):
        """ Test the ``get_quote_author_name`` when the tag name and "author" attribute is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'test', 'quote': 'test2'})
        author_name = opts.get_quote_author_name(tree_node)
        self.assertEqual('test2', author_name)

    def test_get_quote_author_name_with_no_value_set(self):
        """ Test the ``get_quote_author_name`` when no value is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        author_name = opts.get_quote_author_name(tree_node)
        self.assertEqual('', author_name)

    def test_get_quote_author_name_with_html_entities(self):
        """ Test the ``get_quote_author_name`` when author name contain HTML entities. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': '&lt;test&gt;'})
        author_name = opts.get_quote_author_name(tree_node)
        self.assertEqual('<test>', author_name)

    def test_get_quote_link(self):
        """ Test the ``get_quote_link`` when the "link" attribute is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'link': 'https://github.com/TamiaLab/PySkCode'})
        src_link = opts.get_quote_link(tree_node)
        self.assertEqual('https://github.com/TamiaLab/PySkCode', src_link)

    def test_get_quote_link_without_value(self):
        """ Test the ``get_quote_link`` when the "link" attribute is not set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        src_link = opts.get_quote_link(tree_node)
        self.assertEqual('', src_link)

    def test_get_quote_link_call_sanitize_url(self):
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'link': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.quotes.sanitize_url') as mock:
            opts.get_quote_link(tree_node)
        mock.assert_called_once_with('https://github.com/TamiaLab/PySkCode')

    def test_get_quote_date(self):
        """ Test the ``get_quote_date`` when the "date" attribute is set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'date': '1356048000'})
        src_date = opts.get_quote_date(tree_node)
        self.assertEqual(datetime(2012, 12, 21, 0, 0), src_date)

    def test_get_quote_date_no_value(self):
        """ Test the ``get_quote_date`` when the "date" attribute is not set. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        src_date = opts.get_quote_date(tree_node)
        self.assertIsNone(src_date)

    def test_get_quote_date_with_non_number(self):
        """ Test the ``get_quote_date`` when the "date" attribute value is not valid. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'date': 'azerty'})
        src_date = opts.get_quote_date(tree_node)
        self.assertIsNone(src_date)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<blockquote>Hello World!</blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_author_name(self):
        """ Test the ``render_html`` method with an author name. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<blockquote>Hello World!\n<small>par <cite>John Doe</cite></small></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_author_name_containing_html_entities(self):
        """ Test the ``render_html`` method with an author name containing HTML entities. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': '<John Doe>'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<blockquote>Hello World!\n<small>par <cite>&lt;John Doe&gt;</cite></small></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link(self):
        """ Test the ``render_html`` method with a source link. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<blockquote>Hello World!\n<small>par <a href="http://example.com/" rel="nofollow"><cite>John Doe</cite></a></small></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link_nofollow_disabled(self):
        """ Test the ``render_html`` method with a source link and force_nofollow option disabled. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Hello World!', force_rel_nofollow=False)
        expected_result = '<blockquote>Hello World!\n<small>par <a href="http://example.com/"><cite>John Doe</cite></a></small></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_date(self):
        """ Test the ``render_html`` method with a source date. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/',
                                                         'date': '1356048000'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<blockquote>Hello World!\n<small>par <a href="http://example.com/" rel="nofollow"><cite>John Doe</cite></a> - <time datetime="2012-12-21T00:00:00">21/12/2012 00:00:00</time></small></blockquote>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '> Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_author_name(self):
        """ Test the ``render_text`` method with an author name. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '> Hello World!\n>\n> -- par John Doe\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link(self):
        """ Test the ``render_text`` method with a source link. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '> Hello World!\n>\n> -- par John Doe (http://example.com/)\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_date(self):
        """ Test the ``render_text`` method with a source date. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/',
                                                         'date': '1356048000'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '> Hello World!\n>\n> -- par John Doe (http://example.com/) - 21/12/2012 00:00:00\n'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[quote]Hello World![/quote]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_author_name(self):
        """ Test the ``render_skcode`` method with an author name. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[quote author="John Doe"]Hello World![/quote]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_src_link(self):
        """ Test the ``render_skcode`` method with a source link. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[quote author="John Doe" link="http://example.com/"]Hello World![/quote]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_src_date(self):
        """ Test the ``render_skcode`` method a source date. """
        opts = QuoteTagOptions()
        tree_node = TreeNode(None, 'quote', opts, attrs={'author': 'John Doe',
                                                         'link': 'http://example.com/',
                                                         'date': '1356048000'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[quote author="John Doe" link="http://example.com/" date="1356048000"]Hello World![/quote]'
        self.assertEqual(expected_result, output_result)
