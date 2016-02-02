"""
SkCode electronic special tag definitions code.
"""

from .base import TagOptions


class NotNotationTagOptions(TagOptions):
    """ NOT notation tag options container class. """

    inline = True
    close_inlines = False

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<span style="text-decoration:overline; ' \
               'text-transform: uppercase;">%s</span>' % inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '/%s' % inner_text.upper()
