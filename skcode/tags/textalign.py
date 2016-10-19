"""
SkCode text align tag definitions code.
"""

from ..etree import TreeNode


class TextAlignBaseTreeNode(TreeNode):
    """ Base class for all text alignment tag class. """

    # HTML template for rendering
    html_render_template = '<p class="text-{text_alignment}">{inner_html}</p>\n'

    # Default text alignment
    text_alignment = ''

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(text_alignment=self.text_alignment, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class CenterTextTreeNode(TextAlignBaseTreeNode):
    """ Center align text tree node class. """

    canonical_tag_name = 'center'
    alias_tag_names = ()

    text_alignment = 'center'


class LeftTextTreeNode(TextAlignBaseTreeNode):
    """ Left align text tree node class. """

    canonical_tag_name = 'left'
    alias_tag_names = ()

    text_alignment = 'left'


class RightTextTreeNode(TextAlignBaseTreeNode):
    """ Right align text tree node class. """

    canonical_tag_name = 'right'
    alias_tag_names = ()

    text_alignment = 'right'


class JustifyTextTreeNode(TextAlignBaseTreeNode):
    """ Justify align text tree node class. """

    canonical_tag_name = 'justify'
    alias_tag_names = ()

    text_alignment = 'justify'
