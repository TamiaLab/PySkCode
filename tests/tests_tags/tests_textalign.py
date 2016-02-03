"""
SkCode text align tags test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags.textalign import TextAlignBaseTagOptions
from skcode.tags import (RootTagOptions,
                         CenterTextTagOptions,
                         LeftTextTagOptions,
                         RightTextTagOptions,
                         JustifyTextTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TextAlignTagsTestCase(unittest.TestCase):
    """ Tests suite for text align tags module. """

    def test_assertion_constructor(self):
        """ Test assertion at ``__init__`` """
        with self.assertRaises(AssertionError) as e:
            TextAlignBaseTagOptions('')
        self.assertEqual('The text alignment is mandatory.', str(e.exception))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('center', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['center'], CenterTextTagOptions)
        self.assertIn('left', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['left'], LeftTextTagOptions)
        self.assertIn('right', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['right'], RightTextTagOptions)
        self.assertIn('justify', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['justify'], JustifyTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TextAlignBaseTagOptions('center')
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = TextAlignBaseTagOptions('custom')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('center', opts)
        self.assertEqual('<p class="text-custom">test</p>\n', opts.render_html(tree_node, 'test'))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = TextAlignBaseTagOptions('custom')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('center', opts)
        self.assertEqual('test', opts.render_text(tree_node, 'test'))

    def test_center_subclass(self):
        """ Test the center subclass """
        self.assertTrue(issubclass(CenterTextTagOptions, TextAlignBaseTagOptions))
        self.assertEqual('center', CenterTextTagOptions().text_alignment)

    def test_left_subclass(self):
        """ Test the left subclass """
        self.assertTrue(issubclass(LeftTextTagOptions, TextAlignBaseTagOptions))
        self.assertEqual('left', LeftTextTagOptions().text_alignment)

    def test_right_subclass(self):
        """ Test the right subclass """
        self.assertTrue(issubclass(RightTextTagOptions, TextAlignBaseTagOptions))
        self.assertEqual('right', RightTextTagOptions().text_alignment)

    def test_justify_subclass(self):
        """ Test the justify subclass """
        self.assertTrue(issubclass(JustifyTextTagOptions, TextAlignBaseTagOptions))
        self.assertEqual('justify', JustifyTextTagOptions().text_alignment)
