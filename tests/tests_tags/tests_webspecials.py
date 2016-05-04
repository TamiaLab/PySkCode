"""
SkCode web special tag definitions test code.
"""

import unittest

from skcode.tags import (HorizontalLineTagOptions,
                         LineBreakTagOptions,
                         CutHereTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)
from skcode.tags.webspecials import CUT_HERE_STRING


class HorizontalLineTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the horizontal line tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('hr', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['hr'], HorizontalLineTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = HorizontalLineTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertTrue(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('hr', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = HorizontalLineTagOptions()
        self.assertEqual('<hr>\n', opts.render_html(None, ''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = HorizontalLineTagOptions()
        self.assertEqual('----------\n', opts.render_text(None, ''))


class LineBreakTagTestCase(unittest.TestCase):
    """ Tests suite for the line break tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('br', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['br'], LineBreakTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = LineBreakTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertTrue(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertEqual('br', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = LineBreakTagOptions()
        self.assertEqual('<br>\n', opts.render_html(None, ''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = LineBreakTagOptions()
        self.assertEqual('\n', opts.render_text(None, ''))


class CutHereTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the "cut here" tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('cuthere', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['cuthere'], CutHereTagOptions)

    def test_module_constants(self):
        """ Test module level costants """
        self.assertEqual('<!-- Cut Here -->', CUT_HERE_STRING)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = CutHereTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertTrue(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('cuthere', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = CutHereTagOptions()
        self.assertEqual('<!-- Cut Here -->\n', opts.render_html(None, ''))

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = CutHereTagOptions()
        self.assertEqual('', opts.render_text(None, ''))
