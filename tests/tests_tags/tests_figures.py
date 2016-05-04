"""
SkCode figures tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TextTagOptions,
                         FigureDeclarationTagOptions,
                         FigureCaptionTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class FigureCaptionTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the figure caption lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('figcaption', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['figcaption'], FigureCaptionTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = FigureCaptionTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('figcaption', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('caption', opts.caption_css_class_name)
        self.assertEqual('<figcaption class="{class_name}">{inner_html}</figcaption>\n', opts.render_html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = FigureCaptionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figcaption', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<figcaption class="caption">test</figcaption>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering. """
        opts = FigureCaptionTagOptions(caption_css_class_name='custom_css')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figcaption', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<figcaption class="custom_css">test</figcaption>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = FigureCaptionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figcaption', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)


class FigureDeclarationTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the figure lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('figure', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['figure'], FigureDeclarationTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = FigureDeclarationTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('figure', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('id', opts.figure_id_attr_name)
        self.assertEqual(FigureCaptionTagOptions, opts.figure_caption_class)
        self.assertEqual('thumbnail', opts.figure_css_class_name)

    def test_get_figure_id_with_tagname_set(self):
        """ Test the ``get_figure_id`` method with the tag name attribute set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'figure': 'test'})
        rendered_output = opts.get_figure_id(tree_node)
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_id_attr_set(self):
        """ Test the ``get_figure_id`` method with the ``id`` attribute set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'id': 'test'})
        rendered_output = opts.get_figure_id(tree_node)
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_tagname_and_id_attr_set(self):
        """ Test the ``get_figure_id`` method with the tag name and ``id`` attribute set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'figure': 'test', 'id': 'test2'})
        rendered_output = opts.get_figure_id(tree_node)
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_with_no_figure_id_set(self):
        """ Test the ``get_figure_id`` method with no figure ID set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={})
        rendered_output = opts.get_figure_id(tree_node)
        expected_output = ''
        self.assertEqual(expected_output, rendered_output)

    def test_get_figure_id_call_slugify(self):
        """ Test the ``get_figure_id`` method call the ``slugify`` function. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.figures.slugify') as mock_slugify:
            opts.get_figure_id(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_get_figure_caption_node(self):
        """ Test the ``get_figure_caption_node`` method with a caption. """
        opts = FigureDeclarationTagOptions()
        opts_caption = FigureCaptionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        tree_node_caption = tree_node.new_child('figcaption', opts_caption)
        self.assertEqual(tree_node_caption, opts.get_figure_caption_node(tree_node))

    def test_get_figure_caption_node_without_caption(self):
        """ Test the ``get_figure_caption_node`` method without a caption. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        self.assertEqual(None, opts.get_figure_caption_node(tree_node))

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<figure class="thumbnail" id="">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_id(self):
        """ Test HTML rendering with a figure ID set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'id': 'foobar'})
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<figure class="thumbnail" id="foobar">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering. """
        opts = FigureDeclarationTagOptions(figure_css_class_name='custom_css')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<figure class="custom_css" id="">test</figure>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = "+----------\n| test\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_trailing_whitespaces(self):
        """ Test text rendering. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        rendered_output = opts.render_text(tree_node, '   foo bar   ')
        expected_output = "+----------\n| foo bar\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_caption(self):
        """ Test text rendering. """
        opts = FigureDeclarationTagOptions()
        opts_caption = FigureCaptionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        tree_node_caption = tree_node.new_child('figcaption', opts_caption)
        tree_node_caption.new_child('_text', TextTagOptions(), content='Hello world!')
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = "+----------\n| test\n+----------\n| Hello world!\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_caption_and_trailing_whitespaces(self):
        """ Test text rendering. """
        opts = FigureDeclarationTagOptions()
        opts_caption = FigureCaptionTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        tree_node_caption = tree_node.new_child('figcaption', opts_caption)
        tree_node_caption.new_child('_text', TextTagOptions(), content='   Hello world!    ')
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = "+----------\n| test\n+----------\n| Hello world!\n+----------\n"
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts, attrs={'id': 'test'})
        rendered_output = opts.get_skcode_attributes(tree_node, 'foobar')
        expected_output = ({'id': 'test'}, 'id')
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes_with_no_id(self):
        """ Test the ``get_skcode_attributes`` method with no figure ID set. """
        opts = FigureDeclarationTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('figure', opts)
        rendered_output = opts.get_skcode_attributes(tree_node, 'test')
        expected_output = ({'id': ''}, 'id')
        self.assertEqual(expected_output, rendered_output)
