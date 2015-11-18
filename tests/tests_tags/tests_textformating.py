"""
SkCode acronyms tag test code.
"""

import unittest

from skcode import (parse_skcode,
                    render_to_html,
                    render_to_text,
                    render_to_skcode)
from skcode.etree import TreeNode
from skcode.tags import (BoldTextTagOptions,
                         ItalicTextTagOptions,
                         StrikeTextTagOptions,
                         UnderlineTextTagOptions,
                         SubscriptTextTagOptions,
                         SupscriptTextTagOptions,
                         PreTextTagOptions,
                         InlineCodeTextTagOptions,
                         InlineSpoilerTextTagOptions,
                         KeyboardTextTagOptions,
                         HighlightTextTagOptions,
                         SmallTextTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class BoldTextTagTestCase(unittest.TestCase):
    """ Tests suite for the bold text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('b', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['b'], BoldTextTagOptions)
        self.assertIn('bold', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['bold'], BoldTextTagOptions)
        self.assertIn('strong', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['strong'], BoldTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = BoldTextTagOptions()
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
        document_tree = parse_skcode('Run this test [b]ASAP[/b].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <strong>ASAP</strong>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [b]ASAP[/b].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [b]ASAP[/b].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [b]ASAP[/b].'
        self.assertEqual(expected_output, rendered_output)


class ItalicTextTagTestCase(unittest.TestCase):
    """ Tests suite for the italic text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('i', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['i'], ItalicTextTagOptions)
        self.assertIn('italic', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['italic'], ItalicTextTagOptions)
        self.assertIn('em', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['em'], ItalicTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ItalicTextTagOptions()
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
        document_tree = parse_skcode('Run this test [i]ASAP[/i].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <em>ASAP</em>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [i]ASAP[/i].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [i]ASAP[/i].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [i]ASAP[/i].'
        self.assertEqual(expected_output, rendered_output)


class StrikeTextTagTestCase(unittest.TestCase):
    """ Tests suite for the strike text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('s', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['s'], StrikeTextTagOptions)
        self.assertIn('strike', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['strike'], StrikeTextTagOptions)
        self.assertIn('del', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['del'], StrikeTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = StrikeTextTagOptions()
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
        document_tree = parse_skcode('Run this test [s]ASAP[/s].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <del>ASAP</del>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [s]ASAP[/s].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [s]ASAP[/s].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [s]ASAP[/s].'
        self.assertEqual(expected_output, rendered_output)


class UnderlineTextTagTestCase(unittest.TestCase):
    """ Tests suite for the underline text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('u', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['u'], UnderlineTextTagOptions)
        self.assertIn('underline', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['underline'], UnderlineTextTagOptions)
        self.assertIn('ins', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ins'], UnderlineTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = UnderlineTextTagOptions()
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
        document_tree = parse_skcode('Run this test [u]ASAP[/u].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <ins>ASAP</ins>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [u]ASAP[/u].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [u]ASAP[/u].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [u]ASAP[/u].'
        self.assertEqual(expected_output, rendered_output)


class SubscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the italic text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('sub', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['sub'], SubscriptTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = SubscriptTextTagOptions()
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
        document_tree = parse_skcode('Run this test [sub]ASAP[/sub].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <sub>ASAP</sub>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [sub]ASAP[/sub].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [sub]ASAP[/sub].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [sub]ASAP[/sub].'
        self.assertEqual(expected_output, rendered_output)


class SupscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the supscript text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('sup', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['sup'], SupscriptTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = SupscriptTextTagOptions()
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
        document_tree = parse_skcode('Run this test [sup]ASAP[/sup].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <sup>ASAP</sup>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [sup]ASAP[/sup].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [sup]ASAP[/sup].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [sup]ASAP[/sup].'
        self.assertEqual(expected_output, rendered_output)


class PreTextTagTestCase(unittest.TestCase):
    """ Tests suite for the monospaced text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('pre', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['pre'], PreTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = PreTextTagOptions()
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
        document_tree = parse_skcode('Run this test [pre]ASAP[/pre].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <pre>ASAP</pre>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [pre]ASAP[/pre].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [pre]ASAP[/pre].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [pre]ASAP[/pre].'
        self.assertEqual(expected_output, rendered_output)


class InlineCodeTextTagTestCase(unittest.TestCase):
    """ Tests suite for the inline code tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('icode', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['icode'], InlineCodeTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = InlineCodeTextTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertFalse(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='test')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<code>test</code>', output_result)

    def test_render_html_with_brackets(self):
        """ Test the ``render_html`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='[test]')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<code>[test]</code>', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='<test>')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='&lt;test&gt;')
        output_result = opts.render_html(tree_node, '')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='test')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('test', output_result)

    def test_render_text_with_brackets(self):
        """ Test the ``render_text`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='[test]')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('[test]', output_result)

    def test_render_text_with_html_entities(self):
        """ Test the ``render_text`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='&lt;test&gt;')
        output_result = opts.render_text(tree_node, '')
        self.assertEqual('<test>', output_result)

    def test_render_skcode(self):
        """ Test the ``render_skcode`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='test')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('[icode]test[/icode]', output_result)

    def test_render_skcode_with_brackets(self):
        """ Test the ``render_skcode`` method. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='[test]')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('[icode][test][/icode]', output_result)

    def test_render_skcode_with_html_entities(self):
        """ Test the ``render_skcode`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        tree_node = TreeNode(None, 'icode', opts, content='&lt;test&gt;')
        output_result = opts.render_skcode(tree_node, '')
        self.assertEqual('[icode]<test>[/icode]', output_result)


class InlineSpoilerTextTagTestCase(unittest.TestCase):
    """ Tests suite for the inline spoiler text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('ispoiler', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ispoiler'], InlineSpoilerTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = InlineSpoilerTextTagOptions()
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
        document_tree = parse_skcode('Run this test [ispoiler]ASAP[/ispoiler].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <span class="ispoiler">ASAP</span>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [ispoiler]ASAP[/ispoiler].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [ispoiler]ASAP[/ispoiler].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [ispoiler]ASAP[/ispoiler].'
        self.assertEqual(expected_output, rendered_output)


class KeyboardTextTagTestCase(unittest.TestCase):
    """ Tests suite for the keyboard shortcut text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('kbd', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['kbd'], KeyboardTextTagOptions)
        self.assertIn('keyboard', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['keyboard'], KeyboardTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = KeyboardTextTagOptions()
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
        document_tree = parse_skcode('Run this test [kbd]ASAP[/kbd].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <kbd>ASAP</kbd>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [kbd]ASAP[/kbd].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [kbd]ASAP[/kbd].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [kbd]ASAP[/kbd].'
        self.assertEqual(expected_output, rendered_output)


class HighlightTextTagTestCase(unittest.TestCase):
    """ Tests suite for the highlighted text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('glow', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['glow'], HighlightTextTagOptions)
        self.assertIn('highlight', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['highlight'], HighlightTextTagOptions)
        self.assertIn('mark', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['mark'], HighlightTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = HighlightTextTagOptions()
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
        document_tree = parse_skcode('Run this test [mark]ASAP[/mark].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <mark>ASAP</mark>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [mark]ASAP[/mark].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [mark]ASAP[/mark].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [mark]ASAP[/mark].'
        self.assertEqual(expected_output, rendered_output)


class SmallTextTagTestCase(unittest.TestCase):
    """ Tests suite for the small text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('small', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['small'], SmallTextTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = SmallTextTagOptions()
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
        document_tree = parse_skcode('Run this test [small]ASAP[/small].')
        rendered_output = render_to_html(document_tree)
        expected_output = 'Run this test <small>ASAP</small>.'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        document_tree = parse_skcode('Run this test [small]ASAP[/small].')
        rendered_output = render_to_text(document_tree)
        expected_output = 'Run this test ASAP.'
        self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        document_tree = parse_skcode('Run this test [small]ASAP[/small].')
        rendered_output = render_to_skcode(document_tree)
        expected_output = 'Run this test [small]ASAP[/small].'
        self.assertEqual(expected_output, rendered_output)
