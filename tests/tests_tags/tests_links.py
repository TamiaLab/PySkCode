"""
SkCode links tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (
    UrlLinkTreeNode,
    EmailLinkTreeNode,
    AnchorTreeNode,
    GoToAnchorTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class UrlLinksTagTestCase(unittest.TestCase):
    """ Tests suite for the URL links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(UrlLinkTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(UrlLinkTreeNode.newline_closes)
        self.assertFalse(UrlLinkTreeNode.same_tag_closes)
        self.assertFalse(UrlLinkTreeNode.weak_parent_close)
        self.assertFalse(UrlLinkTreeNode.standalone)
        self.assertTrue(UrlLinkTreeNode.parse_embedded)
        self.assertTrue(UrlLinkTreeNode.inline)
        self.assertFalse(UrlLinkTreeNode.close_inlines)
        self.assertEqual('url', UrlLinkTreeNode.canonical_tag_name)
        self.assertEqual(('link', ), UrlLinkTreeNode.alias_tag_names)
        self.assertFalse(UrlLinkTreeNode.make_paragraphs_here)
        self.assertEqual('nofollow', UrlLinkTreeNode.nofollow_attr_name)
        self.assertEqual('title', UrlLinkTreeNode.title_attr_name)
        self.assertEqual('<a href="{src_link}"{extra_args}>{inner_html}</a>', UrlLinkTreeNode.html_render_template)

    def test_is_url_inside_tag_content_with_content(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='http://example.com/')
        self.assertTrue(tree_node.is_url_inside_tag_content())

    def test_is_url_inside_tag_content_with_attribute(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        self.assertFalse(tree_node.is_url_inside_tag_content())

    def test_is_url_inside_tag_content_with_attribute_and_content(self):
        """ Test if the ``is_url_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/'}, content='El website')
        self.assertFalse(tree_node.is_url_inside_tag_content())

    def test_get_nofollow_flag_with_flag_set(self):
        """ Test the ``get_nofollow_flag`` when the "nofollow" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/',
                                                    'nofollow': ''}, content='El website')
        self.assertTrue(tree_node.get_nofollow_flag())

    def test_get_nofollow_flag_with_flag_not_set(self):
        """ Test the ``get_nofollow_flag`` when the "nofollow" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/'}, content='El website')
        self.assertFalse(tree_node.get_nofollow_flag())

    def test_get_target_link_with_tagname_set(self):
        """ Test the ``get_target_link`` when the tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        url_link = tree_node.get_target_link()
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_link_in_content(self):
        """ Test the ``get_target_link`` when the tag name attribute is not set (use content instead). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='http://example.com/')
        url_link = tree_node.get_target_link()
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_link_in_content_trailing_whitespaces(self):
        """ Test the ``get_target_link`` when the tag name attribute is not set (use content instead). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='  http://example.com/   ')
        url_link = tree_node.get_target_link()
        self.assertEqual('http://example.com/', url_link)

    def test_get_target_link_with_no_link(self):
        """ Test the ``get_target_link`` when no link is provided. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode)
        url_link = tree_node.get_target_link()
        self.assertEqual('', url_link)

    def test_get_target_link_call_sanitize_url(self):
        """ Test if the ``get_target_link`` call the ``sanitize_url`` method on the url. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            tree_node.get_target_link()
        mock_sanitize_url.assert_called_once_with('http://example.com/', absolute_base_url='')

    def test_get_target_link_call_sanitize_url_with_relative_url_conversion(self):
        """ Test if the ``get_target_link`` call the ``sanitize_url`` method on the url. """
        root_tree_node = RootTreeNode()
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            tree_node.get_target_link()
        mock_sanitize_url.assert_called_once_with('http://example.com/',
                                                  absolute_base_url='http://example.com/')

    def test_get_link_title_with_title_set(self):
        """ Test the ``get_title_link`` method when the "title" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/', 'title': 'test'})
        title = tree_node.get_title_link()
        self.assertEqual('test', title)

    def test_get_link_title_with_html_entities(self):
        """ Test the ``get_title_link`` method with a title containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/', 'title': '&lt;test&gt;'})
        title = tree_node.get_title_link()
        self.assertEqual('<test>', title)

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={})
        tree_node.sanitize_node([])
        self.assertEqual('Missing or erroneous target URL', tree_node.error_message)
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        output_result = tree_node.render_html('Link to the example.com website.')
        expected_result = '<a href="http://example.com/" rel="nofollow">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_title(self):
        """ Test the ``render_html`` method with a title set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/', 'title': 'test'})
        output_result = tree_node.render_html('Link to the example.com website.')
        expected_result = '<a href="http://example.com/" rel="nofollow" title="test">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        output_result = tree_node.render_html('Link to the example.com website.', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_title(self):
        """ Test the ``render_html`` method with force_nofollow disabled and a title set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/', 'title': 'test'})
        output_result = tree_node.render_html('Link to the example.com website.', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/" title="test">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_but_forced(self):
        """ Test the ``render_html`` method with force_nofollow disabled but forced by attribute. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'url': 'http://example.com/', 'nofollow': ''})
        output_result = tree_node.render_html('Link to the example.com website.', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/" rel="nofollow">Link to the example.com website.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_link_only(self):
        """ Test the ``render_html`` method with only a link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='http://example.com/')
        output_result = tree_node.render_html('test')
        expected_result = '<a href="http://example.com/" rel="nofollow">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_link_only(self):
        """ Test the ``render_html`` method with only a link and force_nofollow disabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='http://example.com/')
        output_result = tree_node.render_html('test', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_but_forced_and_link_only(self):
        """ Test the ``render_html`` method with only a link and force_nofollow disabled but forced by attribute. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode,
                                             attrs={'nofollow': ''}, content='http://example.com/')
        output_result = tree_node.render_html('test', force_rel_nofollow=False)
        expected_result = '<a href="http://example.com/" rel="nofollow">http://example.com/</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_link(self):
        """ Test the ``render_html`` method with no link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={})
        output_result = tree_node.render_html('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={'url': 'http://example.com/'})
        output_result = tree_node.render_text('Link to the example.com website.')
        expected_result = 'Link to the example.com website. (http://example.com/)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_link_only(self):
        """ Test the ``render_text`` method with only a link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, content='http://example.com/')
        output_result = tree_node.render_text('test')
        expected_result = 'http://example.com/'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_link(self):
        """ Test the ``render_text`` method with no link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', UrlLinkTreeNode, attrs={})
        output_result = tree_node.render_text('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)


class EmailLinksTagTestCase(unittest.TestCase):
    """ Tests suite for the email links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(EmailLinkTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(EmailLinkTreeNode.newline_closes)
        self.assertFalse(EmailLinkTreeNode.same_tag_closes)
        self.assertFalse(EmailLinkTreeNode.weak_parent_close)
        self.assertFalse(EmailLinkTreeNode.standalone)
        self.assertTrue(EmailLinkTreeNode.parse_embedded)
        self.assertTrue(EmailLinkTreeNode.inline)
        self.assertFalse(EmailLinkTreeNode.close_inlines)
        self.assertEqual('email', EmailLinkTreeNode.canonical_tag_name)
        self.assertEqual((), EmailLinkTreeNode.alias_tag_names)
        self.assertFalse(EmailLinkTreeNode.make_paragraphs_here)
        self.assertEqual('<a href="mailto:{email_address}"{extra_args}>{inner_html}</a>',
                         EmailLinkTreeNode.html_render_template)

    def test_is_email_inside_tag_content_with_content(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, content='john.doe@example.com')
        self.assertTrue(tree_node.is_email_inside_tag_content())

    def test_is_email_inside_tag_content_with_attribute(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        self.assertFalse(tree_node.is_email_inside_tag_content())

    def test_is_email_inside_tag_content_with_attribute_and_content(self):
        """ Test if the ``is_email_inside_tag_content`` work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode,
                                             attrs={'email': 'john.doe@example.com'}, content='El email')
        self.assertFalse(tree_node.is_email_inside_tag_content())

    def test_get_email_address_with_tagname_set(self):
        """ Test the ``get_email_address`` when the tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        email_address = tree_node.get_email_address()
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_email_in_content(self):
        """ Test the ``get_email_address`` when the tag name attribute is not set (use content instead). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, content='john.doe@example.com')
        email_address = tree_node.get_email_address()
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_email_in_content_trailing_whitespaces(self):
        """ Test the ``get_email_address`` when the tag name attribute is not set (use content instead). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, content='  john.doe@example.com   ')
        email_address = tree_node.get_email_address()
        self.assertEqual('john.doe@example.com', email_address)

    def test_get_email_address_with_no_email(self):
        """ Test the ``get_email_address`` when no email is provided. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode)
        email_address = tree_node.get_email_address()
        self.assertEqual('', email_address)

    def test_get_email_address_call_sanitize_url(self):
        """ Test if the ``get_email_address`` call the ``sanitize_url`` method on the url. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        with unittest.mock.patch('skcode.tags.links.sanitize_url') as mock_sanitize_url:
            tree_node.get_email_address()
        mock_sanitize_url.assert_called_once_with('john.doe@example.com',
                                                  default_scheme='mailto',
                                                  allowed_schemes=('mailto', ),
                                                  force_remove_scheme=True,
                                                  fix_non_local_urls=False)

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={})
        tree_node.sanitize_node([])
        self.assertEqual('Missing or erroneous target email address', tree_node.error_message)
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        output_result = tree_node.render_html('Mail of John Doe.')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled(self):
        """ Test the ``render_html`` method with force_nofollow disabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        output_result = tree_node.render_html('Mail of John Doe.', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">Mail of John Doe.</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_email_only(self):
        """ Test the ``render_html`` method with only a email. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, content='john.doe@example.com')
        output_result = tree_node.render_html('test')
        expected_result = '<a href="mailto:john.doe@example.com" rel="nofollow">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_nofollow_disabled_and_email_only(self):
        """ Test the ``render_html`` method with only a email and force_nofollow disabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, content='john.doe@example.com')
        output_result = tree_node.render_html('test', force_rel_nofollow=False)
        expected_result = '<a href="mailto:john.doe@example.com">john.doe@example.com</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_email(self):
        """ Test the ``render_html`` method with no email. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={})
        output_result = tree_node.render_html('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={'email': 'john.doe@example.com'})
        output_result = tree_node.render_text('Mail of John Doe.')
        expected_result = 'Mail of John Doe. (<john.doe@example.com>)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_email_only(self):
        """ Test the ``render_text`` method with only a email. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('url', EmailLinkTreeNode, content='john.doe@example.com')
        output_result = tree_node.render_text('test')
        expected_result = '<john.doe@example.com>'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_email(self):
        """ Test the ``render_text`` method with no email. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('email', EmailLinkTreeNode, attrs={})
        output_result = tree_node.render_text('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)


class AnchorsTagTestCase(unittest.TestCase):
    """ Tests suite for the anchor links tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(AnchorTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(AnchorTreeNode.newline_closes)
        self.assertFalse(AnchorTreeNode.same_tag_closes)
        self.assertFalse(AnchorTreeNode.weak_parent_close)
        self.assertFalse(AnchorTreeNode.standalone)
        self.assertTrue(AnchorTreeNode.parse_embedded)
        self.assertTrue(AnchorTreeNode.inline)
        self.assertFalse(AnchorTreeNode.close_inlines)
        self.assertEqual('anchor', AnchorTreeNode.canonical_tag_name)
        self.assertEqual((), AnchorTreeNode.alias_tag_names)
        self.assertFalse(AnchorTreeNode.make_paragraphs_here)
        self.assertEqual('<a id="{anchor_id}"></a>', AnchorTreeNode.html_render_template)

    def test_get_anchor_id_from_content(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        anchor_id = tree_node.get_anchor_id()
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        with unittest.mock.patch('skcode.tags.links.slugify') as mock_slugify:
            tree_node.get_anchor_id()
        mock_slugify.assert_called_once_with('test')

    def test_pre_process_node(self):
        """ Test if the ``pre_process_node`` method mark the node as erroneous when anchor ID is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='')
        tree_node.pre_process_node()
        self.assertEqual('Missing anchor ID', tree_node.error_message)
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        tree_node.pre_process_node()
        self.assertEqual('', tree_node.error_message)
        self.assertEqual({'test'}, root_tree_node.known_ids)
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        tree_node.pre_process_node()
        self.assertEqual('ID already used previously', tree_node.error_message)
        self.assertEqual({'test'}, root_tree_node.known_ids)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<a id="test"></a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode)
        output_result = tree_node.render_html('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode, content='test')
        output_result = tree_node.render_text('Hello World!')
        expected_result = '[#test]'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('anchor', AnchorTreeNode)
        output_result = tree_node.render_text('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)


class AnchorReferencesTagTestCase(unittest.TestCase):
    """ Tests suite for the anchor references tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(GoToAnchorTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(GoToAnchorTreeNode.newline_closes)
        self.assertFalse(GoToAnchorTreeNode.same_tag_closes)
        self.assertFalse(GoToAnchorTreeNode.weak_parent_close)
        self.assertFalse(GoToAnchorTreeNode.standalone)
        self.assertTrue(GoToAnchorTreeNode.parse_embedded)
        self.assertTrue(GoToAnchorTreeNode.inline)
        self.assertFalse(GoToAnchorTreeNode.close_inlines)
        self.assertEqual('goto', GoToAnchorTreeNode.canonical_tag_name)
        self.assertEqual((), GoToAnchorTreeNode.alias_tag_names)
        self.assertFalse(GoToAnchorTreeNode.make_paragraphs_here)
        self.assertEqual('id', GoToAnchorTreeNode.anchor_id_attr_name)
        self.assertEqual('<a href="#{anchor_id}">{inner_html}</a>', GoToAnchorTreeNode.html_render_template)

    def test_get_anchor_id_with_tagname_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'goto': 'test'})
        anchor_id = tree_node.get_anchor_id()
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        anchor_id = tree_node.get_anchor_id()
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_tagname_and_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'goto': 'test', 'id': 'test2'})
        anchor_id = tree_node.get_anchor_id()
        self.assertEqual('test', anchor_id)

    def test_get_anchor_id_with_no_id_set(self):
        """ Test if the ``get_anchor_id`` method work as expected. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={})
        anchor_id = tree_node.get_anchor_id()
        self.assertEqual('', anchor_id)

    def test_get_anchor_id_call_slugify(self):
        """ Test if the ``get_anchor_id`` method call ``slugify`` on the anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.links.slugify') as mock_slugify:
            tree_node.get_anchor_id()
        mock_slugify.assert_called_once_with('test')

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': ''})
        tree_node.sanitize_node([])
        self.assertEqual('Missing anchor ID', tree_node.error_message)
        self.assertEqual(set(), root_tree_node.known_ids)
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        tree_node.sanitize_node([])
        self.assertEqual('Unknown anchor ID', tree_node.error_message)
        root_tree_node.known_ids.add('test')
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        output_result = tree_node.render_html('Hello World!')
        expected_result = '<a href="#test">Hello World!</a>'
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_anchor_id(self):
        """ Test the ``render_html`` method without any anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode)
        output_result = tree_node.render_html('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode, attrs={'id': 'test'})
        output_result = tree_node.render_text('Hello World!')
        expected_result = 'Hello World! (#test)'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_anchor_id(self):
        """ Test the ``render_text`` method without any anchor ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('goto', GoToAnchorTreeNode)
        output_result = tree_node.render_text('Hello World!')
        expected_result = 'Hello World!'
        self.assertEqual(expected_result, output_result)
