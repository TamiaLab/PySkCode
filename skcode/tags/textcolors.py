"""
SkCode coloured text tag definitions code.
"""

import re
from gettext import gettext as _

from ..etree import TreeNode


# Valid HEX color according https://www.w3.org/TR/CSS21/syndata.html#value-def-color
RGB_COLOR_RE = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')


class ColorTextTreeNode(TreeNode):
    """ Coloured tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'color'
    alias_tag_names = ()

    # Known plain-text color names (from CSS21).
    known_colors = (
        'aqua', 'black', 'blue',
        'fuchsia', 'gray', 'green',
        'lime', 'maroon', 'navy',
        'olive', 'orange', 'purple',
        'red', 'silver', 'teal',
        'white', 'yellow'
    )

    # HTML template for rendering
    html_render_template = '<span style="color: {color_value}">{inner_html}</span>'

    def get_color_value(self):
        """
        Return the color value.
        :return The color value as string, or an empty string.
        """

        # Get the color string
        user_color_value = self.attrs.get(self.name, '').lower()
        if not user_color_value:
            return ''

        # Accept RGB hex value or color name
        if user_color_value in self.known_colors or RGB_COLOR_RE.match(user_color_value):
            return user_color_value
        else:
            return ''

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(ColorTextTreeNode, self).sanitize_node(breadcrumb)
        if not self.get_color_value():
            self.error_message = _('Missing color value')

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        color = self.get_color_value()
        if not color:
            return inner_html
        return self.html_render_template.format(color_value=color, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


def generate_fixed_color_text_cls(color_value,
                                  canonical_tag_name=None,
                                  alias_tag_names=None):
    """
    Generate a fixed color text class at runtime.
    :param color_value: The desired fixed color value.
    :param canonical_tag_name: The canonical name of the tag.
    :param alias_tag_names: The name alias of the tag
    :return: The generated class type.
    """
    assert color_value, "The color value is mandatory."
    _canonical_tag_name = canonical_tag_name or color_value
    _alias_tag_names = alias_tag_names or ()
    _color_value = color_value

    class FixedColorTextTreeNode(ColorTextTreeNode):
        """ Fixed coloured tree node class. """

        canonical_tag_name = _canonical_tag_name
        alias_tag_names = _alias_tag_names
        color_value = _color_value

        def get_color_value(self):
            """
            Return the color value.
            :return The color value as set set in ``self.color_value``.
            """
            return self.color_value

    return FixedColorTextTreeNode
