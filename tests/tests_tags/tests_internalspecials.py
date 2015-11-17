"""
SkCode specials tag test code.
"""

import unittest

from skcode import (parse_skcode,
                    render_to_html,
                    render_to_text,
                    render_to_skcode)
from skcode.tags import (NoParseTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class NoParseTagtestCase(unittest.TestCase):
    """ Tests suite for the special "no parse" tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('noparse', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['noparse'], NoParseTagOptions)
        self.assertIn('nobbc', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['nobbc'], NoParseTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = NoParseTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertFalse(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        document_tree = parse_skcode('Use the [noparse][u]... some text[/u][/noparse] tag to underline text.')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Use the [u]... some text[/u] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities(self):
        """ Test HTML rendering with HTML entities. """
        document_tree = parse_skcode('Use the [noparse][u]... <some text>[/u][/noparse] tag to underline text.')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Use the [u]... &lt;some text&gt;[/u] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_encoded_html_entities(self):
        """ Test HTML rendering with encoded HTML entities. """
        document_tree = parse_skcode('Use the [noparse][u]... &lt;some text&gt;[/u][/noparse] tag to underline text.')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Use the [u]... &lt;some text&gt;[/u] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Use the [noparse][u]... some text[/u][/noparse] tag to underline text.')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Use the [u]... some text[/u] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities(self):
        """ Test text rendering with encoded HTML entities. """
        document_tree = parse_skcode('Use the [noparse][u]... &lt;some text&gt;[/u][/noparse] tag to underline text.')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Use the [u]... <some text>[/u] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Use the [noparse][u]... some text[/u][/noparse] tag to underline text.')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Use the [noparse][u]... some text[/u][/noparse] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering_with_html_entities(self):
        """ Test SkCode rendering with encoded HTML entities. """
        document_tree = parse_skcode('Use the [noparse][u]... &lt;some text&gt;[/u][/noparse] tag to underline text.')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Use the [noparse][u]... <some text>[/u][/noparse] tag to underline text.'
        self.assertEqual(expected_output, rendered_output)
