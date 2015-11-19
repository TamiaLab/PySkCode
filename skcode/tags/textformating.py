"""
SkCode text formating tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import (InlineWrappingTagOptions,
                   TagOptions)


class BoldTextTagOptions(InlineWrappingTagOptions):
    """ Bold text tag options container class. """

    def __init__(self, **kwargs):
        super(BoldTextTagOptions, self).__init__('<strong>%s</strong>', **kwargs)


class ItalicTextTagOptions(InlineWrappingTagOptions):
    """ Italic text tag options container class. """

    def __init__(self, **kwargs):
        super(ItalicTextTagOptions, self).__init__('<em>%s</em>', **kwargs)


class StrikeTextTagOptions(InlineWrappingTagOptions):
    """ Strike text tag options container class. """

    def __init__(self, **kwargs):
        super(StrikeTextTagOptions, self).__init__('<del>%s</del>', **kwargs)


class UnderlineTextTagOptions(InlineWrappingTagOptions):
    """ Underline text tag options container class. """

    def __init__(self, **kwargs):
        super(UnderlineTextTagOptions, self).__init__('<ins>%s</ins>', **kwargs)


class SubscriptTextTagOptions(InlineWrappingTagOptions):
    """ Subscript text tag options container class. """

    def __init__(self, **kwargs):
        super(SubscriptTextTagOptions, self).__init__('<sub>%s</sub>', **kwargs)


class SupscriptTextTagOptions(InlineWrappingTagOptions):
    """ Supscript text tag options container class. """

    def __init__(self, **kwargs):
        super(SupscriptTextTagOptions, self).__init__('<sup>%s</sup>', **kwargs)


class PreTextTagOptions(InlineWrappingTagOptions):
    """ Pre text tag options container class. """

    def __init__(self, **kwargs):
        super(PreTextTagOptions, self).__init__('<pre>%s</pre>', **kwargs)

class CiteTextTagOptions(InlineWrappingTagOptions):
    """ Cite text tag options container class. """

    def __init__(self, **kwargs):
        super(CiteTextTagOptions, self).__init__('<cite>%s</cite>', **kwargs)


class InlineCodeTextTagOptions(TagOptions):
    """ Inline code text tag options container class. """

    parse_embedded = False
    inline = True
    close_inlines = False

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Wrap the inner HTML code using the wrapping format.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        return '<code>%s</code>' % content

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Return the inner text as-is.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode. Wrap the inner SkCode with the node name tag, without arguments.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, content, node_name)


class InlineSpoilerTextTagOptions(InlineWrappingTagOptions):
    """ Inline spoiler text tag options container class. """

    def __init__(self, **kwargs):
        super(InlineSpoilerTextTagOptions, self).__init__('<span class="ispoiler">%s</span>', **kwargs)


class KeyboardTextTagOptions(InlineWrappingTagOptions):
    """ Keyboard text tag options container class. """

    def __init__(self, **kwargs):
        super(KeyboardTextTagOptions, self).__init__('<kbd>%s</kbd>', **kwargs)


class HighlightTextTagOptions(InlineWrappingTagOptions):
    """ Highlight text tag options container class. """

    def __init__(self, **kwargs):
        super(HighlightTextTagOptions, self).__init__('<mark>%s</mark>', **kwargs)


class SmallTextTagOptions(InlineWrappingTagOptions):
    """ Small text tag options container class. """

    def __init__(self, **kwargs):
        super(SmallTextTagOptions, self).__init__('<small>%s</small>', **kwargs)
