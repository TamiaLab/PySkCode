"""
SkCode links tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import TreeNode
from skcode.tags import (UrlLinkTagOptions,
                         EmailLinkTagOptions,
                         AnchorTagOptions,
                         GoToAnchorTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


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
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        self.assertTrue(opts.is_url_inside_tag_content(tree_node))

    def test_is_url_inside_tag_content_with_attribute(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        self.assertFalse(opts.is_url_inside_tag_content(tree_node))

    def test_get_target_link_with_tagname_set(self):
        """ Test the ``get_target_link`` when the tag name attribute is set. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_link_in_content(self):
        """ Test the ``get_target_link`` when the tag name attribute is not set (use content instead). """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_no_link(self):
        """ Test the ``get_target_link`` when no link is provided. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts)
        url_link = opts.get_target_link(tree_node)
        self.assertEqual('', url_link)

    def test_get_target_link_call_sanitize_url(self):
        """ Test if the ``get_target_link`` call the ``sanitize_url`` method on the url. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock:
            opts.get_target_link(tree_node)
        mock.assert_called_once_with('http://example.com/')

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Link to the example.com website.')
        expected_result = '<a href="http://example.com/" rel="nofollow">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_html(tree_node, 'Link to the example.com website.', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_link_only(self):
        """ Test the ``render_html`` method with only a link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<a href="http://example.com/" rel="nofollow">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_link_only(self):
        """ Test the ``render_html`` method with only a link and force_nofollow disabled. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        output_result = opts.render_html(tree_node, 'test', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_link(self):
        """ Test the ``render_html`` method with no link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_text(tree_node, 'Link to the example.com website.')
        expected_result = 'Link to the example.com website. (http://example.com/)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_link_only(self):
        """ Test the ``render_text`` method with only a link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'http://example.com/'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_link(self):
        """ Test the ``render_text`` method with no link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={})
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={'url': 'http://example.com/'})
        output_result = opts.render_skcode(tree_node, 'Link to the example.com website.')
        expected_result = '[url="http://example.com/"]Link to the example.com website.[/url]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_link_only(self):
        """ Test the ``render_skcode`` method with only a link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='http://example.com/')
        output_result = opts.render_skcode(tree_node, 'test')
        expected_result = '[url]http://example.com/[/url]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_no_link(self):
        """ Test the ``render_skcode`` method with no link. """
        opts = UrlLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={})
        output_result = opts.render_skcode(tree_node, '')
        expected_result = ''
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
        tree_node = TreeNode(None, 'email', opts, content='john.doe@example.com')
        self.assertTrue(opts.is_email_inside_tag_content(tree_node))

    def test_is_email_inside_tag_content_with_attribute(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        self.assertFalse(opts.is_email_inside_tag_content(tree_node))

    def test_get_email_address_with_tagname_set(self):
        """ Test the ``get_email_address`` when the tag name attribute is set. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_email_in_content(self):
        """ Test the ``get_email_address`` when the tag name attribute is not set (use content instead). """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, content='john.doe@example.com')
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_no_email(self):
        """ Test the ``get_email_address`` when no email is provided. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts)
        email_address = opts.get_email_address(tree_node)
        self.assertEqual('', email_address)

    def test_get_email_address_call_sanitize_url(self):
        """ Test if the ``get_email_address`` call the ``sanitize_url`` method on the url. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock:
            opts.get_email_address(tree_node)
        mock.assert_called_once_with('john.doe@example.com',
                                     default_scheme='mailto',
                                     allowed_schemes=('mailto', ),
                                     force_remove_scheme=True,
                                     fix_non_local_urls=False)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_html(tree_node, 'Mail of John Doe.')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_html(tree_node, 'Mail of John Doe.', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_email_only(self):
        """ Test the ``render_html`` method with only a email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, content='john.doe@example.com')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_email_only(self):
        """ Test the ``render_html`` method with only a email and force_nofollow disabled. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, content='john.doe@example.com')
        output_result = opts.render_html(tree_node, 'test', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_email(self):
        """ Test the ``render_html`` method with no email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_text(tree_node, 'Mail of John Doe.')
        expected_result = 'Mail of John Doe. (<john.doe@example.com>)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_email_only(self):
        """ Test the ``render_text`` method with only a email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, content='john.doe@example.com')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = '<john.doe@example.com>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_email(self):
        """ Test the ``render_text`` method with no email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={})
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, attrs={'email': 'john.doe@example.com'})
        output_result = opts.render_skcode(tree_node, 'Mail of John Doe.')
        expected_result = '[email="john.doe@example.com"]Mail of John Doe.[/email]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_email_only(self):
        """ Test the ``render_skcode`` method with only a email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'email', opts, content='john.doe@example.com')
        output_result = opts.render_skcode(tree_node, 'test')
        expected_result = '[email]john.doe@example.com[/email]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_with_no_email(self):
        """ Test the ``render_skcode`` method with no email. """
        opts = EmailLinkTagOptions()
        tree_node = TreeNode(None, 'url', opts, attrs={})
        output_result = opts.render_skcode(tree_node, '')
        expected_result = ''
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
        tree_node = TreeNode(None, 'anchor', opts, content='test')
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts, content='test')
        with unittest.mock.patch('skcode.tags.links.slugify') as mock:
            opts.get_anchor_id(tree_node)
        mock.assert_called_once_with('test')

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts, content='test')
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<a id="test"></a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts)
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts, content='test')
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = '[#test]'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts)
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts, content='test')
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[anchor]test[/anchor]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_without_anchor_id(self):
        """ Test the ``render_skcode`` method without any anchor ID. """
        opts = AnchorTagOptions()
        tree_node = TreeNode(None, 'anchor', opts)
        output_result = opts.render_skcode(tree_node, 'Hello World!')
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
        tree_node = TreeNode(None, 'goto', opts, attrs={'goto': 'test'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_tagname_and_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test', 'goto': 'test2'})
        anchor_id = opts.get_anchor_id(tree_node)
        self.assertEqual('test2', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.links.slugify') as mock:
            opts.get_anchor_id(tree_node)
        mock.assert_called_once_with('test')

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test'})
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = '<a href="#test">Hello World!</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts)
        output_result = opts.render_html(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test'})
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World! (#test)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts)
        output_result = opts.render_text(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts, attrs={'id': 'test'})
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = '[goto id="test"]Hello World![/goto]'
        self.assertEqual(expected_result, output_result)

    def test_render_skcode_without_anchor_id(self):
        """ Test the ``render_skcode`` method without any anchor ID. """
        opts = GoToAnchorTagOptions()
        tree_node = TreeNode(None, 'goto', opts)
        output_result = opts.render_skcode(tree_node, 'Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)
