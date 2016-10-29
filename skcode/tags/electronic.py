"""
SkCode electronic special tag definitions code.
"""

import string

from ..etree import TreeNode


class NotNotationTreeNode(TreeNode):
    """ NOT notation tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'not'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<span style="text-decoration:overline; ' \
                           'text-transform: uppercase;">{inner_html}</span>'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        beg_text = ' ' if inner_text and inner_text[0] in string.whitespace else ''
        inner_text = inner_text.upper().lstrip()
        return beg_text + '/' + inner_text if inner_text else ''
