"""
SkCode text modifiers tag definitions code.
"""

from .base import TagOptions


class TextModifierBaseTagOptions(TagOptions):
    """ Base class for all text modifier tag class. """

    inline = True
    close_inlines = False

    def __init__(self, text_modifier, **kwargs):
        """
        Text modifier tag constructor.
        :param text_modifier: Text modifier to be use, can be ``lowercase``, ``uppercase`` or ``capitalize``.
        :param kwargs: Keyword arguments for super constructor.
        """
        super(TextModifierBaseTagOptions, self).__init__(**kwargs)
        self.text_modifier = text_modifier

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<p class="text-%s">%s</p>\n' % (self.text_modifier, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        if self.text_modifier == "lowercase":
            return inner_text.lower()
        elif self.text_modifier == "uppercase":
            return inner_text.upper()
        elif self.text_modifier == "capitalize":
            return inner_text.capitalize()
        else:
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


class LowerCaseTextTagOptions(TextModifierBaseTagOptions):
    """  align text tag options container class. """

    def __init__(self, **kwargs):
        super(LowerCaseTextTagOptions, self).__init__('lowercase', **kwargs)


class UpperCaseTextTagOptions(TextModifierBaseTagOptions):
    """  align text tag options container class. """

    def __init__(self, **kwargs):
        super(UpperCaseTextTagOptions, self).__init__('uppercase', **kwargs)


class CapitalizeTextTagOptions(TextModifierBaseTagOptions):
    """  align text tag options container class. """

    def __init__(self, **kwargs):
        super(CapitalizeTextTagOptions, self).__init__('capitalize', **kwargs)
