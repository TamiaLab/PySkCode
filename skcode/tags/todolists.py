"""
SkCode TODO list tag definitions code.
"""

from .base import TagOptions


class TodoListTagOptions(TagOptions):
    """ Todo list tag options container class. """

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<ul>%s</ul>\n' % inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '-- TODO LIST --\n%s\n' % inner_text


class TodoTaskTagOptions(TagOptions):
    """ Todo task tag options container class. """

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

    def get_is_done_task_flag(self, tree_node):
        """
        Get the "is done" task flag.
        The flag can be set by set the ``is_done_attr_name`` attribute or by setting the
        tag name value to ``is_done_tagname_value``.
        The lookup order is: ``is_done_attr_name`` attribute (first), tag name value, ``False``.
        :param tree_node: The current tree node instance.
        :return A boolean True if the task is done, False is the task is not.
        """
        return self.is_done_attr_name in tree_node.attrs \
               or tree_node.attrs.get(tree_node.name, '').lower() == self.is_done_tagname_value

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        html_class = self.task_done_html_class if task_is_done else self.task_pending_html_class
        return '<li class="%s">%s</li>\n' % (html_class, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        lines = []
        is_first_line = True
        for line in inner_text.strip().splitlines():
            if is_first_line:
                is_first_line = False
                lines.append('[%s] %s' % ('x' if task_is_done else ' ', line))
            else:
                lines.append('    ' + line)
        lines.append('')
        return '\n'.join(lines)

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        return {
                   'done': None
               } if task_is_done else {}, None
