"""
SkCode footnotes tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (
    FootnoteDeclarationTreeNode,
    FootnoteReferenceTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class FootnoteDeclarationTagTestCase(unittest.TestCase):
    """ Tests suite for the footnote declaration tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(FootnoteDeclarationTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(FootnoteDeclarationTreeNode.newline_closes)
        self.assertFalse(FootnoteDeclarationTreeNode.same_tag_closes)
        self.assertFalse(FootnoteDeclarationTreeNode.weak_parent_close)
        self.assertFalse(FootnoteDeclarationTreeNode.standalone)
        self.assertTrue(FootnoteDeclarationTreeNode.parse_embedded)
        self.assertTrue(FootnoteDeclarationTreeNode.inline)
        self.assertFalse(FootnoteDeclarationTreeNode.close_inlines)
        self.assertEqual('footnote', FootnoteDeclarationTreeNode.canonical_tag_name)
        self.assertEqual(('fn', ), FootnoteDeclarationTreeNode.alias_tag_names)
        self.assertFalse(FootnoteDeclarationTreeNode.make_paragraphs_here)
        self.assertEqual('id', FootnoteDeclarationTreeNode.footnote_id_attr_name)
        self.assertEqual('footnote-{}', FootnoteDeclarationTreeNode.footnote_id_html_format)
        self.assertEqual('footnote-backref-{}', FootnoteDeclarationTreeNode.footnote_id_html_format_backref)
        self.assertEqual('_cached_footnote_counter', FootnoteDeclarationTreeNode.cached_footnote_counter_attr_name)
        self.assertEqual('_last_footnote_counter', FootnoteDeclarationTreeNode.last_footnote_counter_attr_name)
        self.assertEqual('footnote-{}', FootnoteDeclarationTreeNode.footnote_counter_format)
        self.assertEqual('<a id="{backward_id}" href="#{forward_id}"><sup>[{footnote_id}]</sup></a>',
                         FootnoteDeclarationTreeNode.html_render_template)
        self.assertEqual('[^{footnote_id}]', FootnoteDeclarationTreeNode.text_render_template)

    def test_get_footnote_id_from_counter_once(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it once. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        self.assertEqual('footnote-1', tree_node.get_footnote_id_from_counter())

    def test_get_footnote_id_from_counter_multiple(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it multiple time. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        self.assertEqual('footnote-1', tree_node.get_footnote_id_from_counter())
        self.assertEqual('footnote-1', tree_node.get_footnote_id_from_counter())

    def test_get_footnote_id_from_counter_increment(self):
        """ Test the ``get_footnote_id_from_counter`` method by calling it multiple time with different footnote. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        self.assertEqual('footnote-1', tree_node.get_footnote_id_from_counter())
        self.assertEqual('footnote-1', tree_node.get_footnote_id_from_counter())
        tree_node_2 = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        self.assertEqual('footnote-2', tree_node_2.get_footnote_id_from_counter())
        self.assertEqual('footnote-2', tree_node_2.get_footnote_id_from_counter())
        tree_node_3 = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        self.assertEqual('footnote-3', tree_node_3.get_footnote_id_from_counter())
        self.assertEqual('footnote-3', tree_node_3.get_footnote_id_from_counter())

    def test_get_footnote_id_with_tagname_set(self):
        """ Test the ``get_footnote_id`` method with the tag name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'footnote': 'test'})
        output = tree_node.get_footnote_id()
        self.assertEqual('test', output)

    def test_get_footnote_id_with_id_attr_set(self):
        """ Test the ``get_footnote_id`` method with the ``id`` attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'id': 'test'})
        output = tree_node.get_footnote_id()
        self.assertEqual('test', output)

    def test_get_footnote_id_with_tagname_and_id_attr_set(self):
        """ Test the ``get_footnote_id`` method with the tag name and the ``id`` attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode,
                                             attrs={'footnote': 'test', 'id': 'test2'})
        output = tree_node.get_footnote_id()
        self.assertEqual('test', output)

    def test_get_footnote_id_with_no_id_set_and_counter_enabled(self):
        """ Test the ``get_footnote_id`` method with no ID set and auto-counter enabled. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={})
        output = tree_node.get_footnote_id()
        self.assertEqual('footnote-1', output)

    def test_get_footnote_id_call_slugify(self):
        """ Test the ``get_footnote_id`` method call the ``slugify`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.footnotes.slugify') as mock_slugify:
            tree_node.get_footnote_id()
        mock_slugify.assert_called_once_with('test')

    def test_get_footnote_ref_id(self):
        """  Test the ``get_footnote_ref_id`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        output = tree_node.get_footnote_ref_id('test')
        self.assertEqual('footnote-test', output)

    def test_get_footnote_backref_id(self):
        """  Test the ``get_footnote_backref_id`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        output = tree_node.get_footnote_backref_id('test')
        self.assertEqual('footnote-backref-test', output)

    def test_pre_process_node(self):
        """ Test the ``pre_process_node`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode)
        tree_node.pre_process_node()
        self.assertEqual('', tree_node.error_message)
        self.assertEqual({'footnote-1'}, root_tree_node.known_ids)
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'id': 'footnote-1'})
        tree_node.pre_process_node()
        self.assertEqual('ID already used previously', tree_node.error_message)
        self.assertEqual({'footnote-1'}, root_tree_node.known_ids)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'id': 'test'})
        rendered_output = tree_node.render_html('Hello world!')
        expected_output = '<a id="footnote-backref-test" href="#footnote-test"><sup>[test]</sup></a>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('footnote', FootnoteDeclarationTreeNode, attrs={'id': 'test'})
        rendered_output = tree_node.render_text('Hello world!')
        expected_output = '[^test]'
        self.assertEqual(expected_output, rendered_output)


class FootnoteReferenceTagTestCase(unittest.TestCase):
    """ Tests suite for the footnote reference tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(FootnoteReferenceTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(FootnoteReferenceTreeNode.newline_closes)
        self.assertFalse(FootnoteReferenceTreeNode.same_tag_closes)
        self.assertFalse(FootnoteReferenceTreeNode.weak_parent_close)
        self.assertFalse(FootnoteReferenceTreeNode.standalone)
        self.assertTrue(FootnoteReferenceTreeNode.parse_embedded)
        self.assertTrue(FootnoteReferenceTreeNode.inline)
        self.assertFalse(FootnoteReferenceTreeNode.close_inlines)
        self.assertEqual('fnref', FootnoteReferenceTreeNode.canonical_tag_name)
        self.assertEqual((), FootnoteReferenceTreeNode.alias_tag_names)
        self.assertFalse(FootnoteReferenceTreeNode.make_paragraphs_here)
        self.assertEqual('footnote-{}', FootnoteReferenceTreeNode.footnote_id_html_format)
        self.assertEqual('<a href="#{forward_id}"><sup>[{footnote_id}]</sup></a>', FootnoteReferenceTreeNode.html_render_template)
        self.assertEqual('[^{footnote_id}]', FootnoteReferenceTreeNode.text_render_template)

    def test_get_footnote_id(self):
        """ Test the ``get_footnote_id`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        output = tree_node.get_footnote_id()
        self.assertEqual('test', output)

    def test_get_footnote_id_with_no_id_set(self):
        """ Test the ``get_footnote_id`` method with no ID set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='')
        output = tree_node.get_footnote_id()
        self.assertEqual('', output)

    def test_get_footnote_id_call_slugify(self):
        """ Test the ``get_footnote_id`` method call the ``slugify`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        with unittest.mock.patch('skcode.tags.footnotes.slugify') as mock_slugify:
            tree_node.get_footnote_id()
        mock_slugify.assert_called_once_with('test')

    def test_get_footnote_ref_id(self):
        """  Test the ``get_footnote_ref_id`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        output = tree_node.get_footnote_ref_id('test')
        self.assertEqual('footnote-test', output)

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='')
        tree_node.sanitize_node([])
        self.assertEqual('Missing footnote ID', tree_node.error_message)
        self.assertEqual(set(), root_tree_node.known_ids)
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        tree_node.sanitize_node([])
        self.assertEqual('Unknown footnote ID', tree_node.error_message)
        root_tree_node.known_ids.add('test')
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        rendered_output = tree_node.render_html('Hello world!')
        expected_output = '<a href="#footnote-test"><sup>[test]</sup></a>'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_no_id(self):
        """ Test HTML rendering with no ID set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='')
        rendered_output = tree_node.render_html('Hello world!')
        self.assertEqual('Hello world!', rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='test')
        rendered_output = tree_node.render_text('Hello world!')
        expected_output = '[^test]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_no_id(self):
        """ Test text rendering with no ID set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('fnref', FootnoteReferenceTreeNode, content='')
        rendered_output = tree_node.render_html('Hello world!')
        self.assertEqual('Hello world!', rendered_output)
