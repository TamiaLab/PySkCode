"""
SkCode TODO list tag definitions code.
"""

from .base import TagOptions


class TodoListTagOptions(TagOptions):
    """ Todo list tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<ul>%s</ul>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return '-- TODO LIST --\n%s' % inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class TodoTaskTagOptions(TagOptions):
    """ Todo task tag options container class. """

    make_paragraphs_here = True
    same_tag_closes = True

    # "Is done" attribute name (standalone attribute)
    is_done_attr_name = 'done'

    # HTML class for "task done"
    task_done_html_class = 'task_done'

    # HTML class for "task pending"
    task_pending_html_class = 'task_pending'

    def get_is_done_task_flag(self, tree_node):
        """
        Get the "is done" task flag.
        :param tree_node: The current tree node instance.
        :return A boolean True if the task is done, False is the task is not.
        """
        return self.is_done_attr_name in tree_node.attrs

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        html_class = self.task_done_html_class if task_is_done else self.task_pending_html_class
        return '<li class="%s">%s</li>\n' % (html_class, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        lines = []
        is_first_line = True
        for line in inner_text.splitlines():
            if is_first_line:
                is_first_line = False
                lines.append('[%s] %s' % ('x' if task_is_done else ' ', line))
            else:
                lines.append('    ' + line)
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        task_is_done = self.get_is_done_task_flag(tree_node)
        extra_attrs = ' done' if task_is_done else ''
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)
