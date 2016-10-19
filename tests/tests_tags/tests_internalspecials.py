"""
SkCode special internal tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (NoParseTreeNode,
                         DEFAULT_RECOGNIZED_TAGS_LIST)


class NoParseTagTestCase(unittest.TestCase):
    """ Tests suite for the special "no parse" tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(NoParseTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(NoParseTreeNode.newline_closes)
        self.assertFalse(NoParseTreeNode.same_tag_closes)
        self.assertFalse(NoParseTreeNode.standalone)
        self.assertFalse(NoParseTreeNode.parse_embedded)
        self.assertTrue(NoParseTreeNode.inline)
        self.assertFalse(NoParseTreeNode.close_inlines)
        self.assertEqual('noparse', NoParseTreeNode.canonical_tag_name)
        self.assertEqual(('nobbc', ), NoParseTreeNode.alias_tag_names)
        self.assertFalse(NoParseTreeNode.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... some text[/u]')
        rendered_output = tree_node.render_html('')
        expected_output = '[u]... some text[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities(self):
        """ Test HTML rendering with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... <some text>[/u]')
        rendered_output = tree_node.render_html('')
        expected_output = '[u]... &lt;some text&gt;[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_encoded_html_entities(self):
        """ Test HTML rendering with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = tree_node.render_html('')
        expected_output = '[u]... &lt;some text&gt;[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... some text[/u]')
        rendered_output = tree_node.render_text('')
        expected_output = '[u]... some text[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities(self):
        """ Test text rendering with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... <some text>[/u]')
        rendered_output = tree_node.render_text('')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_encoded_html_entities(self):
        """ Test text rendering with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('noparse', NoParseTreeNode, content='[u]... &lt;some text&gt;[/u]')
        rendered_output = tree_node.render_text('')
        expected_output = '[u]... <some text>[/u]'
        self.assertEqual(expected_output, rendered_output)
