"""
SkCode TODO list tag definitions code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    TodoListTreeNode,
    TodoTaskTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class TodoListTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the TODO lists tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TodoListTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TodoListTreeNode.newline_closes)
        self.assertFalse(TodoListTreeNode.same_tag_closes)
        self.assertFalse(TodoListTreeNode.weak_parent_close)
        self.assertFalse(TodoListTreeNode.standalone)
        self.assertTrue(TodoListTreeNode.parse_embedded)
        self.assertFalse(TodoListTreeNode.inline)
        self.assertTrue(TodoListTreeNode.close_inlines)
        self.assertEqual('todolist', TodoListTreeNode.canonical_tag_name)
        self.assertEqual((), TodoListTreeNode.alias_tag_names)
        self.assertFalse(TodoListTreeNode.make_paragraphs_here)
        self.assertEqual('<ul>{inner_html}</ul>\n', TodoListTreeNode.html_render_template)
        self.assertEqual('-- TODO LIST --\n{inner_text}\n', TodoListTreeNode.text_render_template)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('todolist', TodoListTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = '<ul>test</ul>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('todolist', TodoListTreeNode)
        output_result = tree_node.render_text('test')
        expected_result = '-- TODO LIST --\ntest\n'
        self.assertEqual(expected_result, output_result)


class TodoTaskTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the TODO list tasks tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TodoTaskTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TodoTaskTreeNode.newline_closes)
        self.assertTrue(TodoTaskTreeNode.same_tag_closes)
        self.assertTrue(TodoTaskTreeNode.weak_parent_close)
        self.assertFalse(TodoTaskTreeNode.standalone)
        self.assertTrue(TodoTaskTreeNode.parse_embedded)
        self.assertFalse(TodoTaskTreeNode.inline)
        self.assertTrue(TodoTaskTreeNode.close_inlines)
        self.assertEqual('task', TodoTaskTreeNode.canonical_tag_name)
        self.assertEqual((), TodoTaskTreeNode.alias_tag_names)
        self.assertTrue(TodoTaskTreeNode.make_paragraphs_here)
        self.assertEqual('done', TodoTaskTreeNode.is_done_attr_name)
        self.assertEqual('done', TodoTaskTreeNode.is_done_tagname_value)
        self.assertEqual('task_done', TodoTaskTreeNode.task_done_html_class)
        self.assertEqual('task_pending', TodoTaskTreeNode.task_pending_html_class)
        self.assertEqual('<li class="{class_name}">{inner_html}</li>\n', TodoTaskTreeNode.html_render_template)

    def test_get_is_done_task_flag_with_done_attribute_set(self):
        """ Test the ``get_is_done_task_flag`` method with the "done" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode, attrs={'done': ''})
        self.assertTrue(tree_node.get_is_done_task_flag())

    def test_get_is_done_task_flag_with_tagname_value_set(self):
        """ Test the ``get_is_done_task_flag`` method with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode, attrs={'task': 'done'})
        self.assertTrue(tree_node.get_is_done_task_flag())

    def test_get_is_done_task_flag_with_tagname_value_set_to_unknown_value(self):
        """ Test the ``get_is_done_task_flag`` method with the tag name attribute set to an unknown value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode, attrs={'task': 'johndoe'})
        self.assertFalse(tree_node.get_is_done_task_flag())

    def test_get_is_done_task_flag_without_value_set(self):
        """ Test the ``get_is_done_task_flag`` method without the done flag set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode)
        self.assertFalse(tree_node.get_is_done_task_flag())

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = '<li class="task_pending">test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_is_done(self):
        """ Test the ``render_html`` method with a "done" task. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode, attrs={'done': ''})
        output_result = tree_node.render_html('test')
        expected_result = '<li class="task_done">test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode)
        output_result = tree_node.render_text('test\ntest2\n')
        expected_result = '[ ] test\n    test2\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode)
        output_result = tree_node.render_text('    test\ntest2\n    ')
        expected_result = '[ ] test\n    test2\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_is_done(self):
        """ Test the ``render_text`` method with a "done" task. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('task', TodoTaskTreeNode, attrs={'done': ''})
        output_result = tree_node.render_text('test\ntest2\n')
        expected_result = '[x] test\n    test2\n'
        self.assertEqual(expected_result, output_result)
