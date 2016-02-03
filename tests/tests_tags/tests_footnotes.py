"""
SkCode footnotes tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         FootnoteDeclarationTagOptions,
                         FootnoteReferenceTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class FootnoteDeclarationTagTestCase(unittest.TestCase):
    """ Tests suite for the footnote declaration tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('fn', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['fn'], FootnoteDeclarationTagOptions)
        self.assertIn('footnote', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['footnote'], FootnoteDeclarationTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = FootnoteDeclarationTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('id', opts.footnote_id_attr_name)
        self.assertEqual('footnote-%s', opts.footnote_id_html_format)
        self.assertEqual('footnote-backref-%s', opts.footnote_id_html_format_backref)
        self.assertEqual('_cached_footnote_counter', opts.cached_footnote_counter_attr_name)
        self.assertEqual('_last_footnote_counter', opts.last_footnote_counter_attr_name)

    def test_get_footnote_id_from_counter_once(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it once. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts)
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node, root_tree_node), '1')

    def test_get_footnote_id_from_counter_multiple(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it multiple time. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts)
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node, root_tree_node), '1')
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node, root_tree_node), '1')

    def test_get_footnote_id_from_counter_increment(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it multiple time with different footnote. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts)
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node, root_tree_node), '1')
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node, root_tree_node), '1')
        tree_node_2 = root_tree_node.new_child('footnote', opts)
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node_2, root_tree_node), '2')
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node_2, root_tree_node), '2')
        tree_node_3 = root_tree_node.new_child('footnote', opts)
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node_3, root_tree_node), '3')
        self.assertEqual(opts.get_footnote_id_from_counter(tree_node_3, root_tree_node), '3')

    def test_get_footnote_id_with_tagname_set(self):
        """ Test the ``get_footnote_id`` method with the tag name set. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'footnote': 'test'})
        output = opts.get_footnote_id(tree_node, root_tree_node)
        self.assertEqual('test', output)

    def test_get_footnote_id_with_id_attr_set(self):
        """ Test the ``get_footnote_id`` method with the ``id`` attribute set. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'id': 'test'})
        output = opts.get_footnote_id(tree_node, root_tree_node)
        self.assertEqual('test', output)

    def test_get_footnote_id_with_tagname_and_id_attr_set(self):
        """ Test the ``get_footnote_id`` method with the tag name and the ``id`` attribute set. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'footnote': 'test', 'id': 'test2'})
        output = opts.get_footnote_id(tree_node, root_tree_node)
        self.assertEqual('test', output)

    def test_get_footnote_id_with_no_id_set_and_counter_enabled(self):
        """ Test the ``get_footnote_id`` method with no ID set and auto-counter enabled. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={})
        output = opts.get_footnote_id(tree_node, root_tree_node)
        self.assertEqual('1', output)

    def test_get_footnote_id_with_no_id_set_and_counter_disabled(self):
        """ Test the ``get_footnote_id`` method with no ID set and auto-counter disabled. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={})
        output = opts.get_footnote_id(tree_node, root_tree_node, use_auto_generated_id=False)
        self.assertEqual('', output)

    def test_get_footnote_id_call_slugify(self):
        """ Test the ``get_footnote_id`` method call the ``slugify`` function. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.footnotes.slugify') as mock_slugify:
            opts.get_footnote_id(tree_node, root_tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_get_footnote_ref_id(self):
        """  Test the ``get_footnote_ref_id`` method. """
        opts = FootnoteDeclarationTagOptions()
        output = opts.get_footnote_ref_id('test')
        self.assertEqual('footnote-test', output)

    def test_get_footnote_backref_id(self):
        """  Test the ``get_footnote_backref_id`` method. """
        opts = FootnoteDeclarationTagOptions()
        output = opts.get_footnote_backref_id('test')
        self.assertEqual('footnote-backref-test', output)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'id': 'test'})
        rendered_output = opts.render_html(tree_node, 'Hello world!')
        expected_output = '<a id="footnote-backref-test" href="#footnote-test"><sup>[test]</sup></a>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'id': 'test'})
        rendered_output = opts.render_text(tree_node, 'Hello world!')
        expected_output = '[^test]'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = FootnoteDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('footnote', opts, attrs={'id': 'test'})
        rendered_output = opts.get_skcode_attributes(tree_node, 'Hello world!')
        expected_output = ({'id': 'test'}, 'id')
        self.assertEqual(expected_output, rendered_output)


class FootnoteReferenceTagTestCase(unittest.TestCase):
    """ Tests suite for the footnote reference tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('fnref', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['fnref'], FootnoteReferenceTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = FootnoteReferenceTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('footnote-%s', opts.footnote_id_html_format)

    def test_get_footnote_id(self):
        """ Test the ``get_footnote_id`` method. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='test')
        output = opts.get_footnote_id(tree_node)
        self.assertEqual('test', output)

    def test_get_footnote_id_with_no_id_set(self):
        """ Test the ``get_footnote_id`` method with no ID set. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='')
        output = opts.get_footnote_id(tree_node)
        self.assertEqual('', output)

    def test_get_footnote_id_call_slugify(self):
        """ Test the ``get_footnote_id`` method call the ``slugify`` function. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='test')
        with unittest.mock.patch('skcode.tags.footnotes.slugify') as mock_slugify:
            opts.get_footnote_id(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_get_footnote_ref_id(self):
        """  Test the ``get_footnote_ref_id`` method. """
        opts = FootnoteReferenceTagOptions()
        output = opts.get_footnote_ref_id('test')
        self.assertEqual('footnote-test', output)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='test')
        rendered_output = opts.render_html(tree_node, 'Hello world!')
        expected_output = '<a href="#footnote-test"><sup>[test]</sup></a>'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_no_id(self):
        """ Test HTML rendering with no ID set. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='')
        rendered_output = opts.render_html(tree_node, 'Hello world!')
        self.assertEqual('Hello world!', rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='test')
        rendered_output = opts.render_text(tree_node, 'Hello world!')
        expected_output = '[^test]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_no_id(self):
        """ Test text rendering with no ID set. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='')
        rendered_output = opts.render_html(tree_node, 'Hello world!')
        self.assertEqual('Hello world!', rendered_output)

    def test_get_skcode_inner_content(self):
        """ Test the ``get_skcode_inner_content`` method. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='test')
        rendered_output = opts.get_skcode_inner_content(tree_node, 'Hello world!')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_inner_content_with_no_id(self):
        """ Test the ``get_skcode_inner_content`` method with no id set. """
        opts = FootnoteReferenceTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('fnref', opts, content='')
        rendered_output = opts.get_skcode_inner_content(tree_node, 'Hello world!')
        self.assertEqual('Hello world!', rendered_output)
