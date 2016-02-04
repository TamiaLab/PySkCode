"""
SkCode tree builder test code.
"""

import unittest

from skcode import parse_skcode
from skcode.tags import (TagOptions,
                         RootTagOptions,
                         TextTagOptions,
                         ErroneousTextTagOptions,
                         NewlineTagOptions)
from skcode.etree import RootTreeNode


class CustomTextTagOptions(TextTagOptions):
    """ Custom subclass of ``TextTagOptions`for tests. """


class CustomErroneousTextTagOptions(ErroneousTextTagOptions):
    """ Custom subclass of ``ErroneousTextTagOptions`for tests. """


class ParserTestCase(unittest.TestCase):
    """
    Tests suite for the parser high-level API.
    """

    def test_reject_private_tag_names(self):
        with self.assertRaises(ValueError) as e:
            parse_skcode('', recognized_tags={'_test': TagOptions()})
        self.assertEqual('Tag names starting with an underscore are reserved for internal use only.', str(e.exception))

    def test_no_text(self):
        document_tree = parse_skcode('')
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(0, len(document_tree.children))

        document_tree = parse_skcode('     ')
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(0, len(document_tree.children))

    def test_data_block(self):
        document_tree = parse_skcode('[test][i]Hello[test] world![/i][/test]',
                                     recognized_tags={'test': TagOptions(parse_embedded=False)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        code_block = document_tree.children[0]
        self.assertEqual(document_tree, code_block.root_tree_node)
        self.assertEqual(document_tree, code_block.parent)
        self.assertEqual('test', code_block.name)
        self.assertEqual({}, code_block.attrs)
        self.assertEqual('[i]Hello[test] world![/i]', code_block.content)
        self.assertEqual(0, len(code_block.children))
        self.assertEqual('[test]', code_block.source_open_tag)
        self.assertEqual('[/test]', code_block.source_close_tag)

    def test_data_block_swallow_newline(self):
        document_tree = parse_skcode('[test]\n\n[i]Hello[test] world![/i]\n[/test]',
                                     recognized_tags={'test': TagOptions(parse_embedded=False,
                                                                         swallow_trailing_newline=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        code_block = document_tree.children[0]
        self.assertEqual(document_tree, code_block.root_tree_node)
        self.assertEqual(document_tree, code_block.parent)
        self.assertEqual('test', code_block.name)
        self.assertEqual({}, code_block.attrs)
        self.assertEqual('\n[i]Hello[test] world![/i]\n', code_block.content)
        self.assertEqual(0, len(code_block.children))
        self.assertEqual('[test]', code_block.source_open_tag)
        self.assertEqual('[/test]', code_block.source_close_tag)

    def test_unknown_tag(self):
        document_tree = parse_skcode('[test][/test]', recognized_tags={})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(2, len(document_tree.children))
        open_error = document_tree.children[0]
        self.assertTrue(isinstance(open_error.opts, ErroneousTextTagOptions))
        self.assertEqual(document_tree, open_error.root_tree_node)
        self.assertEqual(document_tree, open_error.parent)
        self.assertEqual({}, open_error.attrs)
        self.assertEqual('[test]', open_error.content)
        self.assertEqual(0, len(open_error.children))
        self.assertEqual('', open_error.source_open_tag)
        self.assertEqual('', open_error.source_close_tag)
        close_error = document_tree.children[1]
        self.assertTrue(isinstance(close_error.opts, ErroneousTextTagOptions))
        self.assertEqual(document_tree, close_error.root_tree_node)
        self.assertEqual(document_tree, close_error.parent)
        self.assertEqual({}, close_error.attrs)
        self.assertEqual('[/test]', close_error.content)
        self.assertEqual(0, len(close_error.children))
        self.assertEqual('', close_error.source_open_tag)
        self.assertEqual('', close_error.source_close_tag)

    def test_unknown_tag_custom_error_opts(self):
        document_tree = parse_skcode('[test][/test]', recognized_tags={},
                                     erroneous_text_node_opts=CustomErroneousTextTagOptions())
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(2, len(document_tree.children))
        open_error = document_tree.children[0]
        self.assertTrue(isinstance(open_error.opts, CustomErroneousTextTagOptions))
        close_error = document_tree.children[1]
        self.assertTrue(isinstance(close_error.opts, CustomErroneousTextTagOptions))

    def test_unknown_tag_dropped(self):
        document_tree = parse_skcode('[test][/test]', recognized_tags={}, drop_unrecognized=True)
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(0, len(document_tree.children))

    def test_data(self):
        document_tree = parse_skcode('Foobar')
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertTrue(isinstance(child_node.opts, TextTagOptions))
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('Foobar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)

    def test_data_custom_text_opts(self):
        document_tree = parse_skcode('Foobar', text_node_opts=CustomTextTagOptions())
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertTrue(isinstance(child_node.opts, CustomTextTagOptions))
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('Foobar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)

    def test_newline(self):
        document_tree = parse_skcode('Foo\nbar')
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertTrue(isinstance(child_node.opts, TextTagOptions))
        self.assertEqual('Foo', child_node.content)
        child_node = document_tree.children[1]
        self.assertTrue(isinstance(child_node.opts, NewlineTagOptions))
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('\n', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        child_node = document_tree.children[2]
        self.assertTrue(isinstance(child_node.opts, TextTagOptions))
        self.assertEqual('bar', child_node.content)

    def test_newline_swallow(self):
        document_tree = parse_skcode('[test]\nbar[/test]',
                                     recognized_tags={'test': TagOptions(swallow_trailing_newline=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual(1, len(child_node.children))
        sub_child_node = child_node.children[0]
        self.assertTrue(isinstance(sub_child_node.opts, TextTagOptions))

    def test_newline_close(self):
        document_tree = parse_skcode('[test][test]\nfoobar',
                                     recognized_tags={'test': TagOptions(newline_closes=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(2, len(document_tree.children))
        child_node = document_tree.children[1]
        self.assertEqual('foobar', child_node.content)
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        sub_child_node = child_node.children[0]
        self.assertEqual('test', sub_child_node.name)
        self.assertEqual(1, len(sub_child_node.children))
        self.assertTrue(isinstance(sub_child_node.children[0].opts, NewlineTagOptions))

    def test_nesting_limit(self):
        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags={'test': TagOptions()},
                                     max_nesting_depth=5)
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))

        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags={'test': TagOptions()},
                                     max_nesting_depth=4)
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))

        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags={'test': TagOptions()},
                                     max_nesting_depth=3)
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        child_node = child_node.children[0]
        self.assertTrue(isinstance(child_node.opts, ErroneousTextTagOptions))

    def test_same_tag_close(self):
        document_tree = parse_skcode('[test][test][test]',
                                     recognized_tags={'test': TagOptions(same_tag_closes=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(3, len(document_tree.children))

    def test_close_inline(self):
        document_tree = parse_skcode('[inline][inline][test]',
                                     recognized_tags={'inline': TagOptions(inline=True, close_inlines=False),
                                                      'test': TagOptions(inline=False, close_inlines=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(2, len(document_tree.children))
        self.assertEqual('inline', document_tree.children[0].name)
        self.assertEqual('test', document_tree.children[1].name)

    def test_standalone_tag(self):
        document_tree = parse_skcode('[test][test][test]',
                                     recognized_tags={'test': TagOptions(standalone=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(3, len(document_tree.children))

    def test_bad_closing(self):
        document_tree = parse_skcode('[/test]', recognized_tags={'test': TagOptions()})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        self.assertTrue(isinstance(document_tree.children[0].opts, ErroneousTextTagOptions))

    def test_bad_closing_2(self):
        document_tree = parse_skcode('[inline][/test]', recognized_tags={'test': TagOptions(),
                                                                         'inline': TagOptions()})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        self.assertTrue(isinstance(document_tree.children[0].children[0].opts, ErroneousTextTagOptions))

    def test_self_closing_tag(self):
        document_tree = parse_skcode('[test/]',
                                     recognized_tags={'test': TagOptions(standalone=True)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        self.assertFalse(isinstance(document_tree.children[0].opts, ErroneousTextTagOptions))

    def test_self_closing_tag_2(self):
        document_tree = parse_skcode('[test/]',
                                     recognized_tags={'test': TagOptions(standalone=False)})
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(1, len(document_tree.children))
        self.assertTrue(isinstance(document_tree.children[0].opts, ErroneousTextTagOptions))

    def test_texturize_unclosed(self):
        document_tree = parse_skcode('[test][test][test]',
                                     recognized_tags={'test': TagOptions()},
                                     texturize_unclosed_tags=True)
        self.assertTrue(isinstance(document_tree, RootTreeNode))
        self.assertEqual(3, len(document_tree.children))
        self.assertTrue(isinstance(document_tree.children[0].opts, ErroneousTextTagOptions))
        self.assertTrue(isinstance(document_tree.children[1].opts, ErroneousTextTagOptions))
        self.assertTrue(isinstance(document_tree.children[2].opts, ErroneousTextTagOptions))
