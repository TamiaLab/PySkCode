"""
SkCode TO.DO lists tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TodoListTagOptions,
                         TodoTaskTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TodoListsTagTestCase(unittest.TestCase):
    """ Tests suite for the TO.DO lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('todolist', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['todolist'], TodoListTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TodoListTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = TodoListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('todolist', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<ul>test</ul>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = TodoListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('todolist', opts)
        output_result = opts.render_text(tree_node, 'test')
        expected_result = '-- TODO LIST --\ntest\n'
        self.assertEqual(expected_result, output_result)


class TodoListTasksTagTestCase(unittest.TestCase):
    """ Tests suite for the TO.DO list tasks tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('task', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['task'], TodoTaskTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TodoTaskTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertTrue(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('done', opts.is_done_attr_name)
        self.assertEqual('done', opts.is_done_tagname_value)
        self.assertEqual('task_done', opts.task_done_html_class)
        self.assertEqual('task_pending', opts.task_pending_html_class)

    def test_get_is_done_task_flag_with_done_attribute_set(self):
        """ Test the ``get_is_done_task_flag`` method with the "done" attribute set. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'done': ''})
        self.assertTrue(opts.get_is_done_task_flag(tree_node))

    def test_get_is_done_task_flag_with_tagname_value_set(self):
        """ Test the ``get_is_done_task_flag`` method with the tag name attribute set. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'task': 'done'})
        self.assertTrue(opts.get_is_done_task_flag(tree_node))

    def test_get_is_done_task_flag_with_tagname_value_set_to_unknown_value(self):
        """ Test the ``get_is_done_task_flag`` method with the tag name attribute set to an unknown value. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'task': 'johndoe'})
        self.assertFalse(opts.get_is_done_task_flag(tree_node))

    def test_get_is_done_task_flag_without_value_set(self):
        """ Test the ``get_is_done_task_flag`` method without the done flag set. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts)
        self.assertFalse(opts.get_is_done_task_flag(tree_node))

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<li class="task_pending">test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_is_done(self):
        """ Test the ``render_html`` method with a "done" task. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'done': ''})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<li class="task_done">test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts)
        output_result = opts.render_text(tree_node, 'test\ntest2\n')
        expected_result = '[ ] test\n    test2\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts)
        output_result = opts.render_text(tree_node, '    test\ntest2\n    ')
        expected_result = '[ ] test\n    test2\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_is_done(self):
        """ Test the ``render_text`` method with a "done" task. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'done': ''})
        output_result = opts.render_text(tree_node, 'test\ntest2\n')
        expected_result = '[x] test\n    test2\n'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts)
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_is_done(self):
        """ Test the ``get_skcode_attributes`` method with a "done" task. """
        opts = TodoTaskTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('task', opts, attrs={'done': ''})
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'done': None}, None)
        self.assertEqual(expected_result, output_result)
