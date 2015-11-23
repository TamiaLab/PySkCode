"""
SkCode definitions tag test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (DefinitionListTagOptions,
                         DefinitionListTermTagOptions,
                         DefinitionListTermDefinitionTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class DefinitionListsTagtestCase(unittest.TestCase):
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
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTagOptions()
        tree_node = TreeNode(None, 'dl', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dl>test</dl>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTagOptions()
        tree_node = TreeNode(None, 'dl', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        opts = DefinitionListTagOptions()
        tree_node = TreeNode(None, 'dl', opts)
        rendered_output = opts.render_skcode(tree_node, 'test')
        expected_output = '[dl]test[/dl]'
        self.assertEqual(expected_output, rendered_output)


class DefinitionTermsTagtestCase(unittest.TestCase):
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
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTermTagOptions()
        tree_node = TreeNode(None, 'dt', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dt>test</dt>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTermTagOptions()
        tree_node = TreeNode(None, 'dt', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test : '
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        opts = DefinitionListTermTagOptions()
        tree_node = TreeNode(None, 'dt', opts)
        rendered_output = opts.render_skcode(tree_node, 'test')
        expected_output = '[dt]test[/dt]'
        self.assertEqual(expected_output, rendered_output)


class DefinitionsTagtestCase(unittest.TestCase):
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
        self.assertTrue(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = DefinitionListTermDefinitionTagOptions()
        tree_node = TreeNode(None, 'dd', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<dd>test</dd>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = DefinitionListTermDefinitionTagOptions()
        tree_node = TreeNode(None, 'dd', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        opts = DefinitionListTermDefinitionTagOptions()
        tree_node = TreeNode(None, 'dd', opts)
        rendered_output = opts.render_skcode(tree_node, 'test')
        expected_output = '[dd]test[/dd]'
        self.assertEqual(expected_output, rendered_output)
