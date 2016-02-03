"""
SkCode text direction tag definitions code.
"""

from .base import TagOptions


# Text directions
TEXT_DIR_LEFT_TO_RIGHT = 1
TEXT_DIR_RIGHT_TO_LEFT = 2


class DirectionTextTagOptions(TagOptions):
    """ Custom direction text tag options container class. """

    inline = True
    close_inlines = False

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

    def get_text_direction(self, tree_node):
        """
        Get the text direction.
        The text direction can be set by setting the ``text_direction_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``text_direction_attr_name``.
        :param tree_node: The current tree node instance.
        :return The text direction of this block of text, or the default one.
        """

        # Get the user input
        user_text_direction = tree_node.attrs.get(tree_node.name, '')
        if not user_text_direction:
            user_text_direction = tree_node.attrs.get(self.text_direction_attr_name, '')

        # Remap the supplied value
        user_text_direction = user_text_direction.lower()
        if user_text_direction in self.text_direction_map:
            return self.text_direction_map[user_text_direction]
        else:
            return self.default_text_direction

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        text_direction = self.get_text_direction(tree_node)
        return '<bdo dir="%s">%s</bdo>' % (self.bdo_html_attr_value_map[text_direction], inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        text_direction = self.get_text_direction(tree_node)
        if text_direction == TEXT_DIR_RIGHT_TO_LEFT:
            return inner_text[::-1]
        else:
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
        text_direction = self.get_text_direction(tree_node)
        text_direction = self.reverse_text_direction_map[text_direction]
        return {
                   self.text_direction_attr_name: text_direction
               }, self.text_direction_attr_name


class FixedDirectionTextTagOptions(DirectionTextTagOptions):
    """ Fixed direction text tag options container class. """

    def __init__(self, text_direction, **kwargs):
        """
        Fixed direction text modifier tag constructor.
        :param text_direction: Text direction to use.
        :param kwargs: Keyword arguments for super constructor.
        """
        assert text_direction, "The text direction is mandatory."
        super(FixedDirectionTextTagOptions, self).__init__(**kwargs)
        self.text_direction = text_direction

    def get_text_direction(self, tree_node):
        """
        Get the text direction.
        :param tree_node: The current tree node instance.
        :return The text direction as set in ``__init__``.
        """
        return self.text_direction

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
