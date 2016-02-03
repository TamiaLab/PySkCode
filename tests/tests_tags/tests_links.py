"""
SkCode links tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         UrlLinkTagOptions,
                         EmailLinkTagOptions,
                         AnchorTagOptions,
                         GoToAnchorTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class UrlLinksTagTestCase(unittest.TestCase):
    """ Tests suite for the URL links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('url', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['url'], UrlLinkTagOptions)
        self.assertIn('link', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['link'], UrlLinkTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = UrlLinkTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_is_url_inside_tag_content_with_content(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        self.assertTrue(opts.is_url_inside_tag_content(tree_node))

    def test_is_url_inside_tag_content_with_attribute(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        self.assertFalse(opts.is_url_inside_tag_content(tree_node))

    def test_is_url_inside_tag_content_with_attribute_and_content(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts,
                                             attrs={'url': 'http://example.com/'}, content='El website')
        self.assertFalse(opts.is_url_inside_tag_content(tree_node))

    def test_get_target_link_with_tagname_set(self):
        """ Test the ``get_target_link`` when the tag name attribute is set. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_link_in_content(self):
        """ Test the ``get_target_link`` when the tag name attribute is not set (use content instead). """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_link_in_content_trailing_whitespaces(self):
        """ Test the ``get_target_link`` when the tag name attribute is not set (use content instead). """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='  http://example.com/   ')
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_no_link(self):
        """ Test the ``get_target_link`` when no link is provided. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts)
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('', url_link)

    def test_get_target_link_call_sanitize_url(self):
        """ Test if the ``get_target_link`` call the ``sanitize_url`` method on the url. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            opts.get_target_link(tree_node)
        mock_sanitize_url.assert_called_once_with('http://example.com/',
                                                  absolute_base_url='', convert_relative_to_absolute=False)

    def test_get_target_link_call_sanitize_url_with_relative_url_conversion(self):
        """ Test if the ``get_target_link`` call the ``sanitize_url`` method on the url. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            opts.get_target_link(tree_node)
        mock_sanitize_url.assert_called_once_with('http://example.com/',
                                                  absolute_base_url='http://example.com/', convert_relative_to_absolute=True)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Link to the example.com website.')
        expected_result = '<a href="http://example.com/" rel="nofollow">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Link to the example.com website.', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_link_only(self):
        """ Test the ``render_html`` method with only a link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<a href="http://example.com/" rel="nofollow">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_link_only(self):
        """ Test the ``render_html`` method with only a link and force_nofollow disabled. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        output_result = opts.render_html(tree_node, 'test', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_link(self):
        """ Test the ``render_html`` method with no link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_text(tree_node, 'Link to the example.com website.')
        expected_result = 'Link to the example.com website. (http://example.com/)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_link_only(self):
        """ Test the ``render_text`` method with only a link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'http://example.com/'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_link(self):
        """ Test the ``render_text`` method with no link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={})
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.get_skcode_attributes(tree_node, 'Link to the example.com website.')
        expected_result = ({'url': 'http://example.com/'}, 'url')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_link_only(self):
        """ Test the ``get_skcode_attributes`` method with only a link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='http://example.com/')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_no_link(self):
        """ Test the ``get_skcode_attributes`` method with no link. """
        opts = UrlLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)


class EmailLinksTagTestCase(unittest.TestCase):
    """ Tests suite for the email links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('email', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['email'], EmailLinkTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = EmailLinkTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_is_email_inside_tag_content_with_content(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='john.doe@example.com')
        self.assertTrue(opts.is_email_inside_tag_content(tree_node))

    def test_is_email_inside_tag_content_with_attribute(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        self.assertFalse(opts.is_email_inside_tag_content(tree_node))

    def test_is_email_inside_tag_content_with_attribute_and_content(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts,
                                             attrs={'email': 'john.doe@example.com'}, content='El email')
        self.assertFalse(opts.is_email_inside_tag_content(tree_node))

    def test_get_email_address_with_tagname_set(self):
        """ Test the ``get_email_address`` when the tag name attribute is set. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_email_in_content(self):
        """ Test the ``get_email_address`` when the tag name attribute is not set (use content instead). """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='john.doe@example.com')
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_email_in_content_trailing_whitespaces(self):
        """ Test the ``get_email_address`` when the tag name attribute is not set (use content instead). """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='  john.doe@example.com   ')
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_no_email(self):
        """ Test the ``get_email_address`` when no email is provided. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts)
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('', email_address)

    def test_get_email_address_call_sanitize_url(self):
        """ Test if the ``get_email_address`` call the ``sanitize_url`` method on the url. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            opts.get_email_address(tree_node)
        mock_sanitize_url.assert_called_once_with('john.doe@example.com',
                                                  default_scheme='mailto',
                                                  allowed_schemes=('mailto', ),
                                                  force_remove_scheme=True,
                                                  fix_non_local_urls=False)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_html(tree_node, 'Mail of John Doe.')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_html(tree_node, 'Mail of John Doe.', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_email_only(self):
        """ Test the ``render_html`` method with only a email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='john.doe@example.com')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_email_only(self):
        """ Test the ``render_html`` method with only a email and force_nofollow disabled. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='john.doe@example.com')
        output_result = opts.render_html(tree_node, 'test', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_email(self):
        """ Test the ``render_html`` method with no email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_text(tree_node, 'Mail of John Doe.')
        expected_result = 'Mail of John Doe. (<john.doe@example.com>)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_email_only(self):
        """ Test the ``render_text`` method with only a email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, content='john.doe@example.com')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = '<john.doe@example.com>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_email(self):
        """ Test the ``render_text`` method with no email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={})
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.get_skcode_attributes(tree_node, 'Mail of John Doe.')
        expected_result = ({'email': 'john.doe@example.com'}, 'email')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_email_only(self):
        """ Test the ``get_skcode_attributes`` method with only a email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('email', opts, content='john.doe@example.com')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_no_email(self):
        """ Test the ``get_skcode_attributes`` method with no email. """
        opts = EmailLinkTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('url', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)


