"""
SkCode text direction tag definitions code.
"""

from ..etree import TreeNode


# Text directions
TEXT_DIR_LEFT_TO_RIGHT = 1
TEXT_DIR_RIGHT_TO_LEFT = 2


class DirectionTextTreeNode(TreeNode):
    """ Custom direction text tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'bdo'
    alias_tag_names = ()

    # Default text direction
    default_text_direction = TEXT_DIR_LEFT_TO_RIGHT

    # Text direction map {attribute value: direction}
    text_direction_map = {
        'ltr': TEXT_DIR_LEFT_TO_RIGHT,
        'rtl': TEXT_DIR_RIGHT_TO_LEFT,
    }

    # Reverse text direction map
    reverse_text_direction_map = {
        TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
        TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
    }

    # HTML text direction LUT map
    bdo_html_attr_value_map = {
        TEXT_DIR_LEFT_TO_RIGHT: 'ltr',
        TEXT_DIR_RIGHT_TO_LEFT: 'rtl',
    }

    # Text direction attribute name
    text_direction_attr_name = 'dir'

    # HTML template for rendering
    html_render_template = '<bdo dir="{text_direction}">{inner_html}</bdo>'

    def get_text_direction(self):
        """
        Get the text direction.
        The text direction can be set by setting the ``text_direction_attr_name`` attribute
        of the tag or simply by setting the tag name attribute.
        The lookup order is: tag name (first), ``text_direction_attr_name``.
        :return The text direction of this block of text, or the default one.
        """

        # Get the user input
        user_text_direction = self.get_attribute_value('', self.text_direction_attr_name)

        # Remap the supplied value
        user_text_direction = user_text_direction.lower()
        if user_text_direction in self.text_direction_map:
            return self.text_direction_map[user_text_direction]
        else:
            return self.default_text_direction

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        text_direction = self.get_text_direction()
        return self.html_render_template.format(text_direction=self.bdo_html_attr_value_map[text_direction],
                                                inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        text_direction = self.get_text_direction()
        if text_direction == TEXT_DIR_RIGHT_TO_LEFT:
            return inner_text[::-1]
        else:
            return inner_text


class LTRFixedDirectionTextTreeNode(DirectionTextTreeNode):
    """ Left-to-right fixed direction text tree node class. """

    canonical_tag_name = 'ltr'
    alias_tag_names = ()

    # Text direction
    text_direction = TEXT_DIR_LEFT_TO_RIGHT

    def get_text_direction(self):
        """
        Get the text direction.
        :return The text direction as set in ``__init__``.
        """
        return self.text_direction


class RTLFixedDirectionTextTreeNode(LTRFixedDirectionTextTreeNode):
    """ Right-to-left fixed direction text tree node class. """

    canonical_tag_name = 'rtl'
    alias_tag_names = ()

    text_direction = TEXT_DIR_RIGHT_TO_LEFT
