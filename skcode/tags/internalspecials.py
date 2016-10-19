"""
SkCode special internal tag definitions code.
"""

from ..etree import TreeNode

from html import escape as escape_html
from html import unescape as unescape_html_entities


class NoParseTreeNode(TreeNode):
    """ "No Parse" tree node class. """

    parse_embedded = False
    inline = True
    close_inlines = False

    canonical_tag_name = 'noparse'
    alias_tag_names = ('nobbc', )

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        content = self.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        return content

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        content = self.content
        content = unescape_html_entities(content)
        return content
