"""
SkCode acronym tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import AcronymTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST


class AcronymTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the acronyms tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the default dictionary of recognized tags. """
        self.assertIn(AcronymTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(AcronymTreeNode.newline_closes)
        self.assertFalse(AcronymTreeNode.same_tag_closes)
        self.assertFalse(AcronymTreeNode.weak_parent_close)
        self.assertFalse(AcronymTreeNode.standalone)
        self.assertTrue(AcronymTreeNode.parse_embedded)
        self.assertTrue(AcronymTreeNode.inline)
        self.assertFalse(AcronymTreeNode.close_inlines)
        self.assertFalse(AcronymTreeNode.make_paragraphs_here)
        self.assertEqual('abbr', AcronymTreeNode.canonical_tag_name)
        self.assertEqual(('acronym', ), AcronymTreeNode.alias_tag_names)
        self.assertEqual('title', AcronymTreeNode.acronym_title_attr_name)
        self.assertEqual('<abbr title="{title}">{inner_html}</abbr>', AcronymTreeNode.html_render_template)
        self.assertEqual('{inner_text} ({title})', AcronymTreeNode.text_render_template)

    def test_get_acronym_title_with_tagname_set(self):
        """ Test the ``get_acronym_title`` method when the tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'abbr': 'test'})
        title = tree_node.get_acronym_title()
        self.assertEqual('test', title)

    def test_get_acronym_title_with_title_set(self):
        """ Test the ``get_acronym_title`` method when the "title" attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': 'test'})
        title = tree_node.get_acronym_title()
        self.assertEqual('test', title)

    def test_get_acronym_title_with_title_and_tagname_set(self):
        """ Test the ``get_acronym_title`` method when the "title" and tag name attribute is set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'abbr': 'test', 'title': 'test2'})
        title = tree_node.get_acronym_title()
        self.assertEqual('test', title)

    def test_get_acronym_title_without_title_set(self):
        """ Test the ``get_acronym_title`` method when the title is not set at all. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={})
        title = tree_node.get_acronym_title()
        self.assertEqual('', title)

    def test_get_acronym_title_with_html_entities(self):
        """ Test the ``get_acronym_title`` method with a title containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': '&lt;test&gt;'})
        title = tree_node.get_acronym_title()
        self.assertEqual('<test>', title)

    def test_sanitize_node(self):
        """ Test if the ``sanitize_node`` method mark the node as erroneous when title is missing """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={})
        tree_node.sanitize_node([])
        self.assertEqual('Missing acronym definition', tree_node.error_message)
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'abbr': '', 'title': ''})
        tree_node.sanitize_node([])
        self.assertEqual('Missing acronym definition', tree_node.error_message)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': 'As Soon As Possible'})
        rendered_output = tree_node.render_html('ASAP')
        expected_output = '<abbr title="As Soon As Possible">ASAP</abbr>'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title(self):
        """ Test HTML rendering without title. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={})
        rendered_output = tree_node.render_html('ASAP')
        expected_output = 'ASAP'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities_in_title(self):
        """ Test HTML rendering with HTML entities in title. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': '<As Soon As Possible>'})
        rendered_output = tree_node.render_html('ASAP')
        expected_output = '<abbr title="&lt;As Soon As Possible&gt;">ASAP</abbr>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': 'As Soon As Possible'})
        rendered_output = tree_node.render_text('ASAP')
        expected_output = 'ASAP (As Soon As Possible)'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title(self):
        """ Test text rendering without title. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={})
        rendered_output = tree_node.render_text('ASAP')
        expected_output = 'ASAP'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities_in_title(self):
        """ Test text rendering with HTML entities in title. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': '<As Soon As Possible>'})
        rendered_output = tree_node.render_text('ASAP')
        expected_output = 'ASAP (<As Soon As Possible>)'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_whitespaces(self):
        """ Test text rendering with extra whitespaces around the inner text. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('abbr', AcronymTreeNode, attrs={'title': 'As Soon As Possible'})
        rendered_output = tree_node.render_text(' ASAP ')
        expected_output = ' ASAP (As Soon As Possible) '
        self.assertEqual(expected_output, rendered_output)
