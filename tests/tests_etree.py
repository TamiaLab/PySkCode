"""
SkCode elements tree test code.
"""

import unittest

from skcode.etree import (
    TreeNode,
    RootTreeNode,
    debug_print_ast
)


class DummyTreeNode(TreeNode):
    """ Dummy tag options class for tests. """

    canonical_tag_name = 'test'
    alias_tag_names = ()


class OtherDummyTreeNode(TreeNode):
    """ Dummy tag options class for tests. """

    canonical_tag_name = 'test'
    alias_tag_names = ()


class TreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the ``TreeNode`` class. """

    def test_constants_defaults(self):
        """ Test all constants default values """
        self.assertIsNone(TreeNode.canonical_tag_name)
        self.assertEqual((), TreeNode.alias_tag_names)
        self.assertFalse(TreeNode.newline_closes)
        self.assertFalse(TreeNode.same_tag_closes)
        self.assertFalse(TreeNode.weak_parent_close)
        self.assertFalse(TreeNode.standalone)
        self.assertTrue(TreeNode.parse_embedded)
        self.assertFalse(TreeNode.inline)
        self.assertTrue(TreeNode.close_inlines)
        self.assertFalse(TreeNode.make_paragraphs_here)
        self.assertFalse(TreeNode.is_root)

    def test_assertions_constructor(self):
        """ Test assertions at constructor """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', DummyTreeNode)
        with self.assertRaises(AssertionError) as e:
            TreeNode(None, tree_node, 'test')
        self.assertEqual('The root tree node instance is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            TreeNode(root_tree_node, None, 'test')
        self.assertEqual('The parent node instance is mandatory for non-root nodes.', str(e.exception))

    def test_node_creation(self):
        """ Test if the tree node constructor work as expected. """
        root_tree_node = RootTreeNode()
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'parent')
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test')
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test', tree_node.name)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual('', tree_node.content)
        self.assertEqual(tree_node.children, [])
        self.assertEqual('', tree_node.source_open_tag)
        self.assertEqual('', tree_node.source_close_tag)
        self.assertEqual('', tree_node.error_message)

    def test_node_creation_advanced(self):
        """ Test if the tree node constructor work as expected. """
        root_tree_node = RootTreeNode()
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'parent')
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test',
                             attrs={'foo': 'bar'}, content='foobar',
                             source_open_tag='[test]', source_close_tag='[/test]',
                             error_message='Error msg')
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test', tree_node.name)
        self.assertEqual(tree_node.attrs, {'foo': 'bar'})
        self.assertEqual('foobar', tree_node.content)
        self.assertEqual(tree_node.children, [])
        self.assertEqual('[test]', tree_node.source_open_tag)
        self.assertEqual('[/test]', tree_node.source_close_tag)
        self.assertEqual('Error msg', tree_node.error_message)

    def test_node_parent_rebase(self):
        """ Test if the constructor reset the parent and tree node instance of given children. """
        root_tree_node = RootTreeNode()
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'parent 1')
        root_tree_node_2 = RootTreeNode()
        parent_tree_node_2 = TreeNode(root_tree_node_2, root_tree_node_2, 'parent 2')
        child_tree_node = TreeNode(root_tree_node_2, parent_tree_node_2, 'test')
        child_of_child_tree_node = TreeNode(root_tree_node_2, child_tree_node, 'test')
        child_tree_node.children.append(child_of_child_tree_node)
        self.assertEqual(root_tree_node_2, child_tree_node.root_tree_node)
        self.assertEqual(parent_tree_node_2, child_tree_node.parent)
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test', children=[child_tree_node])
        self.assertEqual(root_tree_node, child_tree_node.root_tree_node)
        self.assertEqual(tree_node, child_tree_node.parent)
        self.assertEqual(root_tree_node, child_of_child_tree_node.root_tree_node)
        self.assertEqual(child_tree_node, child_of_child_tree_node.parent)

    def test_new_child_method(self):
        """ Test if the ``new_child`` method work as expected. """
        root_tree_node = RootTreeNode()
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'parent')
        tree_node = parent_tree_node.new_child('child', DummyTreeNode, content='test kwargs')
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('child', tree_node.name)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual('test kwargs', tree_node.content)
        self.assertEqual(tree_node.children, [])
        self.assertEqual('', tree_node.source_open_tag)
        self.assertEqual('', tree_node.source_close_tag)
        self.assertEqual(parent_tree_node.children, [tree_node])
        self.assertEqual('', tree_node.error_message)

    def test_new_child_method_create_only(self):
        """ Test if the ``new_child`` method work as expected. """
        root_tree_node = RootTreeNode()
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'parent')
        tree_node = parent_tree_node.new_child('child', DummyTreeNode, content='test kwargs', append=False)
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('child', tree_node.name)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual('test kwargs', tree_node.content)
        self.assertEqual(tree_node.children, [])
        self.assertEqual('', tree_node.source_open_tag)
        self.assertEqual('', tree_node.source_close_tag)
        self.assertEqual(parent_tree_node.children, [])
        self.assertEqual('', tree_node.error_message)

    def test_get_raw_content_method(self):
        """ Test if the ``get_raw_content`` method work as expected. """
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode()
        l1_tree_node = root_tree_node.new_child('level 1 child 1', DummyTreeNode, content='Level 1-1')
        root_tree_node.new_child('level 1 child 2', DummyTreeNode, content='Level 1-2')
        l2_tree_node = l1_tree_node.new_child('level 2 child', DummyTreeNode, content='Level 2')
        l2_tree_node.new_child('level 3 child', DummyTreeNode, content='Level 3')
        raw_content = root_tree_node.get_raw_content()
        self.assertEqual('Level 1-1Level 2Level 3Level 1-2', raw_content)

    def test_get_raw_content_method_no_recursion(self):
        """ Test if the ``get_raw_content`` method work as expected. """
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode()
        l1_tree_node = root_tree_node.new_child('level 1 child 1', DummyTreeNode, content='Level 1-1')
        root_tree_node.new_child('level 1 child 2', DummyTreeNode, content='Level 1-2')
        l2_tree_node = l1_tree_node.new_child('level 2 child', DummyTreeNode, content='Level 2')
        l2_tree_node.new_child('level 3 child', DummyTreeNode, content='Level 3')
        raw_content = l1_tree_node.get_raw_content(recursive=False)
        self.assertEqual('Level 1-1', raw_content)

    def test_search_in_tree(self):
        """ Test the ``search_in_tree`` helper. """
        document_tree = RootTreeNode()
        node1 = document_tree.new_child('node', DummyTreeNode)
        l1_tree_node = document_tree.new_child('test_l1', OtherDummyTreeNode)
        node2 = l1_tree_node.new_child('node', DummyTreeNode)
        l2_tree_node = l1_tree_node.new_child('test_l2', OtherDummyTreeNode)
        node3 = l2_tree_node.new_child('node', DummyTreeNode)
        nodes = list(document_tree.search_in_tree(DummyTreeNode))
        self.assertEqual([node1, node2, node3], nodes)

    def test_default_sanitize_node_policy(self):
        """ Test the default ``sanitize_node`` method policy. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode)
        tree_node.sanitize_node([])
        self.assertTrue(True)
        # TODO Implement sanitize_node and test it

    def test_default_post_process_node_implementation(self):
        """ Test the default ``post_process_node`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode)
        self.assertTrue(tree_node.post_process_node())

    def test_default_render_html_implementation(self):
        """ Test the default ``render_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode)
        with self.assertRaises(NotImplementedError) as e:
            tree_node.render_html('', custom_value='foobar')
        self.assertEqual('render_html() need to be implemented in subclass', str(e.exception))

    def test_default_render_error_html_implementation(self):
        """ Test the default ``render_error_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode, error_message='msg',
                                             source_open_tag='[test]', source_close_tag='[/test]', content='')
        expected_html = '<error="msg">[test]</error>\ninner HTML\n<error="msg">[/test]</error>'
        self.assertEqual(expected_html, tree_node.render_error_html('inner HTML',
                                                                    '<error="{error_message}">{source}</error>'))

    def test_default_render_error_html_implementation_open_tag(self):
        """ Test the default ``render_error_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode, error_message='msg',
                                             source_open_tag='[test]', source_close_tag='', content='')
        expected_html = '<error="msg">[test]</error>\ninner HTML'
        self.assertEqual(expected_html, tree_node.render_error_html('inner HTML',
                                                                    '<error="{error_message}">{source}</error>'))

    def test_default_render_error_html_implementation_close_tag(self):
        """ Test the default ``render_error_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode, error_message='msg',
                                             source_open_tag='', source_close_tag='[/test]', content='')
        expected_html = 'inner HTML\n<error="msg">[/test]</error>'
        self.assertEqual(expected_html, tree_node.render_error_html('inner HTML',
                                                                    '<error="{error_message}">{source}</error>'))

    def test_default_render_error_html_implementation_content(self):
        """ Test the default ``render_error_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode, error_message='msg',
                                             source_open_tag='[test]', source_close_tag='[/test]', content='content')
        expected_html = '<error="msg">[test]</error>\ncontent\n<error="msg">[/test]</error>'
        self.assertEqual(expected_html, tree_node.render_error_html('', '<error="{error_message}">{source}</error>'))

    def test_default_render_error_html_implementation_no_source(self):
        """ Test the default ``render_error_html`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode, error_message='msg',
                                             source_open_tag='', source_close_tag='', content='')
        self.assertEqual('', tree_node.render_error_html('', '<error="{error_message}">{source}</error>'))

    def test_default_render_text_implementation(self):
        """ Test the default ``render_text`` method implementation. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('child', DummyTreeNode)
        with self.assertRaises(NotImplementedError) as e:
            tree_node.render_text('', custom_value='foobar')
        self.assertEqual('render_text() need to be implemented in subclass', str(e.exception))


class RootTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the ``TreeNode`` class. """

    def test_root_tree_node_is_a_tree_node(self):
        """ Assert inheritance of ``RootTreeNode`` from ``TreeNode``. """
        root_tree_node = RootTreeNode()
        self.assertTrue(isinstance(root_tree_node, TreeNode))

    def test_constants_defaults(self):
        """ Test all constants default values """
        self.assertIsNone(RootTreeNode.canonical_tag_name)
        self.assertEqual((), RootTreeNode.alias_tag_names)
        self.assertFalse(RootTreeNode.newline_closes)
        self.assertFalse(RootTreeNode.same_tag_closes)
        self.assertFalse(RootTreeNode.weak_parent_close)
        self.assertFalse(RootTreeNode.standalone)
        self.assertTrue(RootTreeNode.parse_embedded)
        self.assertFalse(RootTreeNode.inline)
        self.assertTrue(RootTreeNode.close_inlines)
        self.assertTrue(RootTreeNode.make_paragraphs_here)
        self.assertTrue(RootTreeNode.is_root)

    def test_node_creation(self):
        """ Test if the tree node constructor work as expected. """
        root_tree_node = RootTreeNode()
        self.assertEqual(root_tree_node.root_tree_node, root_tree_node)
        self.assertIsNone(root_tree_node.parent)
        self.assertIsNone(root_tree_node.name)
        self.assertEqual(root_tree_node.attrs, {})
        self.assertEqual('', root_tree_node.content)
        self.assertEqual(root_tree_node.children, [])
        self.assertEqual('', root_tree_node.source_open_tag)
        self.assertEqual('', root_tree_node.source_close_tag)
        self.assertEqual('', root_tree_node.error_message)

    def test_render_html(self):
        """ Test the ``render_html`` method implementation. """
        root_tree_node = RootTreeNode()
        self.assertEqual('inner HTML', root_tree_node.render_html('inner HTML'))

    def test_render_text(self):
        """ Test the ``render_text`` method implementation. """
        root_tree_node = RootTreeNode()
        self.assertEqual('inner text', root_tree_node.render_text('inner text'))


class DebugApiTestCase(unittest.TestCase):
    """ Test suite for the etree debug API. """

    def test_debug_print_ast(self):
        """ Test if the ``debug_print_ast`` work as expected. """
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child 1
        #     - level 3 child 1
        #  - level 1 child 2
        root_tree_node = RootTreeNode()
        l1_tree_node = root_tree_node.new_child('level_1_child_1', DummyTreeNode, attrs={'foo': 'bar'})
        root_tree_node.new_child('level_1_child_2', DummyTreeNode)
        l2_tree_node = l1_tree_node.new_child('level_2_child_1', DummyTreeNode)
        l2_tree_node.new_child('level_3_child_1', DummyTreeNode, content='Hello world!')

        output_returned = []

        def _print_to_str(*args):
            output_returned.append(' '.join(args))
        debug_print_ast(root_tree_node, print_fnct=_print_to_str)

        expected_output = [
            "RootTreeNode(name=\"None\", attrs={}, content='', len(children)=2) ",
            "    DummyTreeNode(name=\"level_1_child_1\", attrs={'foo': 'bar'}, content='', len(children)=1) ",
            "        DummyTreeNode(name=\"level_2_child_1\", attrs={}, content='', len(children)=1) ",
            "            DummyTreeNode(name=\"level_3_child_1\", attrs={}, content='Hello world!', len(children)=0) ",
            "    DummyTreeNode(name=\"level_1_child_2\", attrs={}, content='', len(children)=0) "
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, output_returned)

    def test_debug_print_ast_with_erroneous_parent(self):
        """ Test if the ``debug_print_ast`` work as expected when an erroneous aprent is found. """
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child 1
        #     - level 3 child 1
        #  - level 1 child 2
        root_tree_node = RootTreeNode()
        l1_tree_node = root_tree_node.new_child('level_1_child_1', DummyTreeNode, attrs={'foo': 'bar'})
        root_tree_node.new_child('level_1_child_2', DummyTreeNode)
        l2_tree_node = l1_tree_node.new_child('level_2_child_1', DummyTreeNode)
        l3_tree_node = l2_tree_node.new_child('level_3_child_1', DummyTreeNode, content='Hello world!')

        # Add some oops
        l3_tree_node.parent = root_tree_node

        output_returned = []

        def _print_to_str(*args):
            output_returned.append(' '.join(args))
        debug_print_ast(root_tree_node, print_fnct=_print_to_str)

        expected_output = [
            "RootTreeNode(name=\"None\", attrs={}, content='', len(children)=2) ",
            "    DummyTreeNode(name=\"level_1_child_1\", attrs={'foo': 'bar'}, content='', len(children)=1) ",
            "        DummyTreeNode(name=\"level_2_child_1\", attrs={}, content='', len(children)=1) ",
            "            DummyTreeNode(name=\"level_3_child_1\", attrs={}, content='Hello world!', len(children)=0) !! Parent mismatch !!",
            "    DummyTreeNode(name=\"level_1_child_2\", attrs={}, content='', len(children)=0) "
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, output_returned)
