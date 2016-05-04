"""
SkCode elements tree test code.
"""

import unittest

from skcode.etree import (TreeNode,
                          RootTreeNode,
                          ROOT_NODE_NAME,
                          TEXT_NODE_NAME,
                          NEWLINE_NODE_NAME,
                          debug_print_ast)
from skcode.tags import (TagOptions,
                         RootTagOptions)


class DummyTagOptions(TagOptions):
    """ Dummy tag options class for tests. """

    canonical_tag_name = 'test'
    alias_tag_names = ()


class ConstantsTestCase(unittest.TestCase):
    """ Test suite for module constants. """

    def test_constant_values(self):
        """ Test if constants are correct. """
        self.assertEqual('_root', ROOT_NODE_NAME)
        self.assertEqual('_text', TEXT_NODE_NAME)
        self.assertEqual('_newline', NEWLINE_NODE_NAME)


class TreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the ``TreeNode`` class. """

    def test_assertions_constructor(self):
        """ Test assertions at ``__init__`` """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', DummyTagOptions())
        with self.assertRaises(AssertionError) as e:
            TreeNode(None, tree_node, 'test', DummyTagOptions())
        self.assertEqual('The root tree node instance is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            TreeNode(root_tree_node, None, 'test', DummyTagOptions())
        self.assertEqual('The parent node instance is mandatory for non-root nodes.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            TreeNode(root_tree_node, tree_node, '', DummyTagOptions())
        self.assertEqual('Node name must be specified.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            TreeNode(root_tree_node, tree_node, 'test', None)
        self.assertEqual('Node options must be specified.', str(e.exception))

    def test_node_creation(self):
        """ Test if the tree node constructor work as expected. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'test', opts)
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test2', opts)
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test2', tree_node.name)
        self.assertEqual(tree_node.opts, opts)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual(tree_node.content, '')
        self.assertEqual(tree_node.children, [])
        self.assertEqual(tree_node.source_open_tag, '')
        self.assertEqual(tree_node.source_close_tag, '')

    def test_node_creation_2(self):
        """ Test if the tree node constructor work as expected. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'test', opts)
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test2', opts,
                             attrs={'foo': 'bar'}, content='foobar',
                             source_open_tag='test', source_close_tag='test2')
        self.assertEqual(tree_node.root_tree_node, root_tree_node)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test2', tree_node.name)
        self.assertEqual(tree_node.opts, opts)
        self.assertEqual(tree_node.attrs, {'foo': 'bar'})
        self.assertEqual(tree_node.content, 'foobar')
        self.assertEqual(tree_node.children, [])
        self.assertEqual(tree_node.source_open_tag, 'test')
        self.assertEqual(tree_node.source_close_tag, 'test2')

    def test_node_parent_rebase(self):
        """ Test if the constructor reset the parent and tree node instance of given children. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'test', opts)
        root_tree_node_2 = RootTreeNode(RootTagOptions())
        parent_tree_node_2 = TreeNode(root_tree_node_2, root_tree_node_2, 'test', opts)
        child_tree_node = TreeNode(root_tree_node_2, parent_tree_node_2, 'test', opts)
        child_of_child_tree_node = TreeNode(root_tree_node_2, child_tree_node, 'test', opts)
        child_tree_node.children.append(child_of_child_tree_node)
        self.assertEqual(root_tree_node_2, child_tree_node.root_tree_node)
        self.assertEqual(parent_tree_node_2, child_tree_node.parent)
        tree_node = TreeNode(root_tree_node, parent_tree_node, 'test', opts, children=[child_tree_node])
        self.assertEqual(root_tree_node, child_tree_node.root_tree_node)
        self.assertEqual(tree_node, child_tree_node.parent)
        self.assertEqual(root_tree_node, child_of_child_tree_node.root_tree_node)
        self.assertEqual(child_tree_node, child_of_child_tree_node.parent)

    def test_new_child_method(self):
        """ Test if the ``new_child`` method work as expected. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'test', opts)
        tree_node = parent_tree_node.new_child('test_child', opts, content='test kwargs')
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test_child', tree_node.name)
        self.assertEqual(tree_node.opts, opts)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual(tree_node.content, 'test kwargs')
        self.assertEqual(tree_node.children, [])
        self.assertEqual(tree_node.source_open_tag, '')
        self.assertEqual(tree_node.source_close_tag, '')
        self.assertEqual(parent_tree_node.children, [tree_node])

    def test_new_child_method_create_only(self):
        """ Test if the ``new_child`` method work as expected. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = TreeNode(root_tree_node, root_tree_node, 'test', opts)
        tree_node = parent_tree_node.new_child('test_child', opts, content='test kwargs', append=False)
        self.assertEqual(tree_node.parent, parent_tree_node)
        self.assertEqual('test_child', tree_node.name)
        self.assertEqual(tree_node.opts, opts)
        self.assertEqual(tree_node.attrs, {})
        self.assertEqual(tree_node.content, 'test kwargs')
        self.assertEqual(tree_node.children, [])
        self.assertEqual(tree_node.source_open_tag, '')
        self.assertEqual(tree_node.source_close_tag, '')
        self.assertEqual(parent_tree_node.children, [])

    def test_get_raw_content_method(self):
        """ Test if the ``get_raw_content`` method work as expected. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode(RootTagOptions())
        l1_tree_node = root_tree_node.new_child('level 1 child 1', opts, content='Level 1-1')
        root_tree_node.new_child('level 1 child 2', opts, content='Level 1-2')
        l2_tree_node = l1_tree_node.new_child('level 2 child', opts, content='Level 2')
        l2_tree_node.new_child('level 3 child', opts, content='Level 3')
        raw_content = root_tree_node.get_raw_content()
        self.assertEqual('Level 1-1Level 2Level 3Level 1-2', raw_content)

    def test_get_raw_content_method_no_recursion(self):
        """ Test if the ``get_raw_content`` method work as expected. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode(RootTagOptions())
        l1_tree_node = root_tree_node.new_child('level 1 child 1', opts, content='Level 1-1')
        root_tree_node.new_child('level 1 child 2', opts, content='Level 1-2')
        l2_tree_node = l1_tree_node.new_child('level 2 child', opts, content='Level 2')
        l2_tree_node.new_child('level 3 child', opts, content='Level 3')
        raw_content = l1_tree_node.get_raw_content(recursive=False)
        self.assertEqual('Level 1-1', raw_content)

    def test_unwrap_as_erroneous_method_without_sources(self):
        """ Test if the ``unwrap_as_erroneous`` method work as expected. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child (test unwrap this)
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode(RootTagOptions())
        l1_tree_node = root_tree_node.new_child('level 1 child 1', opts)
        l1_2_tree_node = root_tree_node.new_child('level 1 child 2', opts)
        l2_tree_node = l1_tree_node.new_child('level 2 child', opts)
        l3_tree_node = l2_tree_node.new_child('level 3 child 1', opts)

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(l1_tree_node.children, [l2_tree_node])
        self.assertEqual(l2_tree_node.children, [l3_tree_node])
        self.assertEqual(l3_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])

        l2_tree_node.unwrap_as_erroneous(opts)

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(l1_tree_node.children, [l3_tree_node])
        self.assertEqual(l3_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])

    def test_unwrap_as_erroneous_method_with_sources(self):
        """ Test if the ``unwrap_as_erroneous`` method work as expected when unwrapped tag has sources. """
        opts = DummyTagOptions()
        err_opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child (test unwrap this)
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode(RootTagOptions())
        l1_tree_node = root_tree_node.new_child('level 1 child 1', opts)
        l1_2_tree_node = root_tree_node.new_child('level 1 child 2', opts)
        l2_tree_node = l1_tree_node.new_child('level 2 child', opts,
                                              source_open_tag='tag_open',
                                              source_close_tag='tag_close')
        l3_tree_node = l2_tree_node.new_child('level 3 child 1', opts)

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(l1_tree_node.children, [l2_tree_node])
        self.assertEqual(l2_tree_node.children, [l3_tree_node])
        self.assertEqual(l3_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])

        l2_tree_node.unwrap_as_erroneous(err_opts)

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(len(l1_tree_node.children), 3)
        self.assertEqual(l1_tree_node.children[0].name, TEXT_NODE_NAME)
        self.assertEqual(l1_tree_node.children[0].content, 'tag_open')
        self.assertEqual(l1_tree_node.children[0].opts, err_opts)
        self.assertEqual(l1_tree_node.children[1], l3_tree_node)
        self.assertEqual(l1_tree_node.children[2].name, TEXT_NODE_NAME)
        self.assertEqual(l1_tree_node.children[2].content, 'tag_close')
        self.assertEqual(l1_tree_node.children[2].opts, err_opts)
        self.assertEqual(l3_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])

    def test_delete_from_parent_method(self):
        """ Test if the ``delete_from_parent`` method work as expected. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child (test delete this)
        #     - level 3 child
        #  - level 1 child 2
        root_tree_node = RootTreeNode(RootTagOptions())
        l1_tree_node = root_tree_node.new_child('level 1 child 1', opts)
        l1_2_tree_node = root_tree_node.new_child('level 1 child 2', opts)
        l2_tree_node = l1_tree_node.new_child('level 2 child', opts)
        l3_tree_node = l2_tree_node.new_child('level 3 child 1', opts)

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(l1_tree_node.children, [l2_tree_node])
        self.assertEqual(l2_tree_node.children, [l3_tree_node])
        self.assertEqual(l3_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])

        l2_tree_node.delete_from_parent()

        self.assertEqual(root_tree_node.children, [l1_tree_node, l1_2_tree_node])
        self.assertEqual(l1_tree_node.children, [])
        self.assertEqual(l1_2_tree_node.children, [])


class RootTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the ``TreeNode`` class. """

    def test_root_tree_node_is_a_tree_node(self):
        """ Assert inheritance of ``RootTreeNode`` from ``TreeNode``. """
        root_tree_node = RootTreeNode(RootTagOptions())
        self.assertTrue(isinstance(root_tree_node, TreeNode))

    def test_root_node_creation(self):
        """ Test if the root tree node constructor work as expected. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(opts)
        self.assertIsNotNone(root_tree_node)
        self.assertIsNone(root_tree_node.parent)
        self.assertEqual(ROOT_NODE_NAME, root_tree_node.name)
        self.assertEqual(root_tree_node.opts, opts)
        self.assertEqual(root_tree_node.attrs, {})
        self.assertEqual(root_tree_node.content, '')
        self.assertEqual(root_tree_node.children, [])
        self.assertEqual(root_tree_node.source_open_tag, '')
        self.assertEqual(root_tree_node.source_close_tag, '')

    def test_unwrap_as_erroneous_not_implemented(self):
        """ Assert that ``unwrap_as_erroneous`` is not implemented for root tree node. """
        opts = DummyTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        self.assertIsNotNone(root_tree_node)
        with self.assertRaises(NotImplementedError):
            root_tree_node.unwrap_as_erroneous(opts)

    def test_delete_from_parent_not_implemented(self):
        """ Assert that ``delete_from_parent`` is not implemented for root tree node. """
        root_tree_node = RootTreeNode(RootTagOptions())
        self.assertIsNotNone(root_tree_node)
        with self.assertRaises(NotImplementedError):
            root_tree_node.delete_from_parent()


