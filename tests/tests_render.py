"""
SkCode rendering test code.
"""

import unittest

from skcode.etree import TreeNode, RootTreeNode
from skcode.render import (
    render_inner_html,
    render_to_html,
    render_inner_text,
    render_to_text,
    DEFAULT_ERROR_HTML_TEMPLATE,
    SUPPRESS_ERROR_HTML_TEMPLATE
)


def get_test_node(_identifier):
    """ Get a test node class with the given identifier as name """
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

    def test_constants(self):
        """ Test module constants """
        self.assertEqual('<span style="font-weight: bold; color: red;" '
                         'title="{error_message}">{source}</span>', DEFAULT_ERROR_HTML_TEMPLATE)
        self.assertEqual('<!-- {error_message} --> {source}', SUPPRESS_ERROR_HTML_TEMPLATE)

    def test_render_inner_html(self):
        """ Test the ``render_inner_html`` function """
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

    def test_render_inner_html_with_errors(self):
        """ Test the ``render_inner_html`` function with erroneous node """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'),
                               source_open_tag='[test]', source_close_tag='[/test]', error_message='foo')
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_inner_html(tree_node_l2,
                                   html_error_template='<error={error_message}>{source}</error>',
                                   some_custom_kwarg='foobar')
        expected_output = '[HTML+level3-1][/HTML]' \
                          '<error=foo>[test]</error>\n<error=foo>[/test]</error>'
        self.assertEqual(expected_output, output)

    def test_render_inner_html_with_errors_suppressed(self):
        """ Test the ``render_inner_html`` function with erroneous node (error suppressed) """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'),
                               source_open_tag='[test]', source_close_tag='[/test]', error_message='foo')
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_inner_html(tree_node_l2,
                                   html_error_template=SUPPRESS_ERROR_HTML_TEMPLATE,
                                   some_custom_kwarg='foobar')
        expected_output = '[HTML+level3-1][/HTML]' \
                          '<!-- foo --> [test]\n<!-- foo --> [/test]'
        self.assertEqual(expected_output, output)

    def test_render_to_html(self):
        """ Test the ``render_to_html`` function """
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
        """ Test the ``render_to_html`` function with erroneous node """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'),
                                                source_open_tag='[level1-1]',
                                                source_close_tag='[/level1-1]', error_message='foo')
        tree_node_l1.error_message = 'foo'
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l3 = tree_node_l2.new_child('level3', get_test_node('level3-2'),
                                              source_open_tag='[level3-2]',
                                              source_close_tag='[/level3-2]', error_message='bar')
        tree_node_l3.error_message = 'bar'
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_html(root_tree_node,
                                html_error_template='<error={error_message}>{source}</error>',
                                some_custom_kwarg='foobar')
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
        self.assertEqual(expected_output, output)

    def test_render_to_html_with_error_suppressed(self):
        """ Test the ``render_to_html`` function with erroneous node (error suppressed) """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'),
                                                source_open_tag='[level1-1]',
                                                source_close_tag='[/level1-1]', error_message='foo')
        tree_node_l1.error_message = 'foo'
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l3 = tree_node_l2.new_child('level3', get_test_node('level3-2'),
                                              source_open_tag='[level3-2]',
                                              source_close_tag='[/level3-2]', error_message='bar')
        tree_node_l3.error_message = 'bar'
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_html(root_tree_node,
                                html_error_template=SUPPRESS_ERROR_HTML_TEMPLATE,
                                some_custom_kwarg='foobar')
        expected_output = '<!-- foo --> [level1-1]\n' \
                          '[HTML+level2-1]' \
                          '[HTML+level3-1][/HTML]' \
                          '<!-- bar --> [level3-2]\n<!-- bar --> [/level3-2]' \
                          '[/HTML]' \
                          '[HTML+level2-2][/HTML]' \
                          '[HTML+level2-3][/HTML]\n' \
                          '<!-- foo --> [/level1-1]' \
                          '[HTML+level1-2][/HTML]' \
                          '[HTML+level1-3][/HTML]'
        self.assertEqual(expected_output, output)

    def test_render_inner_text(self):
        """ Test the ``render_inner_text`` function """
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

    def test_render_inner_text_with_error(self):
        """ Test the ``render_inner_text`` function with erroneous node """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'),
                               source_open_tag='[test]', source_close_tag='[/test]', error_message='foo')
        tree_node_l2.new_child('level3', get_test_node('level3-2'))
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_inner_text(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[test][/test]' \
                          '[TEXT+level3-2][/TEXT]'
        self.assertEqual(expected_output, output)

    def test_render_to_text(self):
        """ Test the ``render_to_text`` function """
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

    def test_render_to_text_with_error(self):
        """ Test the ``render_to_text`` function with erroneous node """
        root_tree_node = RootTreeNode()
        tree_node_l1 = root_tree_node.new_child('level1', get_test_node('level1-1'))
        root_tree_node.new_child('level1', get_test_node('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', get_test_node('level2-1'))
        tree_node_l1.new_child('level2', get_test_node('level2-2'))
        root_tree_node.new_child('level1', get_test_node('level1-3'))
        tree_node_l2.new_child('level3', get_test_node('level3-1'))
        tree_node_l2.new_child('level3', get_test_node('level3-2'),
                               source_open_tag='[test]', source_close_tag='[/test]', error_message='foo')
        tree_node_l1.new_child('level2', get_test_node('level2-3'))
        output = render_to_text(root_tree_node, some_custom_kwarg='foobar')
        expected_output = '[TEXT+level1-1]' \
                          '[TEXT+level2-1]' \
                          '[TEXT+level3-1][/TEXT]' \
                          '[test][/test]' \
                          '[/TEXT]' \
                          '[TEXT+level2-2][/TEXT]' \
                          '[TEXT+level2-3][/TEXT]' \
                          '[/TEXT]' \
                          '[TEXT+level1-2][/TEXT]' \
                          '[TEXT+level1-3][/TEXT]'
        self.assertEqual(expected_output, output)
