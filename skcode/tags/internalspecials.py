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

    canonical_tag_name = 'noparse'
    alias_tag_names = ('nobbc', )

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        return content

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content

    def get_skcode_inner_content(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving the inner content of this node for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The inner content for SkCode rendering.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content
