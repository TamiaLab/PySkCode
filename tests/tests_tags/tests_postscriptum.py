"""
SkCode Post scriptum tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         PostScriptumTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class PostScriptumTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the Post scriptum tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('postscriptum', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['postscriptum'], PostScriptumTagOptions)
        self.assertIn('ps', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ps'], PostScriptumTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = PostScriptumTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('postscriptum', opts.canonical_tag_name)
        self.assertEqual(('ps', ), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('important', opts.is_important_attr_name)
        self.assertEqual('important', opts.is_important_tagname_value)
        self.assertEqual('<p class="text-justify"><em>PS {inner_html}</em></p>\n', opts.html_render_template)
        self.assertEqual('PS {inner_text}\n\n', opts.text_render_template)
        self.assertEqual('<p class="text-justify"><strong>PS {inner_html}</strong></p>\n', opts.html_render_important_template)
        self.assertEqual('PS {inner_text}\n\n', opts.text_render_important_template)

    def test_get_is_important_flag_with_done_attribute_set(self):
        """ Test the ``get_is_important_flag`` method with the "important" attribute set. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'important': ''})
        self.assertTrue(opts.get_is_important_flag(tree_node))

    def test_get_is_important_flag_with_tagname_value_set(self):
        """ Test the ``get_is_important_flag`` method with the tag name attribute set. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'postscriptum': 'important'})
        self.assertTrue(opts.get_is_important_flag(tree_node))

    def test_get_is_important_flag_with_tagname_value_set_to_unknown_value(self):
        """ Test the ``get_is_important_flag`` method with the tag name attribute set to an unknown value. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'postscriptum': 'johndoe'})
        self.assertFalse(opts.get_is_important_flag(tree_node))

    def test_get_is_important_flag_without_value_set(self):
        """ Test the ``get_is_important_flag`` method without the done flag set. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts)
        self.assertFalse(opts.get_is_important_flag(tree_node))

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<p class="text-justify"><em>PS test</em></p>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_is_important(self):
        """ Test the ``render_html`` method with a "important" flag. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'important': ''})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<p class="text-justify"><strong>PS test</strong></p>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts)
        output_result = opts.render_text(tree_node, 'test\ntest2\n')
        expected_result = 'PS test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts)
        output_result = opts.render_text(tree_node, '    test\ntest2\n    ')
        expected_result = 'PS test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_is_important(self):
        """ Test the ``render_text`` method with a "important" flag. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'important': ''})
        output_result = opts.render_text(tree_node, 'test\ntest2\n')
        expected_result = 'PS test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces_and_is_important(self):
        """ Test the ``render_text`` method with a "important" flag. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'important': ''})
        output_result = opts.render_text(tree_node, '    test\ntest2\n    ')
        expected_result = 'PS test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts)
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_is_important(self):
        """ Test the ``get_skcode_attributes`` method with a "important" flag. """
        opts = PostScriptumTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('postscriptum', opts, attrs={'important': ''})
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'important': None}, None)
        self.assertEqual(expected_result, output_result)
