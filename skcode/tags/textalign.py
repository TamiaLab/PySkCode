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
        assert text_alignment, "The text alignment is mandatory."
        super(TextAlignBaseTagOptions, self).__init__(**kwargs)
        self.text_alignment = text_alignment

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<p class="text-%s">%s</p>\n' % (self.text_alignment, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class CenterTextTagOptions(TextAlignBaseTagOptions):
    """ Center align text tag options container class. """

    def __init__(self, **kwargs):
        super(CenterTextTagOptions, self).__init__('center', **kwargs)


class LeftTextTagOptions(TextAlignBaseTagOptions):
    """ Left align text tag options container class. """

    def __init__(self, **kwargs):
        super(LeftTextTagOptions, self).__init__('left', **kwargs)


class RightTextTagOptions(TextAlignBaseTagOptions):
    """ Right align text tag options container class. """

    def __init__(self, **kwargs):
        super(RightTextTagOptions, self).__init__('right', **kwargs)


class JustifyTextTagOptions(TextAlignBaseTagOptions):
    """ Justify align text tag options container class. """

    def __init__(self, **kwargs):
        super(JustifyTextTagOptions, self).__init__('justify', **kwargs)