class AnchorsTagTestCase(unittest.TestCase):
    """ Tests suite for the anchor links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('anchor', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['anchor'], AnchorTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = AnchorTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_get_anchor_id_from_content(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts, content='test')
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts, content='test')
        with unittest.mock.patch('skcode.tags.links.slugify') as mock_slugify:
            opts.get_anchor_id(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts, content='test')
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<a id="test"></a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts)
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts, content='test')
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '[#test]'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts)
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_inner_content(self):
        """ Test the ``get_skcode_inner_content`` method. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts, content='test')
        output_result = opts.get_skcode_inner_content(tree_node, 'Hello World!')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_inner_content_without_anchor_id(self):
        """ Test the ``get_skcode_inner_content`` method without any anchor ID. """
        opts = AnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('anchor', opts)
        output_result = opts.get_skcode_inner_content(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)


class AnchorReferencesTagTestCase(unittest.TestCase):
    """ Tests suite for the anchor references tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('goto', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['goto'], GoToAnchorTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = GoToAnchorTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('id', opts.anchor_id_attr_name)

    def test_get_anchor_id_with_tagname_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'goto': 'test'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'id': 'test'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_tagname_and_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'goto': 'test', 'id': 'test2'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_no_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.links.slugify') as mock_slugify:
            opts.get_anchor_id(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'id': 'test'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<a href="#test">Hello World!</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts)
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'id': 'test'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World! (#test)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts)
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts, attrs={'id': 'test'})
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'id': 'test'}, 'id')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_without_anchor_id(self):
        """ Test the ``get_skcode_attributes`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('goto', opts)
        output_result = opts.get_skcode_attributes(tree_node, 'Hello World!')
        expected_result = ({'id': ''}, 'id')
        self.assertEqual(expected_result, output_result)
