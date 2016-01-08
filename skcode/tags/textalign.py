"""
SkCode text align tag definitions code.
"""

from .base import TagOptions


class TextAlignBaseTagOptions(TagOptions):
    """ Base class for all text alignment tag class. """

    def __init__(self, text_alignment, **kwargs):
        """
        Text alignment tag constructor.
        :param text_alignment: Text alignment as string, can be ``left``, ``right``, ``center`` or ``justify``.
        :param kwargs: Keywords arguments for super constructor.
        """
        super(TextAlignBaseTagOptions, self).__init__(**kwargs)
        self.text_alignment = text_alignment

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<p class="text-%s">%s</p>\n' % (self.text_alignment, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class CenterTextTagOptions(TextAlignBaseTagOptions):
    """ Center align text tag options container class. """

    def __init__(self, **kwargs):
        """
        Center algn text tag constructor.
        :param kwargs: Keywords arguments for super constructor.
        """
        super(CenterTextTagOptions, self).__init__('center', **kwargs)


class LeftTextTagOptions(TextAlignBaseTagOptions):
    """ Left align text tag options container class. """

    def __init__(self, **kwargs):
        """
        Left align text tag constructor.
        :param kwargs: Keywords arguments for super constructor.
        """
        super(LeftTextTagOptions, self).__init__('left', **kwargs)


class RightTextTagOptions(TextAlignBaseTagOptions):
    """ Right align text tag options container class. """

    def __init__(self, **kwargs):
        """
        Right align text tag constructor.
        :param kwargs: Keywords arguments for super constructor.
        """
        super(RightTextTagOptions, self).__init__('right', **kwargs)
