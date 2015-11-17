"""
SkCode electronic tag test code.
"""

import unittest

from skcode import (parse_skcode,
                    render_to_html,
                    render_to_text,
                    render_to_skcode)
from skcode.tags import (NotNotationTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class NotNotationTagtestCase(unittest.TestCase):
    """ Tests suite for the NOT notation tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('not', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['not'], NotNotationTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = NotNotationTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        document_tree = parse_skcode('Pull the [not]RESET[/not] pin low to reset.')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Pull the <span style="text-decoration:overline; text-transform: uppercase;">RESET</span> pin low to reset.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Pull the [not]RESET[/not] pin low to reset.')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Pull the /RESET pin low to reset.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_auto_upper(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Pull the [not]reset[/not] pin low to reset.')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Pull the /RESET pin low to reset.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Pull the [not]RESET[/not] pin low to reset.')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Pull the [not]RESET[/not] pin low to reset.'
        self.assertEqual(expected_output, rendered_output)
