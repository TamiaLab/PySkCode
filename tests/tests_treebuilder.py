"""
SkCode tree builder test code.
"""

import unittest

from skcode import parse_skcode
from skcode.tags import TextTreeNode, NewlineTreeNode
from skcode.etree import TreeNode, RootTreeNode


class CustomTextTreeNode(TextTreeNode):
    """ Custom text tree node """


class DummyTreeNode(TreeNode):
    """ Dummy tag options for tests """

    canonical_tag_name = 'test'

    def render_html(self, inner_html, **kwargs):
        return 'TEST'

    def render_text(self, inner_text, **kwargs):
        return 'TEST'


def get_dummy_node(**kwargs):
    """
    Get a dummy node class witht the given kwargs set as class attribute
    """
    return type('CustomDummyTreeNode', (DummyTreeNode, ), kwargs)


class ParserTestCase(unittest.TestCase):
    """
    Tests suite for the parser high-level API.
    """

    def test_new_tags_declaration_style(self):
        """ Test if the new tags declarations style (list based) works. """
        known_tags = (get_dummy_node(alias_tag_names = ('alias', )), )
        document_tree = parse_skcode('[test][/test] [alias][/alias]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        tree_node = document_tree.children[0]
        self.assertEqual(document_tree, tree_node.root_tree_node)
        self.assertEqual(document_tree, tree_node.parent)
        self.assertEqual('test', tree_node.name)
        self.assertIsInstance(tree_node, DummyTreeNode)
        self.assertEqual({}, tree_node.attrs)
        self.assertEqual('', tree_node.content)
        self.assertEqual(0, len(tree_node.children))
        self.assertEqual('[test]', tree_node.source_open_tag)
        self.assertEqual('[/test]', tree_node.source_close_tag)
        tree_node = document_tree.children[1]
        self.assertEqual(document_tree, tree_node.root_tree_node)
        self.assertEqual(document_tree, tree_node.parent)
        self.assertIsNone(tree_node.name)
        self.assertIsInstance(tree_node, TextTreeNode)
        self.assertEqual({}, tree_node.attrs)
        self.assertEqual(' ', tree_node.content)
        self.assertEqual(0, len(tree_node.children))
        self.assertEqual('', tree_node.source_open_tag)
        self.assertEqual('', tree_node.source_close_tag)
        tree_node = document_tree.children[2]
        self.assertEqual(document_tree, tree_node.root_tree_node)
        self.assertEqual(document_tree, tree_node.parent)
        self.assertEqual('alias', tree_node.name)
        self.assertIsInstance(tree_node, DummyTreeNode)
        self.assertEqual({}, tree_node.attrs)
        self.assertEqual('', tree_node.content)
        self.assertEqual(0, len(tree_node.children))
        self.assertEqual('[alias]', tree_node.source_open_tag)
        self.assertEqual('[/alias]', tree_node.source_close_tag)

    def test_no_text(self):
        document_tree = parse_skcode('')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(0, len(document_tree.children))

        document_tree = parse_skcode('     ')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(0, len(document_tree.children))

    def test_data_block(self):
        document_tree = parse_skcode('[test][i]Hello[test] world![/i][/test]',
                                     recognized_tags=(get_dummy_node(parse_embedded=False), ))
        self.assertIsInstance(document_tree, RootTreeNode)
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

    def test_unknown_tag(self):
        document_tree = parse_skcode('[test][/test]', recognized_tags=())
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(2, len(document_tree.children))
        open_error = document_tree.children[0]
        self.assertIsInstance(open_error, TextTreeNode)
        self.assertEqual(document_tree, open_error.root_tree_node)
        self.assertEqual(document_tree, open_error.parent)
        self.assertEqual({}, open_error.attrs)
        self.assertEqual('', open_error.content)
        self.assertEqual(0, len(open_error.children))
        self.assertEqual('[test]', open_error.source_open_tag)
        self.assertEqual('', open_error.source_close_tag)
        close_error = document_tree.children[1]
        self.assertIsInstance(close_error, TextTreeNode)
        self.assertEqual(document_tree, close_error.root_tree_node)
        self.assertEqual(document_tree, close_error.parent)
        self.assertEqual({}, close_error.attrs)
        self.assertEqual('', close_error.content)
        self.assertEqual(0, len(close_error.children))
        self.assertEqual('[/test]', close_error.source_open_tag)
        self.assertEqual('', close_error.source_close_tag)

    def test_data(self):
        document_tree = parse_skcode('Foobar')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('Foobar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)

    def test_data_custom_text_opts(self):
        document_tree = parse_skcode('Foobar', text_node_cls=CustomTextTreeNode)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, CustomTextTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('Foobar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)

    def test_newline(self):
        document_tree = parse_skcode('Foo\nbar')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual('Foo', child_node.content)
        child_node = document_tree.children[1]
        self.assertIsInstance(child_node, NewlineTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        child_node = document_tree.children[2]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual('bar', child_node.content)

    def test_newline_close(self):
        document_tree = parse_skcode('[test][test]\nfoobar',
                                     recognized_tags=(get_dummy_node(newline_closes=True), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(2, len(document_tree.children))
        child_node = document_tree.children[1]
        self.assertEqual('foobar', child_node.content)
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        sub_child_node = child_node.children[0]
        self.assertEqual('test', sub_child_node.name)
        self.assertEqual(1, len(sub_child_node.children))
        self.assertIsInstance(sub_child_node.children[0], NewlineTreeNode)

    def test_nesting_limit(self):
        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags=(DummyTreeNode, ),
                                     max_nesting_depth=5)
        self.assertIsInstance(document_tree, RootTreeNode)
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
                                     recognized_tags=(DummyTreeNode,),
                                     max_nesting_depth=4)
        self.assertIsInstance(document_tree, RootTreeNode)
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
                                     recognized_tags=(DummyTreeNode,),
                                     max_nesting_depth=3)
        self.assertIsInstance(document_tree, RootTreeNode)
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
        self.assertIsInstance(child_node, TextTreeNode)

    def test_same_tag_close(self):
        document_tree = parse_skcode('[test][test][test]',
                                     recognized_tags=(get_dummy_node(same_tag_closes=True), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))

    def test_close_inline(self):
        document_tree = parse_skcode('[inline][inline][test]',
                                     recognized_tags=(get_dummy_node(canonical_tag_name='inline',
                                                                     inline=True, close_inlines=False),
                                                      get_dummy_node(inline=False, close_inlines=True)))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(2, len(document_tree.children))
        self.assertEqual('inline', document_tree.children[0].name)
        self.assertEqual('test', document_tree.children[1].name)

    def test_standalone_tag(self):
        document_tree = parse_skcode('[test][test][test]',
                                     recognized_tags=(get_dummy_node(standalone=True), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))

    def test_bad_closing(self):
        document_tree = parse_skcode('[/test]', recognized_tags=(DummyTreeNode, ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        self.assertIsInstance(document_tree.children[0], TextTreeNode)

    def test_bad_closing_2(self):
        document_tree = parse_skcode('[inline][/test]', recognized_tags=(get_dummy_node(canonical_tag_name='inline'),
                                                                         DummyTreeNode))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        self.assertIsInstance(document_tree.children[0].children[0], TextTreeNode)

    def test_self_closing_tag(self):
        document_tree = parse_skcode('[test/]',
                                     recognized_tags=(get_dummy_node(standalone=True), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        self.assertFalse(isinstance(document_tree.children[0], TextTreeNode))

    def test_self_closing_tag_2(self):
        document_tree = parse_skcode('[test/]',
                                     recognized_tags=(get_dummy_node(standalone=False), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        self.assertIsInstance(document_tree.children[0], TextTreeNode)

    def test_weak_parent_close(self):
        document_tree = parse_skcode('[test][foobar][/test]',
                                     recognized_tags=(DummyTreeNode,
                                                      get_dummy_node(canonical_tag_name='foobar',
                                                                     weak_parent_close=True)))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(1, len(test_node.children))
        foobar_node = test_node.children[0]
        self.assertIsInstance(foobar_node, DummyTreeNode)
        self.assertEqual('foobar', foobar_node.name)
        self.assertEqual(0, len(foobar_node.children))

    def test_after_building_unclosed_weak_parent_close(self):
        document_tree = parse_skcode('[test]', recognized_tags=(get_dummy_node(weak_parent_close=True), ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(0, len(test_node.children))
