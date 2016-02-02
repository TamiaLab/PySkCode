"""
SkCode coloured text tag definitions code.
"""

import re

from .base import TagOptions


# Valid HEX color according https://www.w3.org/TR/CSS21/syndata.html#value-def-color
RGB_COLOR_RE = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')


class ColorTextTagOptions(TagOptions):
    """ Coloured tag options container class. """

    inline = True
    close_inlines = False

    # Known plain-text color names (from CSS21).
    known_colors = (
        'aqua', 'black', 'blue',
        'fuchsia', 'gray', 'green',
        'lime', 'maroon', 'navy',
        'olive', 'orange', 'purple',
        'red', 'silver', 'teal',
        'white', 'yellow'
    )

    def get_color_value(self, tree_node):
        """
        Return the color value.
        :param tree_node: The current tree node instance.
        :return The color value as string, or None.
        """

        # Get the color string
        user_color_value = tree_node.attrs.get(tree_node.name, '').lower()
        if not user_color_value:
            return ''

        # Accept RGB hex value or color name
        if RGB_COLOR_RE.match(user_color_value) or user_color_value in self.known_colors:
            return user_color_value
        else:
            return ''

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get color value
        color = self.get_color_value(tree_node)

        # If no color -> direct output
        if not color:
            return inner_html

        # Render the color
        return '<span style="color: %s">%s</span>' % (color, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get color value
        color = self.get_color_value(tree_node)
        return {
                   tree_node.name: color
               }, tree_node.name


class FixedColorTextTagOptions(ColorTextTagOptions):
    """ Fixed coloured tag options container class. """

    def __init__(self, color_value, **kwargs):
        """
        Fixed color text tag constructor.
        :param color_value: Text color to use.
        :param kwargs: Keyword arguments for super.
        """
        assert color_value, "The color value is mandatory."
        super(FixedColorTextTagOptions, self).__init__(**kwargs)
        self.color_value = color_value

    def get_color_value(self, tree_node):
        """
        Return the color value.
        :param tree_node: The current tree node instance.
        :return The color value as set set in ``__init__``.
        """
        return self.color_value

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        return {}, None