class DebugApiTestCase(unittest.TestCase):
    """ Test suite for the etree debug API. """

    def test_debug_print_ast(self):
        """ Test if the ``debug_print_ast`` work as expected. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child 1
        #     - level 3 child 1
        #  - level 1 child 2
        root_tree_node = RootTreeNode(opts)
        l1_tree_node = root_tree_node.new_child('level_1_child_1', opts, attrs={'foo': 'bar'})
        root_tree_node.new_child('level_1_child_2', opts)
        l2_tree_node = l1_tree_node.new_child('level_2_child_1', opts)
        l2_tree_node.new_child('level_3_child_1', opts, content='Hello world!')

        output_returned = []

        def _print_to_str(*args):
            output_returned.append(' '.join(args))
        debug_print_ast(root_tree_node, print_fnct=_print_to_str)

        expected_output = [
            "TreeNode(name=_root, attrs={}, content='', len(children)=2, opts=DummyTagOptions) ",
            "    TreeNode(name=level_1_child_1, attrs={'foo': 'bar'}, content='', len(children)=1, opts=DummyTagOptions) ",
            "        TreeNode(name=level_2_child_1, attrs={}, content='', len(children)=1, opts=DummyTagOptions) ",
            "            TreeNode(name=level_3_child_1, attrs={}, content='Hello world!', len(children)=0, opts=DummyTagOptions) ",
            "    TreeNode(name=level_1_child_2, attrs={}, content='', len(children)=0, opts=DummyTagOptions) "
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, output_returned)

    def test_debug_print_ast_with_erroneous_parent(self):
        """ Test if the ``debug_print_ast`` work as expected when an erroneous aprent is found. """
        opts = DummyTagOptions()
        # RootTreeNode
        #  - level 1 child 1
        #   - level 2 child 1
        #     - level 3 child 1
        #  - level 1 child 2
        root_tree_node = RootTreeNode(opts)
        l1_tree_node = root_tree_node.new_child('level_1_child_1', opts, attrs={'foo': 'bar'})
        root_tree_node.new_child('level_1_child_2', opts)
        l2_tree_node = l1_tree_node.new_child('level_2_child_1', opts)
        l3_tree_node = l2_tree_node.new_child('level_3_child_1', opts, content='Hello world!')

        # Add some oops
        l3_tree_node.parent = root_tree_node

        output_returned = []

        def _print_to_str(*args):
            output_returned.append(' '.join(args))
        debug_print_ast(root_tree_node, print_fnct=_print_to_str)

        expected_output = [
            "TreeNode(name=_root, attrs={}, content='', len(children)=2, opts=DummyTagOptions) ",
            "    TreeNode(name=level_1_child_1, attrs={'foo': 'bar'}, content='', len(children)=1, opts=DummyTagOptions) ",
            "        TreeNode(name=level_2_child_1, attrs={}, content='', len(children)=1, opts=DummyTagOptions) ",
            "            TreeNode(name=level_3_child_1, attrs={}, content='Hello world!', len(children)=0, opts=DummyTagOptions) !! Parent mismatch !!",
            "    TreeNode(name=level_1_child_2, attrs={}, content='', len(children)=0, opts=DummyTagOptions) "
        ]
        self.maxDiff = None
        self.assertEqual(expected_output, output_returned)
