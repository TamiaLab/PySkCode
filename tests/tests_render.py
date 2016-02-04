"""
SkCode rendering test code.
"""

import unittest

from skcode.tags import (TagOptions,
                         RootTagOptions)
from skcode.etree import RootTreeNode
from skcode.render import (render_inner_html, render_to_html,
                           render_inner_text, render_to_text,
                           render_inner_skcode, render_to_skcode)


class TestTagOptions(TagOptions):
    """ Test tag options class """

    def __init__(self, identifier, **kwargs):
        super(TestTagOptions, self).__init__(**kwargs)
        assert identifier, "The node identifier string must be set for testing."
        self.identifier = identifier

    def render_text(self, tree_node, inner_text, **kwargs):
        assert 'some_custom_kwarg' in kwargs, "Extra kwargs must be passed to rendering function."
        return '[TEXT+%s]%s[/TEXT]' % (self.identifier, inner_text)

    def render_html(self, tree_node, inner_html, **kwargs):
        assert 'some_custom_kwarg' in kwargs, "Extra kwargs must be passed to rendering function."
        return '[HTML+%s]%s[/HTML]' % (self.identifier, inner_html)

    def render_skcode(self, tree_node, inner_skcode,
                      opening_tag_ch='[', closing_tag_ch=']',
                      allow_tagvalue_attr=True, **kwargs):
        assert 'some_custom_kwarg' in kwargs, "Extra kwargs must be passed to rendering function."
        return '[SKCODE+%s]%s[/SKCODE]' % (self.identifier, inner_skcode)


class RenderingTestCase(unittest.TestCase):
    """ Test suite for the rendering module. """

    def test_render_inner_html(self):
        """ Test the ``render_inner_html`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
        output = render_inner_html(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[HTML+level3-1][/HTML]' \
                          '[HTML+level3-2][/HTML]'
        self.assertEqual(expected_output, output)

    def test_render_to_html(self):
        """ Test the ``render_to_html`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
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

    def test_render_inner_text(self):
        """ Test the ``render_inner_text`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
        output = render_inner_text(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[TEXT+level3-1][/TEXT]' \
                          '[TEXT+level3-2][/TEXT]'
        self.assertEqual(expected_output, output)

    def test_render_to_text(self):
        """ Test the ``render_to_text`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
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

    def test_render_inner_skcode(self):
        """ Test the ``render_inner_skcode`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
        output = render_inner_skcode(tree_node_l2, some_custom_kwarg='foobar')
        expected_output = '[SKCODE+level3-1][/SKCODE]' \
                          '[SKCODE+level3-2][/SKCODE]'
        self.assertEqual(expected_output, output)

    def test_render_to_skcode(self):
        """ Test the ``render_to_skcode`` function. """
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node_l1 = root_tree_node.new_child('level1', TestTagOptions('level1-1'))
        root_tree_node.new_child('level1', TestTagOptions('level1-2'))
        tree_node_l2 = tree_node_l1.new_child('level2', TestTagOptions('level2-1'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-2'))
        root_tree_node.new_child('level1', TestTagOptions('level1-3'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-1'))
        tree_node_l2.new_child('level3', TestTagOptions('level3-2'))
        tree_node_l1.new_child('level2', TestTagOptions('level2-3'))
        output = render_to_skcode(root_tree_node, some_custom_kwarg='foobar')
        expected_output = '[SKCODE+level1-1]' \
                          '[SKCODE+level2-1]' \
                          '[SKCODE+level3-1][/SKCODE]' \
                          '[SKCODE+level3-2][/SKCODE]' \
                          '[/SKCODE]' \
                          '[SKCODE+level2-2][/SKCODE]' \
                          '[SKCODE+level2-3][/SKCODE]' \
                          '[/SKCODE]' \
                          '[SKCODE+level1-2][/SKCODE]' \
                          '[SKCODE+level1-3][/SKCODE]'
        self.assertEqual(expected_output, output)
