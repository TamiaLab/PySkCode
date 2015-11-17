"""
SkCode coloured text tag definitions code.
"""

import re

from .base import TagOptions
from ..tools import escape_attrvalue


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
        user_color_value = tree_node.attrs.get(tree_node.name, '')
        if not user_color_value:
            return ''

        # Accept RGB hex value or color name
        if RGB_COLOR_RE.match(user_color_value):
            return user_color_value
        elif user_color_value in self.known_colors:
            return user_color_value
        else:
            return ''

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get color value
        color = self.get_color_value(tree_node)

        # If no color -> direct output
        if not color:
            return inner_html

        # Render the color
        return '<span style="color: %s">%s</span>' % (color, inner_html)

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
        
        # Get color value
        color = self.get_color_value(tree_node)

        # If no color -> direct output
        if not color:
            return inner_skcode

        # Return the code
        node_name = tree_node.name
        return '[%s=%s]%s[/%s]' % (node_name, escape_attrvalue(color), inner_skcode, node_name)


class FixedColorTextTagOptions(ColorTextTagOptions):
    """ Fixed coloured tag options container class. """

    def __init__(self, color_value, **kwargs):
        """
        Fixed color text tag constructor.
        :param color_value: Text color to use.
        :param kwargs: Keyword arguments for super.
        """
        super(FixedColorTextTagOptions, self).__init__(**kwargs)
        self.color_value = color_value

    def get_color_value(self, tree_node):
        """
        Return the color value.
        :param tree_node: The current tree node instance.
        :return The color value as set set in __init__.
        """
        return self.color_value

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)
