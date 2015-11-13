"""
SkCode special internal tag definitions code.
"""

from .base import TagOptions

from html import escape as escape_html
from html import unescape as unescape_html_entities


class NoParseTagOptions(TagOptions):
    """ "No Parse" tag options container class. """

    parse_embedded = False
    inline = True
    close_inlines = False

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Return the content of the node, un-escaped to void double escaped HTML
        entities, then escaped again to avoid HTML entities at all.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        return content

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Un-escaped HTML entities and returns the result as-is.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode. Un-escaped HTML entities and wrap the result with the node name tag.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, content, node_name)
