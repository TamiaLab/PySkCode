"""
SkCode acronyms tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (InlineWrappingTagOptions,
                         RootTagOptions,
                         BoldTextTagOptions,
                         ItalicTextTagOptions,
                         StrikeTextTagOptions,
                         UnderlineTextTagOptions,
                         SubscriptTextTagOptions,
                         SupscriptTextTagOptions,
                         PreTextTagOptions,
                         CiteTextTagOptions,
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

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(BoldTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<strong>%s</strong>', BoldTextTagOptions().wrapping_format)
        self.assertEqual('b', BoldTextTagOptions().canonical_tag_name)
        self.assertEqual(('bold', 'strong'), BoldTextTagOptions().alias_tag_names)


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

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(ItalicTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<em>%s</em>', ItalicTextTagOptions().wrapping_format)
        self.assertEqual('i', ItalicTextTagOptions().canonical_tag_name)
        self.assertEqual(('italic', 'em'), ItalicTextTagOptions().alias_tag_names)


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

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(StrikeTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<del>%s</del>', StrikeTextTagOptions().wrapping_format)
        self.assertEqual('s', StrikeTextTagOptions().canonical_tag_name)
        self.assertEqual(('strike', 'del'), StrikeTextTagOptions().alias_tag_names)


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

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(UnderlineTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<ins>%s</ins>', UnderlineTextTagOptions().wrapping_format)
        self.assertEqual('u', UnderlineTextTagOptions().canonical_tag_name)
        self.assertEqual(('underline', 'ins'), UnderlineTextTagOptions().alias_tag_names)


class SubscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the italic text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('sub', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['sub'], SubscriptTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SubscriptTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<sub>%s</sub>', SubscriptTextTagOptions().wrapping_format)
        self.assertEqual('sub', SubscriptTextTagOptions().canonical_tag_name)
        self.assertEqual((), SubscriptTextTagOptions().alias_tag_names)


class SupscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the supscript text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('sup', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['sup'], SupscriptTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SupscriptTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<sup>%s</sup>', SupscriptTextTagOptions().wrapping_format)
        self.assertEqual('sup', SupscriptTextTagOptions().canonical_tag_name)
        self.assertEqual((), SupscriptTextTagOptions().alias_tag_names)


class PreTextTagTestCase(unittest.TestCase):
    """ Tests suite for the monospaced text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('pre', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['pre'], PreTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(PreTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<pre>%s</pre>', PreTextTagOptions().wrapping_format)
        self.assertEqual('pre', PreTextTagOptions().canonical_tag_name)
        self.assertEqual((), PreTextTagOptions().alias_tag_names)


class CiteTextTagTestCase(unittest.TestCase):
    """ Tests suite for the cite text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('cite', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['cite'], CiteTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(CiteTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<cite>%s</cite>', CiteTextTagOptions().wrapping_format)
        self.assertEqual('cite', CiteTextTagOptions().canonical_tag_name)
        self.assertEqual((), CiteTextTagOptions().alias_tag_names)


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
        self.assertEqual('icode', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('<code>{content}</code>', opts.html_render_template)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='test')
        output_result = opts.render_html(tree_node, 'foobar')
        self.assertEqual('<code>test</code>', output_result)

    def test_render_html_with_brackets(self):
        """ Test the ``render_html`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='[test]')
        output_result = opts.render_html(tree_node, 'foobar')
        self.assertEqual('<code>[test]</code>', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='<test>')
        output_result = opts.render_html(tree_node, 'foobar')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='&lt;test&gt;')
        output_result = opts.render_html(tree_node, 'foobar')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='test')
        output_result = opts.render_text(tree_node, 'foobar')
        self.assertEqual('test', output_result)

    def test_render_text_with_brackets(self):
        """ Test the ``render_text`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='[test]')
        output_result = opts.render_text(tree_node, 'foobar')
        self.assertEqual('[test]', output_result)

    def test_render_text_with_html_entities(self):
        """ Test the ``render_text`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='<test>')
        output_result = opts.render_text(tree_node, 'foobar')
        self.assertEqual('<test>', output_result)

    def test_render_text_with_encoded_html_entities(self):
        """ Test the ``render_text`` method with encoded HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='&lt;test&gt;')
        output_result = opts.render_text(tree_node, 'foobar')
        self.assertEqual('<test>', output_result)

    def test_get_skcode_inner_content(self):
        """ Test the ``get_skcode_inner_content`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='test')
        output_result = opts.get_skcode_inner_content(tree_node, 'foobar')
        self.assertEqual('test', output_result)

    def test_get_skcode_inner_content_with_brackets(self):
        """ Test the ``render_skcode`` method. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='[test]')
        output_result = opts.get_skcode_inner_content(tree_node, 'foobar')
        self.assertEqual('[test]', output_result)

    def test_get_skcode_inner_content_with_html_entities(self):
        """ Test the ``get_skcode_inner_content`` method with HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='<test>')
        output_result = opts.get_skcode_inner_content(tree_node, 'foobar')
        self.assertEqual('<test>', output_result)

    def test_get_skcode_inner_content_with_encoded_html_entities(self):
        """ Test the ``get_skcode_inner_content`` method with encoded HTML entities. """
        opts = InlineCodeTextTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('icode', opts, content='&lt;test&gt;')
        output_result = opts.get_skcode_inner_content(tree_node, 'foobar')
        self.assertEqual('<test>', output_result)


class InlineSpoilerTextTagTestCase(unittest.TestCase):
    """ Tests suite for the inline spoiler text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('ispoiler', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ispoiler'], InlineSpoilerTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(InlineSpoilerTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('ispoiler', InlineSpoilerTextTagOptions().css_class_name)
        self.assertEqual('<span class="{class_name}">%s</span>', InlineSpoilerTextTagOptions().html_render_template)
        self.assertEqual('<span class="ispoiler">%s</span>', InlineSpoilerTextTagOptions().wrapping_format)
        self.assertEqual('ispoiler', InlineSpoilerTextTagOptions().canonical_tag_name)
        self.assertEqual((), InlineSpoilerTextTagOptions().alias_tag_names)

    def test_subclassing_custom_css(self):
        """ Test super class """
        self.assertTrue(issubclass(InlineSpoilerTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<span class="custom_css">%s</span>',
                         InlineSpoilerTextTagOptions(css_class_name='custom_css').wrapping_format)


class KeyboardTextTagTestCase(unittest.TestCase):
    """ Tests suite for the keyboard shortcut text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('kbd', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['kbd'], KeyboardTextTagOptions)
        self.assertIn('keyboard', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['keyboard'], KeyboardTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(KeyboardTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<kbd>%s</kbd>', KeyboardTextTagOptions().wrapping_format)
        self.assertEqual('kbd', KeyboardTextTagOptions().canonical_tag_name)
        self.assertEqual(('keyboard', ), KeyboardTextTagOptions().alias_tag_names)


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

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(HighlightTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<mark>%s</mark>', HighlightTextTagOptions().wrapping_format)
        self.assertEqual('mark', HighlightTextTagOptions().canonical_tag_name)
        self.assertEqual(('glow', 'highlight'), HighlightTextTagOptions().alias_tag_names)


class SmallTextTagTestCase(unittest.TestCase):
    """ Tests suite for the small text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('small', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['small'], SmallTextTagOptions)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SmallTextTagOptions, InlineWrappingTagOptions))
        self.assertEqual('<small>%s</small>', SmallTextTagOptions().wrapping_format)
        self.assertEqual('small', SmallTextTagOptions().canonical_tag_name)
        self.assertEqual((), SmallTextTagOptions().alias_tag_names)
