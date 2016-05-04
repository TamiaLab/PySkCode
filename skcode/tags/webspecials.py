"""
SkCode web special tag definitions code.
"""

from .base import TagOptions


class HorizontalLineTagOptions(TagOptions):
    """ Horizontal line tag options container class. """

    standalone = True

    canonical_tag_name = 'hr'
    alias_tag_names = ()

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<hr>\n'

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '----------\n'


class LineBreakTagOptions(TagOptions):
    """ Line break tag options container class. """

    standalone = True
    inline = True
    close_inlines = False

    canonical_tag_name = 'br'
    alias_tag_names = ()

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<br>\n'

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '\n'


# The famous "cut here" string, for paid content preview
CUT_HERE_STRING = '<!-- Cut Here -->'


class CutHereTagOptions(TagOptions):
    """ "Cut here" tag options container class. """

    standalone = True

    canonical_tag_name = 'cuthere'
    alias_tag_names = ()

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return CUT_HERE_STRING + '\n'

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return ''
