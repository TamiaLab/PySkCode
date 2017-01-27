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


def get_dummy_node(**kwargs):
    """
    Get a dummy node class with the given kwargs set as class attribute
    """
    return type('CustomDummyTreeNode', (DummyTreeNode, ), kwargs)


class ParserTestCase(unittest.TestCase):
    """
    Tests suite for the parser high-level API.
    """

    def test_new_tags_declaration_style(self):
        """ Test if the new tags declarations style (list based) works """
        known_tags = (
            get_dummy_node(alias_tag_names=('alias', )),
        )
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
        self.assertEqual('', tree_node.error_message)
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
        self.assertEqual('', tree_node.error_message)
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
        self.assertEqual('', tree_node.error_message)

    def test_no_text(self):
        """ Test the tree builder with no input text """
        document_tree = parse_skcode('')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(0, len(document_tree.children))
        document_tree = parse_skcode('     ')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(0, len(document_tree.children))

    def test_data_block(self):
        """ Test the tree builder with data block tag (``parse_embedded=False``) """
        known_tags = (
            get_dummy_node(parse_embedded=False),
        )
        document_tree = parse_skcode('[test][i]Hello[test] world![/i][/test]', recognized_tags=known_tags)
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
        self.assertEqual('', code_block.error_message)

    def test_unknown_tag(self):
        """ Test the tree builder with an unknown tag name """
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
        self.assertEqual('Unknown tag name', open_error.error_message)
        close_error = document_tree.children[1]
        self.assertIsInstance(close_error, TextTreeNode)
        self.assertEqual(document_tree, close_error.root_tree_node)
        self.assertEqual(document_tree, close_error.parent)
        self.assertEqual({}, close_error.attrs)
        self.assertEqual('', close_error.content)
        self.assertEqual(0, len(close_error.children))
        self.assertEqual('[/test]', close_error.source_open_tag)
        self.assertEqual('', close_error.source_close_tag)
        self.assertEqual('Unknown tag name', close_error.error_message)

    def test_data(self):
        """ Test the tree builder with some raw text data """
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
        self.assertEqual('', child_node.error_message)

    def test_data_custom_text_cls(self):
        """ Test the tree builder with some raw text data and a custom text node class """
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
        self.assertEqual('', child_node.error_message)

    def test_newline(self):
        """ Test the tree builder with some newlines """
        document_tree = parse_skcode('Foo\nbar')
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('Foo', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[1]
        self.assertIsInstance(child_node, NewlineTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[2]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('bar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)

    def test_newline_close(self):
        """ Test the tree builder handle ``newline_closes=True`` when handling a newline """
        known_tags = (
            get_dummy_node(newline_closes=True),
        )
        document_tree = parse_skcode('[test][test]\nfoobar', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('[test]', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)
        sub_child_node = child_node.children[0]
        self.assertEqual(document_tree, sub_child_node.root_tree_node)
        self.assertEqual(child_node, sub_child_node.parent)
        self.assertEqual({}, sub_child_node.attrs)
        self.assertEqual('test', sub_child_node.name)
        self.assertEqual(0, len(sub_child_node.children))
        self.assertEqual('[test]', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[1]
        self.assertIsInstance(child_node, NewlineTreeNode)
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[2]
        self.assertEqual(document_tree, child_node.root_tree_node)
        self.assertEqual(document_tree, child_node.parent)
        self.assertEqual({}, child_node.attrs)
        self.assertEqual('foobar', child_node.content)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)

    def test_nesting_limit(self):
        """ Test the tree builder handle the ``max_nesting_depth`` limit """
        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags=(DummyTreeNode, ),
                                     max_nesting_depth=5)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)

        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags=(DummyTreeNode,),
                                     max_nesting_depth=4)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)

        document_tree = parse_skcode('[test][test][test][test]',
                                     recognized_tags=(DummyTreeNode,),
                                     max_nesting_depth=3)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = child_node.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual('[test]', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('Nesting depth limit reached', child_node.error_message)

    def test_same_tag_close(self):
        """ Test the tree builder handle ``same_tag_closes=True`` when handling a tag """
        known_tags = (
            get_dummy_node(same_tag_closes=True),
        )
        document_tree = parse_skcode('[test][test][test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[1]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[2]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)

    def test_close_inline(self):
        """ Test the tree builder handle ``close_inlines=True`` when handling a tag """
        known_tags = (
            get_dummy_node(canonical_tag_name='inline', inline=True, close_inlines=False),
            get_dummy_node(inline=False, close_inlines=True),
        )
        document_tree = parse_skcode('[inline][inline][test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(2, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('inline', child_node.name)
        self.assertEqual(1, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        sub_child_node = child_node.children[0]
        self.assertEqual('inline', sub_child_node.name)
        self.assertEqual(0, len(sub_child_node.children))
        self.assertEqual('', sub_child_node.error_message)
        child_node = document_tree.children[1]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)

    def test_standalone_tag(self):
        """ Test the tree builder handle ``standalone=True`` when handling a tag """
        known_tags = (
            get_dummy_node(standalone=True),
        )
        document_tree = parse_skcode('[test][test][test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(3, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[1]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)
        child_node = document_tree.children[2]
        self.assertEqual('test', child_node.name)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('', child_node.error_message)

    def test_bad_closing(self):
        """ Test if the tree builder detect bad closing tag """
        document_tree = parse_skcode('[/test]', recognized_tags=(DummyTreeNode, ))
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('[/test]', child_node.source_close_tag)
        self.assertEqual('Unexpected closing tag', child_node.error_message)

    def test_bad_closing_2(self):
        """ Test if the tree builder detect bad closing tag (nested tag) """
        known_tags = (
            get_dummy_node(canonical_tag_name='inline'),
            DummyTreeNode,
        )
        document_tree = parse_skcode('[inline][/test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, DummyTreeNode)
        self.assertEqual('inline', child_node.name)
        self.assertEqual(1, len(child_node.children))
        sub_child_node = child_node.children[0]
        self.assertIsInstance(sub_child_node, TextTreeNode)
        self.assertEqual(0, len(sub_child_node.children))
        self.assertEqual('[/test]', sub_child_node.source_close_tag)
        self.assertEqual('Unexpected closing tag', sub_child_node.error_message)

    def test_self_closing_tag(self):
        """ Test if the tree builder handle standalone self closing tag """
        known_tags = (
            get_dummy_node(standalone=True),
        )
        document_tree = parse_skcode('[test/]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, DummyTreeNode)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('[test/]', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('', child_node.error_message)

    def test_self_closing_tag_2(self):
        """ Test if the tree builder handle wrong non standalone self closing tag """
        known_tags = (
            get_dummy_node(standalone=False),
        )
        document_tree = parse_skcode('[test/]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        child_node = document_tree.children[0]
        self.assertIsInstance(child_node, TextTreeNode)
        self.assertEqual(0, len(child_node.children))
        self.assertEqual('[test/]', child_node.source_open_tag)
        self.assertEqual('', child_node.source_close_tag)
        self.assertEqual('Unexpected self closing tag', child_node.error_message)

    def test_weak_parent_close(self):
        """ Test if the tree builder handle weak children tag when handling a parent closing tag """
        known_tags = (
            DummyTreeNode,
            get_dummy_node(canonical_tag_name='foobar', weak_parent_close=True),
        )
        document_tree = parse_skcode('[test][foobar][/test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(1, len(test_node.children))
        self.assertEqual('[test]', test_node.source_open_tag)
        self.assertEqual('[/test]', test_node.source_close_tag)
        self.assertEqual('', test_node.error_message)
        foobar_node = test_node.children[0]
        self.assertIsInstance(foobar_node, DummyTreeNode)
        self.assertEqual('foobar', foobar_node.name)
        self.assertEqual(0, len(foobar_node.children))
        self.assertEqual('[foobar]', foobar_node.source_open_tag)
        self.assertEqual('', foobar_node.source_close_tag)
        self.assertEqual('', foobar_node.error_message)

    def test_weak_parent_close_nested(self):
        """ Test if the tree builder handle nested weak children tag when handling a parent closing tag """
        known_tags = (
            DummyTreeNode,
            get_dummy_node(canonical_tag_name='foobar', weak_parent_close=True),
        )
        document_tree = parse_skcode('[test][foobar][foobar][/test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(1, len(test_node.children))
        self.assertEqual('[test]', test_node.source_open_tag)
        self.assertEqual('[/test]', test_node.source_close_tag)
        self.assertEqual('', test_node.error_message)
        foobar_node = test_node.children[0]
        self.assertIsInstance(foobar_node, DummyTreeNode)
        self.assertEqual('foobar', foobar_node.name)
        self.assertEqual(1, len(foobar_node.children))
        self.assertEqual('[foobar]', foobar_node.source_open_tag)
        self.assertEqual('', foobar_node.source_close_tag)
        self.assertEqual('', foobar_node.error_message)
        foobar_node = foobar_node.children[0]
        self.assertIsInstance(foobar_node, DummyTreeNode)
        self.assertEqual('foobar', foobar_node.name)
        self.assertEqual(0, len(foobar_node.children))
        self.assertEqual('[foobar]', foobar_node.source_open_tag)
        self.assertEqual('', foobar_node.source_close_tag)
        self.assertEqual('', foobar_node.error_message)

    def test_after_building_unclosed_weak_parent_close(self):
        """ Test if the tree builder handle weak children tag when reached the end of the document """
        known_tags = (
            get_dummy_node(weak_parent_close=True),
        )
        document_tree = parse_skcode('[test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(0, len(test_node.children))
        self.assertEqual('[test]', test_node.source_open_tag)
        self.assertEqual('', test_node.source_close_tag)
        self.assertEqual('', test_node.error_message)

    def test_unclosed_tag(self):
        """ Test if the tree builder mark unclosed tags as unclosed """
        known_tags = (
            DummyTreeNode,
        )
        document_tree = parse_skcode('[test]', recognized_tags=known_tags, mark_unclosed_tags_as_erroneous=False)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(0, len(test_node.children))
        self.assertEqual('[test]', test_node.source_open_tag)
        self.assertEqual('', test_node.source_close_tag)
        self.assertEqual('', test_node.error_message)
        document_tree = parse_skcode('[test]', recognized_tags=known_tags, mark_unclosed_tags_as_erroneous=True)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertIsInstance(test_node, DummyTreeNode)
        self.assertEqual('test', test_node.name)
        self.assertEqual(0, len(test_node.children))
        self.assertEqual('[test]', test_node.source_open_tag)
        self.assertEqual('', test_node.source_close_tag)
        self.assertEqual('Unclosed tag', test_node.error_message)

    def test_pre_post_processing_sanitizing(self):
        """ Test if the tree builder start the pre/post processing and sanitizing process """

        class TestTreeNode(TreeNode):
            """ Test tag options for tests """

            canonical_tag_name = 'test'
            pre_processed = False
            sanitized = False
            breadcrumb = None
            post_processed = False

            def pre_process_node(self):
                self.pre_processed = True

            def sanitize_node(self, breadcrumb):
                self.sanitized = True
                self.breadcrumb = breadcrumb

            def post_process_node(self):
                self.post_processed = True

        known_tags = (
            TestTreeNode,
        )
        document_tree = parse_skcode('[test][test]', recognized_tags=known_tags)
        self.assertIsInstance(document_tree, RootTreeNode)
        self.assertEqual(1, len(document_tree.children))
        test_node = document_tree.children[0]
        self.assertEqual(1, len(test_node.children))
        self.assertTrue(test_node.pre_processed)
        self.assertTrue(test_node.sanitized)
        self.assertEqual([], test_node.breadcrumb)
        self.assertTrue(test_node.post_processed)
        sub_test_node = test_node.children[0]
        self.assertEqual(0, len(sub_test_node.children))
        self.assertTrue(sub_test_node.pre_processed)
        self.assertTrue(sub_test_node.sanitized)
        self.assertEqual([test_node], sub_test_node.breadcrumb)
        self.assertTrue(sub_test_node.post_processed)
