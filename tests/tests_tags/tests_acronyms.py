"""
SkCode acronym tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         AcronymTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class AcronymTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the acronyms tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the default dictionary of recognized tags. """
        self.assertIn('abbr', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['abbr'], AcronymTagOptions)
        self.assertIn('acronym', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['acronym'], AcronymTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = AcronymTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('abbr', opts.canonical_tag_name)
        self.assertEqual(('acronym', ), opts.alias_tag_names)
        self.assertEqual('title', opts.acronym_title_attr_name)
        self.assertEqual('<abbr title="{title}">{inner_html}</abbr>', opts.html_render_template)
        self.assertEqual('{inner_text} ({title})', opts.text_render_template)

    def test_get_acronym_title_with_tagname_set(self):
        """ Test the ``get_acronym_title`` method when the tag name attribute is set. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'abbr': 'test'})
        title = opts.get_acronym_title(tree_node)
        self.assertEqual('test', title)

    def test_get_acronym_title_with_title_set(self):
        """ Test the ``get_acronym_title`` method when the "title" attribute is set. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': 'test'})
        title = opts.get_acronym_title(tree_node)
        self.assertEqual('test', title)

    def test_get_acronym_title_with_title_and_tagname_set(self):
        """ Test the ``get_acronym_title`` method when the "title" and tag name attribute is set. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'abbr': 'test', 'title': 'test2'})
        title = opts.get_acronym_title(tree_node)
        self.assertEqual('test', title)

    def test_get_acronym_title_without_title_set(self):
        """ Test the ``get_acronym_title`` method when the title is not set at all. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={})
        title = opts.get_acronym_title(tree_node)
        self.assertEqual('', title)

    def test_get_acronym_title_with_html_entities(self):
        """ Test the ``get_acronym_title`` method with a title containing HTML entities. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': '&lt;test&gt;'})
        title = opts.get_acronym_title(tree_node)
        self.assertEqual('<test>', title)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': 'As Soon As Possible'})
        rendered_output = opts.render_html(tree_node, 'ASAP')
        expected_output = '<abbr title="As Soon As Possible">ASAP</abbr>'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title(self):
        """ Test HTML rendering without title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={})
        rendered_output = opts.render_html(tree_node, 'ASAP')
        expected_output = 'ASAP'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities_in_title(self):
        """ Test HTML rendering with HTML entities in title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': '<As Soon As Possible>'})
        rendered_output = opts.render_html(tree_node, 'ASAP')
        expected_output = '<abbr title="&lt;As Soon As Possible&gt;">ASAP</abbr>'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': 'As Soon As Possible'})
        rendered_output = opts.render_text(tree_node, 'ASAP')
        expected_output = 'ASAP (As Soon As Possible)'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title(self):
        """ Test text rendering without title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={})
        rendered_output = opts.render_text(tree_node, 'ASAP')
        expected_output = 'ASAP'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities_in_title(self):
        """ Test text rendering with HTML entities in title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': '<As Soon As Possible>'})
        rendered_output = opts.render_text(tree_node, 'ASAP')
        expected_output = 'ASAP (<As Soon As Possible>)'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_whitespaces(self):
        """ Test text rendering with extra whitespaces around the inner text. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': 'As Soon As Possible'})
        rendered_output = opts.render_text(tree_node, ' ASAP ')
        expected_output = ' ASAP (As Soon As Possible) '
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': 'As Soon As Possible'})
        expected_result = ({'title': 'As Soon As Possible'}, 'title')
        self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'ASAP'))

    def test_get_skcode_attributes_without_title(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering without title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={})
        expected_result = ({'title': ''}, 'title')
        self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'ASAP'))

    def test_get_skcode_attributes_with_html_entities(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering with HTML entities in title. """
        opts = AcronymTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('abbr', opts, attrs={'title': '<As Soon As Possible>'})
        expected_result = ({'title': '<As Soon As Possible>'}, 'title')
        self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'ASAP'))
