"""
SkCode text formatting tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from ..etree import TreeNode


class InlineWrappingTreeNode(TreeNode):
    """
    Wrapping inline tree node class.
    Subclass of ``TreeNode`` which wrap the HTML output of children nodes with a format string.
    """

    inline = True
    close_inlines = False

    # The wrapping format
    wrapping_format = None

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.wrapping_format.format(inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class BoldTextTreeNode(InlineWrappingTreeNode):
    """ Bold text tree node class. """

    canonical_tag_name = 'b'
    alias_tag_names = ('bold', 'strong')

    wrapping_format = '<strong>{}</strong>'


class ItalicTextTreeNode(InlineWrappingTreeNode):
    """ Italic text tree node class. """

    canonical_tag_name = 'i'
    alias_tag_names = ('italic', 'em')

    wrapping_format = '<em>{}</em>'


class StrikeTextTreeNode(InlineWrappingTreeNode):
    """ Strike text tree node class. """

    canonical_tag_name = 's'
    alias_tag_names = ('strike', 'del')

    wrapping_format = '<del>{}</del>'


class UnderlineTextTreeNode(InlineWrappingTreeNode):
    """ Underline text tree node class. """

    canonical_tag_name = 'u'
    alias_tag_names = ('underline', 'ins')

    wrapping_format = '<ins>{}</ins>'


class SubscriptTextTreeNode(InlineWrappingTreeNode):
    """ Subscript text tree node class. """

    canonical_tag_name = 'sub'
    alias_tag_names = ()

    wrapping_format = '<sub>{}</sub>'


class SupscriptTextTreeNode(InlineWrappingTreeNode):
    """ Supscript text tree node class. """

    canonical_tag_name = 'sup'
    alias_tag_names = ()

    wrapping_format = '<sup>{}</sup>'


class PreTextTreeNode(InlineWrappingTreeNode):
    """ Pre text tree node class. """

    canonical_tag_name = 'pre'
    alias_tag_names = ()

    wrapping_format = '<pre>{}</pre>'


class CiteTextTreeNode(InlineWrappingTreeNode):
    """ Cite text tree node class. """

    canonical_tag_name = 'cite'
    alias_tag_names = ()

    wrapping_format = '<cite>{}</cite>'


class InlineCodeTextTreeNode(TreeNode):
    """ Inline code text tree node class. """

    parse_embedded = False
    inline = True
    close_inlines = False

    canonical_tag_name = 'icode'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<code>{content}</code>'

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
        return self.html_render_template.format(content=content)

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


class InlineSpoilerTextTreeNode(InlineWrappingTreeNode):
    """ Inline spoiler text tree node class. """

    canonical_tag_name = 'ispoiler'
    alias_tag_names = ()

    wrapping_format = '<span class="ispoiler">{}</span>'


class KeyboardTextTreeNode(InlineWrappingTreeNode):
    """ Keyboard text tree node class. """

    canonical_tag_name = 'kbd'
    alias_tag_names = ('keyboard', )

    wrapping_format = '<kbd>{}</kbd>'


class HighlightTextTreeNode(InlineWrappingTreeNode):
    """ Highlight text tree node class. """

    canonical_tag_name = 'mark'
    alias_tag_names = ('glow', 'highlight')

    wrapping_format = '<mark>{}</mark>'


class SmallTextTreeNode(InlineWrappingTreeNode):
    """ Small text tree node class. """

    canonical_tag_name = 'small'
    alias_tag_names = ()

    wrapping_format = '<small>{}</small>'
