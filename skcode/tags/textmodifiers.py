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
        assert text_modifier, "The text modifier is mandatory."
        super(TextModifierBaseTagOptions, self).__init__(**kwargs)
        self.text_modifier = text_modifier

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<span class="text-%s">%s</span>\n' % (self.text_modifier, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        if self.text_modifier == "lowercase":
            return inner_text.lower()
        elif self.text_modifier == "uppercase":
            return inner_text.upper()
        elif self.text_modifier == "capitalize":
            return inner_text.capitalize()
        else:
            return inner_text


class LowerCaseTextTagOptions(TextModifierBaseTagOptions):
    """ Lowercase text modifier tag options container class. """

    def __init__(self, **kwargs):
        super(LowerCaseTextTagOptions, self).__init__('lowercase', **kwargs)


class UpperCaseTextTagOptions(TextModifierBaseTagOptions):
    """ Uppercase text modifier tag options container class. """

    def __init__(self, **kwargs):
        super(UpperCaseTextTagOptions, self).__init__('uppercase', **kwargs)


class CapitalizeTextTagOptions(TextModifierBaseTagOptions):
    """ Capitalize text modifier tag options container class. """

    def __init__(self, **kwargs):
        super(CapitalizeTextTagOptions, self).__init__('capitalize', **kwargs)
