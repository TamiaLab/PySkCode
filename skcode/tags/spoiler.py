"""
SkCode spoiler tag definitions code.
"""

from .base import TagOptions


class SpoilerTagOptions(TagOptions):
    """ Spoiler tag options container class. """

    make_paragraphs_here = True

    # CSS class name for the spoiler ``div`` element
    css_class_name = 'spoiler'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<div class="%s">%s</div>\n' % (self.css_class_name, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        lines = ['!!! SPOILER !!!']
        for line in inner_text.splitlines():
            lines.append('! ' + line)
        lines.append('!!!')
        lines.append('')
        return '\n'.join(lines)
