"""
SkCode acronyms tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    BoldTextTreeNode,
    ItalicTextTreeNode,
    StrikeTextTreeNode,
    UnderlineTextTreeNode,
    SubscriptTextTreeNode,
    SupscriptTextTreeNode,
    PreTextTreeNode,
    CiteTextTreeNode,
    InlineCodeTextTreeNode,
    InlineSpoilerTextTreeNode,
    KeyboardTextTreeNode,
    HighlightTextTreeNode,
    SmallTextTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.tags.textformatting import InlineWrappingTreeNode


class TestInlineWrappingTreeNode(InlineWrappingTreeNode):
    """ Test class """

    wrapping_format = 'foo{}bar'


class InlineWrappingTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the inline code tag module. """

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(InlineWrappingTreeNode.newline_closes)
        self.assertFalse(InlineWrappingTreeNode.same_tag_closes)
        self.assertFalse(InlineWrappingTreeNode.weak_parent_close)
        self.assertFalse(InlineWrappingTreeNode.standalone)
        self.assertTrue(InlineWrappingTreeNode.parse_embedded)
        self.assertTrue(InlineWrappingTreeNode.inline)
        self.assertFalse(InlineWrappingTreeNode.close_inlines)
        self.assertFalse(InlineWrappingTreeNode.make_paragraphs_here)
        self.assertIsNone(InlineWrappingTreeNode.wrapping_format)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TestInlineWrappingTreeNode, content='test')
        output_result = tree_node.render_html('test')
        self.assertEqual('footestbar', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', TestInlineWrappingTreeNode, content='test')
        output_result = tree_node.render_text('test')
        self.assertEqual('test', output_result)


class BoldTextTagTestCase(unittest.TestCase):
    """ Tests suite for the bold text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(BoldTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(BoldTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<strong>{}</strong>', BoldTextTreeNode.wrapping_format)
        self.assertEqual('b', BoldTextTreeNode.canonical_tag_name)
        self.assertEqual(('bold', 'strong'), BoldTextTreeNode.alias_tag_names)


class ItalicTextTagTestCase(unittest.TestCase):
    """ Tests suite for the italic text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(ItalicTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(ItalicTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<em>{}</em>', ItalicTextTreeNode.wrapping_format)
        self.assertEqual('i', ItalicTextTreeNode.canonical_tag_name)
        self.assertEqual(('italic', 'em'), ItalicTextTreeNode.alias_tag_names)


class StrikeTextTagTestCase(unittest.TestCase):
    """ Tests suite for the strike text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(StrikeTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(StrikeTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<del>{}</del>', StrikeTextTreeNode.wrapping_format)
        self.assertEqual('s', StrikeTextTreeNode.canonical_tag_name)
        self.assertEqual(('strike', 'del'), StrikeTextTreeNode.alias_tag_names)


class UnderlineTextTagTestCase(unittest.TestCase):
    """ Tests suite for the underline text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(UnderlineTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(UnderlineTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<ins>{}</ins>', UnderlineTextTreeNode.wrapping_format)
        self.assertEqual('u', UnderlineTextTreeNode.canonical_tag_name)
        self.assertEqual(('underline', 'ins'), UnderlineTextTreeNode.alias_tag_names)


class SubscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the italic text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(SubscriptTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SubscriptTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<sub>{}</sub>', SubscriptTextTreeNode.wrapping_format)
        self.assertEqual('sub', SubscriptTextTreeNode.canonical_tag_name)
        self.assertEqual((), SubscriptTextTreeNode.alias_tag_names)


class SupscriptTextTagTestCase(unittest.TestCase):
    """ Tests suite for the supscript text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(SupscriptTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SupscriptTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<sup>{}</sup>', SupscriptTextTreeNode.wrapping_format)
        self.assertEqual('sup', SupscriptTextTreeNode.canonical_tag_name)
        self.assertEqual((), SupscriptTextTreeNode.alias_tag_names)


class PreTextTagTestCase(unittest.TestCase):
    """ Tests suite for the monospaced text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(PreTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(PreTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<pre>{}</pre>', PreTextTreeNode.wrapping_format)
        self.assertEqual('pre', PreTextTreeNode.canonical_tag_name)
        self.assertEqual((), PreTextTreeNode.alias_tag_names)


class CiteTextTagTestCase(unittest.TestCase):
    """ Tests suite for the cite text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(CiteTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)
        
    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(CiteTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<cite>{}</cite>', CiteTextTreeNode.wrapping_format)
        self.assertEqual('cite', CiteTextTreeNode.canonical_tag_name)
        self.assertEqual((), CiteTextTreeNode.alias_tag_names)


class InlineCodeTextTagTestCase(unittest.TestCase):
    """ Tests suite for the inline code tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(InlineCodeTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(InlineCodeTextTreeNode.newline_closes)
        self.assertFalse(InlineCodeTextTreeNode.same_tag_closes)
        self.assertFalse(InlineCodeTextTreeNode.weak_parent_close)
        self.assertFalse(InlineCodeTextTreeNode.standalone)
        self.assertFalse(InlineCodeTextTreeNode.parse_embedded)
        self.assertTrue(InlineCodeTextTreeNode.inline)
        self.assertFalse(InlineCodeTextTreeNode.close_inlines)
        self.assertEqual('icode', InlineCodeTextTreeNode.canonical_tag_name)
        self.assertEqual((), InlineCodeTextTreeNode.alias_tag_names)
        self.assertFalse(InlineCodeTextTreeNode.make_paragraphs_here)
        self.assertEqual('<code>{content}</code>', InlineCodeTextTreeNode.html_render_template)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='test')
        output_result = tree_node.render_html('foobar')
        self.assertEqual('<code>test</code>', output_result)

    def test_render_html_with_brackets(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='[test]')
        output_result = tree_node.render_html('foobar')
        self.assertEqual('<code>[test]</code>', output_result)

    def test_render_html_with_html_entities(self):
        """ Test the ``render_html`` method with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='<test>')
        output_result = tree_node.render_html('foobar')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_html_with_encoded_html_entities(self):
        """ Test the ``render_html`` method with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='&lt;test&gt;')
        output_result = tree_node.render_html('foobar')
        self.assertEqual('<code>&lt;test&gt;</code>', output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='test')
        output_result = tree_node.render_text('foobar')
        self.assertEqual('test', output_result)

    def test_render_text_with_brackets(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='[test]')
        output_result = tree_node.render_text('foobar')
        self.assertEqual('[test]', output_result)

    def test_render_text_with_html_entities(self):
        """ Test the ``render_text`` method with HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='<test>')
        output_result = tree_node.render_text('foobar')
        self.assertEqual('<test>', output_result)

    def test_render_text_with_encoded_html_entities(self):
        """ Test the ``render_text`` method with encoded HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('icode', InlineCodeTextTreeNode, content='&lt;test&gt;')
        output_result = tree_node.render_text('foobar')
        self.assertEqual('<test>', output_result)


class InlineSpoilerTextTagTestCase(unittest.TestCase):
    """ Tests suite for the inline spoiler text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(InlineSpoilerTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(InlineSpoilerTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<span class="ispoiler">{}</span>', InlineSpoilerTextTreeNode.wrapping_format)
        self.assertEqual('ispoiler', InlineSpoilerTextTreeNode.canonical_tag_name)
        self.assertEqual((), InlineSpoilerTextTreeNode.alias_tag_names)


class KeyboardTextTagTestCase(unittest.TestCase):
    """ Tests suite for the keyboard shortcut text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(KeyboardTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(KeyboardTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<kbd>{}</kbd>', KeyboardTextTreeNode.wrapping_format)
        self.assertEqual('kbd', KeyboardTextTreeNode.canonical_tag_name)
        self.assertEqual(('keyboard', ), KeyboardTextTreeNode.alias_tag_names)


class HighlightTextTagTestCase(unittest.TestCase):
    """ Tests suite for the highlighted text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(HighlightTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(HighlightTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<mark>{}</mark>', HighlightTextTreeNode.wrapping_format)
        self.assertEqual('mark', HighlightTextTreeNode.canonical_tag_name)
        self.assertEqual(('glow', 'highlight'), HighlightTextTreeNode.alias_tag_names)


class SmallTextTagTestCase(unittest.TestCase):
    """ Tests suite for the small text tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(SmallTextTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(SmallTextTreeNode, InlineWrappingTreeNode))
        self.assertEqual('<small>{}</small>', SmallTextTreeNode.wrapping_format)
        self.assertEqual('small', SmallTextTreeNode.canonical_tag_name)
        self.assertEqual((), SmallTextTreeNode.alias_tag_names)
