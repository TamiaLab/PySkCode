"""
SkCode TODO list tag definitions code.
"""

from ..etree import TreeNode


class TodoListTreeNode(TreeNode):
    """ TODO list tree node class. """

    canonical_tag_name = 'todolist'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<ul>{inner_html}</ul>\n'

    # Text template for rendering
    text_render_template = '-- TODO LIST --\n{inner_text}\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return self.text_render_template.format(inner_text=inner_text)


class TodoTaskTreeNode(TreeNode):
    """ TODO task tree node class. """

    canonical_tag_name = 'task'
    alias_tag_names = ()

    make_paragraphs_here = True
    same_tag_closes = True

    # "Is done" attribute name (standalone attribute)
    is_done_attr_name = 'done'

    # "Is done" value (tag name value)
    is_done_tagname_value = 'done'

    # HTML class for "task done"
    task_done_html_class = 'task_done'

    # HTML class for "task pending"
    task_pending_html_class = 'task_pending'

    # HTML template for rendering
    html_render_template = '<li class="{class_name}">{inner_html}</li>\n'

    def get_is_done_task_flag(self):
        """
        Get the "is done" task flag.
        The flag can be set by set the ``is_done_attr_name`` attribute or by setting the
        tag name value to ``is_done_tagname_value``.
        The lookup order is: ``is_done_attr_name`` attribute (first), tag name value, ``False``.
        :return A boolean True if the task is done, False is the task is not.
        """
        return self.has_attribute_switch_set(self.is_done_attr_name, self.is_done_tagname_value)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        task_is_done = self.get_is_done_task_flag()
        html_class = self.task_done_html_class if task_is_done else self.task_pending_html_class
        return self.html_render_template.format(inner_html=inner_html, class_name=html_class)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        task_is_done = self.get_is_done_task_flag()
        lines = []
        is_first_line = True
        for line in inner_text.strip().splitlines():
            if is_first_line:
                is_first_line = False
                lines.append('[{}] {}'.format('x' if task_is_done else ' ', line))
            else:
                lines.append('    ' + line)
        lines.append('')
        return '\n'.join(lines)
