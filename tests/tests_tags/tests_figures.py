"""
SkCode figures tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (
    TextTreeNode,
    FigureDeclarationTreeNode,
    FigureCaptionTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class CustomFigureDeclarationTreeNode(FigureDeclarationTreeNode):
    """ Custom figure  class """

    figure_css_class_name = 'custom_css'


class CustomFigureCaptionTreeNode(FigureCaptionTreeNode):
    """ Custom figure caption class """

    caption_css_class_name = 'custom_css'


class FigureCaptionTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the figure caption lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(FigureCaptionTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(FigureCaptionTreeNode.newline_closes)
        self.assertFalse(FigureCaptionTreeNode.same_tag_closes)
        self.assertFalse(FigureCaptionTreeNode.weak_parent_close)
        self.assertFalse(FigureCaptionTreeNode.standalone)
        self.assertTrue(FigureCaptionTreeNode.parse_embedded)
        self.assertFalse(FigureCaptionTreeNode.inline)
        self.assertTrue(FigureCaptionTreeNode.close_inlines)
        self.assertEqual('figcaption', FigureCaptionTreeNode.canonical_tag_name)
        self.assertEqual((), FigureCaptionTreeNode.alias_tag_names)
        self.assertFalse(FigureCaptionTreeNode.make_paragraphs_here)
        self.assertEqual('caption', FigureCaptionTreeNode.caption_css_class_name)
        self.assertEqual('<figcaption class="{class_name}">{inner_html}</figcaption>\n', FigureCaptionTreeNode.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figcaption', FigureCaptionTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<figcaption class="caption">test</figcaption>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figcaption', CustomFigureCaptionTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<figcaption class="custom_css">test</figcaption>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figcaption', FigureCaptionTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)


class FigureDeclarationTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the figure lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(FigureDeclarationTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(FigureDeclarationTreeNode.newline_closes)
        self.assertFalse(FigureDeclarationTreeNode.same_tag_closes)
        self.assertFalse(FigureDeclarationTreeNode.weak_parent_close)
        self.assertFalse(FigureDeclarationTreeNode.standalone)
        self.assertTrue(FigureDeclarationTreeNode.parse_embedded)
        self.assertFalse(FigureDeclarationTreeNode.inline)
        self.assertTrue(FigureDeclarationTreeNode.close_inlines)
        self.assertEqual('figure', FigureDeclarationTreeNode.canonical_tag_name)
        self.assertEqual((), FigureDeclarationTreeNode.alias_tag_names)
        self.assertTrue(FigureDeclarationTreeNode.make_paragraphs_here)
        self.assertEqual('id', FigureDeclarationTreeNode.figure_id_attr_name)
        self.assertEqual(FigureCaptionTreeNode, FigureDeclarationTreeNode.figure_caption_class)
        self.assertEqual('thumbnail', FigureDeclarationTreeNode.figure_css_class_name)
        self.assertEqual('<figure class="{class_name}" id="{figure_id}">{inner_html}</figure>\n',
                         FigureDeclarationTreeNode.render_html_template)
        self.assertEqual('_cached_figure_counter', FigureDeclarationTreeNode.cached_figure_counter_attr_name)
        self.assertEqual('_last_figure_counter', FigureDeclarationTreeNode.last_figure_counter_attr_name)
        self.assertEqual('figure-{}', FigureDeclarationTreeNode.figure_counter_format)

    def test_get_figure_id_from_counter_once(self):
        """ Test the ``get_figure_id_from_counter`` method by calling it once. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual('figure-1', tree_node.get_figure_id_from_counter())

    def test_get_figure_id_from_counter_multiple(self):
        """ Test the ``get_figure_id_from_counter`` method by calling it multiple time. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual('figure-1', tree_node.get_figure_id_from_counter())
        self.assertEqual('figure-1', tree_node.get_figure_id_from_counter())

    def test_get_figure_id_from_counter_increment(self):
        """ Test the ``get_figure_id_from_counter`` method by calling it multiple time with different figures. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual('figure-1', tree_node.get_figure_id_from_counter())
        self.assertEqual('figure-1', tree_node.get_figure_id_from_counter())
        tree_node_2 = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual('figure-2', tree_node_2.get_figure_id_from_counter())
        self.assertEqual('figure-2', tree_node_2.get_figure_id_from_counter())
        tree_node_3 = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual('figure-3', tree_node_3.get_figure_id_from_counter())
        self.assertEqual('figure-3', tree_node_3.get_figure_id_from_counter())

    def test_get_figure_id_with_tagname_set(self):
        """ Test the ``get_figure_id`` method with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'figure': 'test'})
        rendered_output = tree_node.get_figure_id()
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_id_attr_set(self):
        """ Test the ``get_figure_id`` method with the ``id`` attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'id': 'test'})
        rendered_output = tree_node.get_figure_id()
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_tagname_and_id_attr_set(self):
        """ Test the ``get_figure_id`` method with the tag name and ``id`` attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'figure': 'test', 'id': 'test2'})
        rendered_output = tree_node.get_figure_id()
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_no_figure_id_set(self):
        """ Test the ``get_figure_id`` method with no figure ID set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={})
        rendered_output = tree_node.get_figure_id()
        expected_output = 'figure-1'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_call_slugify(self):
        """ Test the ``get_figure_id`` method call the ``slugify`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.figures.slugify') as mock_slugify:
            tree_node.get_figure_id()
        mock_slugify.assert_called_once_with('test')

    def test_get_figure_caption_node(self):
        """ Test the ``get_figure_caption_node`` method with a caption. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        tree_node_caption = tree_node.new_child('figcaption', FigureCaptionTreeNode)
        self.assertEqual(tree_node_caption, tree_node.get_figure_caption_node())

    def test_get_figure_caption_node_without_caption(self):
        """ Test the ``get_figure_caption_node`` method without a caption. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        self.assertEqual(None, tree_node.get_figure_caption_node())

    def test_pre_process_node(self):
        """ Test the ``pre_process_node`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        tree_node.pre_process_node()
        self.assertEqual('', tree_node.error_message)
        self.assertEqual({'figure-1'}, root_tree_node.known_ids)
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'id': 'figure-1'})
        tree_node.pre_process_node()
        self.assertEqual('ID already used previously', tree_node.error_message)
        self.assertEqual({'figure-1'}, root_tree_node.known_ids)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<figure class="thumbnail" id="figure-1">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_id(self):
        """ Test HTML rendering with a figure ID set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode, attrs={'id': 'foobar'})
        rendered_output = tree_node.render_html('test')
        expected_output = '<figure class="thumbnail" id="foobar">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', CustomFigureDeclarationTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<figure class="custom_css" id="figure-1">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = "+----------\n| test\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        rendered_output = tree_node.render_text('   foo bar   ')
        expected_output = "+----------\n| foo bar\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_caption(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        tree_node_caption = tree_node.new_child('figcaption', FigureCaptionTreeNode)
        tree_node_caption.new_child(None, TextTreeNode, content='Hello world!')
        rendered_output = tree_node.render_text('test')
        expected_output = "+----------\n| test\n+----------\n| Hello world!\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_caption_and_trailing_whitespaces(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('figure', FigureDeclarationTreeNode)
        tree_node_caption = tree_node.new_child('figcaption', FigureCaptionTreeNode)
        tree_node_caption.new_child(None, TextTreeNode, content='   Hello world!    ')
        rendered_output = tree_node.render_text('test')
        expected_output = "+----------\n| test\n+----------\n| Hello world!\n+----------\n"
        self.assertEqual(expected_output, rendered_output)
