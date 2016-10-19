"""
SkCode definitions list tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (DefinitionListTreeNode,
                         DefinitionListTermTreeNode,
                         DefinitionListTermDefinitionTreeNode,
                         DEFAULT_RECOGNIZED_TAGS_LIST)


class DefinitionListTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the definition lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(DefinitionListTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(DefinitionListTreeNode.newline_closes)
        self.assertFalse(DefinitionListTreeNode.same_tag_closes)
        self.assertFalse(DefinitionListTreeNode.standalone)
        self.assertTrue(DefinitionListTreeNode.parse_embedded)
        self.assertFalse(DefinitionListTreeNode.inline)
        self.assertTrue(DefinitionListTreeNode.close_inlines)
        self.assertEqual('dl', DefinitionListTreeNode.canonical_tag_name)
        self.assertEqual((), DefinitionListTreeNode.alias_tag_names)
        self.assertFalse(DefinitionListTreeNode.make_paragraphs_here)
        self.assertEqual('<dl>{inner_html}</dl>\n', DefinitionListTreeNode.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dl', DefinitionListTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<dl>test</dl>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dl', DefinitionListTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class DefinitionListTermTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the definition terms tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(DefinitionListTermTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(DefinitionListTermTreeNode.newline_closes)
        self.assertFalse(DefinitionListTermTreeNode.same_tag_closes)
        self.assertFalse(DefinitionListTermTreeNode.standalone)
        self.assertTrue(DefinitionListTermTreeNode.parse_embedded)
        self.assertFalse(DefinitionListTermTreeNode.inline)
        self.assertTrue(DefinitionListTermTreeNode.close_inlines)
        self.assertEqual('dt', DefinitionListTermTreeNode.canonical_tag_name)
        self.assertEqual((), DefinitionListTermTreeNode.alias_tag_names)
        self.assertFalse(DefinitionListTermTreeNode.make_paragraphs_here)
        self.assertEqual('<dt>{inner_html}</dt>\n', DefinitionListTermTreeNode.render_html_template)
        self.assertEqual('{inner_text} : ', DefinitionListTermTreeNode.render_text_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dt', DefinitionListTermTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<dt>test</dt>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dt', DefinitionListTermTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test : '
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering with trailing whitespaces. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dt', DefinitionListTermTreeNode)
        rendered_output = tree_node.render_text('  foo bar   ')
        expected_output = 'foo bar : '
        self.assertEqual(expected_output, rendered_output)


class DefinitionListTermDefinitionTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the definitions tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(DefinitionListTermDefinitionTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(DefinitionListTermDefinitionTreeNode.newline_closes)
        self.assertFalse(DefinitionListTermDefinitionTreeNode.same_tag_closes)
        self.assertFalse(DefinitionListTermDefinitionTreeNode.standalone)
        self.assertTrue(DefinitionListTermDefinitionTreeNode.parse_embedded)
        self.assertFalse(DefinitionListTermDefinitionTreeNode.inline)
        self.assertTrue(DefinitionListTermDefinitionTreeNode.close_inlines)
        self.assertEqual('dd', DefinitionListTermDefinitionTreeNode.canonical_tag_name)
        self.assertEqual((), DefinitionListTermDefinitionTreeNode.alias_tag_names)
        self.assertTrue(DefinitionListTermDefinitionTreeNode.make_paragraphs_here)
        self.assertEqual('<dd>{inner_html}</dd>\n', DefinitionListTermDefinitionTreeNode.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dd', DefinitionListTermDefinitionTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<dd>test</dd>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dd', DefinitionListTermDefinitionTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering with trailing whitespaces. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('dd', DefinitionListTermDefinitionTreeNode)
        rendered_output = tree_node.render_text('  foo bar   ')
        expected_output = 'foo bar'
        self.assertEqual(expected_output, rendered_output)
