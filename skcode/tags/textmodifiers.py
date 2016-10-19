"""
SkCode text modifiers tag definitions code.
"""

from ..etree import TreeNode


class TextModifierBaseTreeNode(TreeNode):
    """ Base class for all text modifier tag class. """

    inline = True
    close_inlines = False

    canonical_tag_name = None
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<span class="text-{text_modifier}">{inner_html}</span>\n'

    # Default text modifier
    text_modifier = ''

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(text_modifier=self.text_modifier, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
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


class LowerCaseTextTreeNode(TextModifierBaseTreeNode):
    """ Lowercase text modifier tree node class. """

    canonical_tag_name = 'lowercase'
    alias_tag_names = ()

    text_modifier = 'lowercase'


class UpperCaseTextTreeNode(TextModifierBaseTreeNode):
    """ Uppercase text modifier tree node class. """

    canonical_tag_name = 'uppercase'
    alias_tag_names = ()

    text_modifier = 'uppercase'


class CapitalizeTextTreeNode(TextModifierBaseTreeNode):
    """ Capitalize text modifier tree node class. """

    canonical_tag_name = 'capitalize'
    alias_tag_names = ()

    text_modifier = 'capitalize'
