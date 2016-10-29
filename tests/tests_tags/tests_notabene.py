"""
SkCode Nota Bene tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    NotaBeneTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class NotaBeneTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the Nota Bene tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(NotaBeneTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(NotaBeneTreeNode.newline_closes)
        self.assertFalse(NotaBeneTreeNode.same_tag_closes)
        self.assertFalse(NotaBeneTreeNode.weak_parent_close)
        self.assertFalse(NotaBeneTreeNode.standalone)
        self.assertTrue(NotaBeneTreeNode.parse_embedded)
        self.assertFalse(NotaBeneTreeNode.inline)
        self.assertTrue(NotaBeneTreeNode.close_inlines)
        self.assertEqual('notabene', NotaBeneTreeNode.canonical_tag_name)
        self.assertEqual(('nb', ), NotaBeneTreeNode.alias_tag_names)
        self.assertFalse(NotaBeneTreeNode.make_paragraphs_here)
        self.assertEqual('important', NotaBeneTreeNode.is_important_attr_name)
        self.assertEqual('important', NotaBeneTreeNode.is_important_tagname_value)
        self.assertEqual('<p class="text-justify"><em>N.B. {inner_html}</em></p>\n',
                         NotaBeneTreeNode.html_render_template)
        self.assertEqual('N.B. {inner_text}\n\n', NotaBeneTreeNode.text_render_template)
        self.assertEqual('<p class="text-justify"><strong>N.B. {inner_html}</strong></p>\n',
                         NotaBeneTreeNode.html_render_important_template)
        self.assertEqual('N.B. {inner_text}\n\n', NotaBeneTreeNode.text_render_important_template)

    def test_get_is_important_flag_with_done_attribute_set(self):
        """ Test the ``get_is_important_flag`` method with the "important" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'important': ''})
        self.assertTrue(tree_node.get_is_important_flag())

    def test_get_is_important_flag_with_tagname_value_set(self):
        """ Test the ``get_is_important_flag`` method with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'notabene': 'important'})
        self.assertTrue(tree_node.get_is_important_flag())

    def test_get_is_important_flag_with_tagname_value_set_to_unknown_value(self):
        """ Test the ``get_is_important_flag`` method with the tag name attribute set to an unknown value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'notabene': 'johndoe'})
        self.assertFalse(tree_node.get_is_important_flag())

    def test_get_is_important_flag_without_value_set(self):
        """ Test the ``get_is_important_flag`` method without the done flag set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode)
        self.assertFalse(tree_node.get_is_important_flag())

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = '<p class="text-justify"><em>N.B. test</em></p>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_is_important(self):
        """ Test the ``render_html`` method with a "important" flag. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'important': ''})
        output_result = tree_node.render_html('test')
        expected_result = '<p class="text-justify"><strong>N.B. test</strong></p>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode)
        output_result = tree_node.render_text('test\ntest2\n')
        expected_result = 'N.B. test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode)
        output_result = tree_node.render_text('    test\ntest2\n    ')
        expected_result = 'N.B. test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_is_important(self):
        """ Test the ``render_text`` method with a "important" flag. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'important': ''})
        output_result = tree_node.render_text('test\ntest2\n')
        expected_result = 'N.B. test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces_and_is_important(self):
        """ Test the ``render_text`` method with a "important" flag. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('notabene', NotaBeneTreeNode, attrs={'important': ''})
        output_result = tree_node.render_text('    test\ntest2\n    ')
        expected_result = 'N.B. test\ntest2\n\n'
        self.assertEqual(expected_result, output_result)
