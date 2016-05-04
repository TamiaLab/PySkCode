"""
SkCode definitions list tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         DefinitionListTagOptions,
                         DefinitionListTermTagOptions,
                         DefinitionListTermDefinitionTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class DefinitionListTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the definition lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('dl', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['dl'], DefinitionListTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = DefinitionListTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('dl', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('<dl>{inner_html}</dl>\n', opts.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dl', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dl>test</dl>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dl', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class DefinitionListTermTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the definition terms tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('dt', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['dt'], DefinitionListTermTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = DefinitionListTermTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('dt', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('<dt>{inner_html}</dt>\n', opts.render_html_template)
        self.assertEqual('{inner_text} : ', opts.render_text_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTermTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dt', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dt>test</dt>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTermTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dt', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test : '
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering with trailing whitespaces. """
        opts = DefinitionListTermTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dt', opts)
        rendered_output = opts.render_text(tree_node, '  foo bar   ')
        expected_output = 'foo bar : '
        self.assertEqual(expected_output, rendered_output)


class DefinitionListTermDefinitionTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the definitions tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('dd', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['dd'], DefinitionListTermDefinitionTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = DefinitionListTermDefinitionTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('dd', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('<dd>{inner_html}</dd>\n', opts.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTermDefinitionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dd', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dd>test</dd>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTermDefinitionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dd', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering with trailing whitespaces. """
        opts = DefinitionListTermDefinitionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('dd', opts)
        rendered_output = opts.render_text(tree_node, '  foo bar   ')
        expected_output = 'foo bar'
        self.assertEqual(expected_output, rendered_output)
