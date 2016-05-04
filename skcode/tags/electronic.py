"""
SkCode electronic special tag definitions code.
"""

import string

from .base import TagOptions


class NotNotationTagOptions(TagOptions):
    """ NOT notation tag options container class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'not'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<span style="text-decoration:overline; ' \
                           'text-transform: uppercase;">{inner_html}</span>'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        if inner_text:
            beg_text = ' ' if inner_text[0] in string.whitespace else ''
        else:
            beg_text = ''
        inner_text = inner_text.upper().lstrip()
        if inner_text:
            return beg_text + '/' + inner_text
        else:
            return inner_text
