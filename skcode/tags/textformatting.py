"""
SkCode text formatting tag definitions code.
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
        return '<code>%s</code>' % content

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


class InlineSpoilerTextTagOptions(InlineWrappingTagOptions):
    """ Inline spoiler text tag options container class. """

    # CSS class name for the ``span`` element
    css_class_name = 'ispoiler'

    def __init__(self, **kwargs):
        css_class_name = kwargs.get('css_class_name', self.css_class_name)
        super(InlineSpoilerTextTagOptions, self).__init__('<span class="{}">%s</span>'.format(css_class_name), **kwargs)


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
