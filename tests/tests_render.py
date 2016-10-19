"""
SkCode rendering test code.
"""

import unittest

from skcode.etree import TreeNode, RootTreeNode
from skcode.render import (
    render_inner_html,
    render_to_html,
    render_inner_text,
    render_to_text
)


def get_test_node(_identifier):
    """ Get a test node class witht the given identifier as name """
    assert _identifier, "The node identifier string must be set for testing."

    class TestTreeNode(TreeNode):
        """ Test tag options class """

        canonical_tag_name = 'test'
        alias_tag_names = ()
        identifier = _identifier

        def render_text(self, inner_text, **kwargs):
            assert 'some_custom_kwarg' in kwargs, "Extra kwargs must be passed to rendering function."
            return '[TEXT+%s]%s[/TEXT]' % (self.identifier, inner_text)

        def render_html(self, inner_html, **kwargs):
            assert 'some_custom_kwarg' in kwargs, "Extra kwargs must be passed to rendering function."
            return '[HTML+%s]%s[/HTML]' % (self.identifier, inner_html)

    return TestTreeNode


class RenderingTestCase(unittest.TestCase):
    """ Test suite for the rendering module. """

    def test_render_inner_html(self):
        """ Test the ``render_inner_html`` function. """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'))
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_inner_html(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[HTML+level3-1][/HTML]' \
                          '[HTML+level3-2][/HTML]'
        self.assertEqual(expected_output, output)

    def test_render_to_html(self):
        """ Test the ``render_to_html`` function. """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'))
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_html(root_tree_node, some_custom_kwarg='foobar')
        expected_output = '[HTML+level1-1]' \
                          '[HTML+level2-1]' \
                          '[HTML+level3-1][/HTML]' \
                          '[HTML+level3-2][/HTML]' \
                          '[/HTML]' \
                          '[HTML+level2-2][/HTML]' \
                          '[HTML+level2-3][/HTML]' \
                          '[/HTML]' \
                          '[HTML+level1-2][/HTML]' \
                          '[HTML+level1-3][/HTML]'
        self.assertEqual(expected_output, output)

    def test_render_to_html_with_error(self):
        """ Test the ``render_to_html`` function. """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'),
                                                source_open_tag='[level1-1]', source_close_tag='[/level1-1]')
        tree_node_l1.error_message = 'foo'
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l3 = tree_node_l2.new_child('level3', get_test_node('level3-2'),
                                              source_open_tag='[level3-2]', source_close_tag='[/level3-2]')
        tree_node_l3.error_message = 'bar'
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_html(root_tree_node, some_custom_kwarg='foobar',
                                html_error_template='<error={error_message}>{source}</error>')
        expected_output = '<error=foo>[level1-1]</error>\n' \
                          '[HTML+level2-1]' \
                          '[HTML+level3-1][/HTML]' \
                          '<error=bar>[level3-2]</error>\n<error=bar>[/level3-2]</error>' \
                          '[/HTML]' \
                          '[HTML+level2-2][/HTML]' \
                          '[HTML+level2-3][/HTML]\n' \
                          '<error=foo>[/level1-1]</error>' \
                          '[HTML+level1-2][/HTML]' \
                          '[HTML+level1-3][/HTML]'
        print(output)
        self.assertEqual(expected_output, output)

    def test_render_inner_text(self):
        """ Test the ``render_inner_text`` function. """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'))
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_inner_text(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[TEXT+level3-1][/TEXT]' \
                          '[TEXT+level3-2][/TEXT]'
        self.assertEqual(expected_output, output)

    def test_render_to_text(self):
        """ Test the ``render_to_text`` function. """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'))
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_text(root_tree_node, some_custom_kwarg='foobar')
        expected_output = '[TEXT+level1-1]' \
                          '[TEXT+level2-1]' \
                          '[TEXT+level3-1][/TEXT]' \
                          '[TEXT+level3-2][/TEXT]' \
                          '[/TEXT]' \
                          '[TEXT+level2-2][/TEXT]' \
                          '[TEXT+level2-3][/TEXT]' \
                          '[/TEXT]' \
                          '[TEXT+level1-2][/TEXT]' \
                          '[TEXT+level1-3][/TEXT]'
        self.assertEqual(expected_output, output)
