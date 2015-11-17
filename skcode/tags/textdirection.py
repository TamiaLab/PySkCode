"""
SkCode text direction tag definitions code.
"""

from .base import TagOptions
from ..tools import escape_attrvalue


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
        The text direction can be set by setting the text_direction_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), text_direction_attr_name.
        :param tree_node: The current tree node instance.
        :return The text direction of this block of text, or the default one.
        """

        # Get the user input
        user_text_direction = tree_node.attrs.get(tree_node.name, '')
        if not user_text_direction:
            user_text_direction = tree_node.attrs.get(self.text_direction_attr_name, self.default_text_direction)

        # Remap the supplied value
        if user_text_direction in self.text_direction_map:
            return self.text_direction_map[user_text_direction]
        else:
            return self.default_text_direction

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        text_direction = self.get_text_direction(tree_node)
        return '<bdo dir="%s">%s</bdo>' % (self.bdo_html_attr_value_map[text_direction], inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        text_direction = self.get_text_direction(tree_node)
        if text_direction == TEXT_DIR_RIGHT_TO_LEFT:
            return inner_text[::-1]
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        text_direction = self.get_text_direction(tree_node)
        text_direction = self.reverse_text_direction_map[text_direction]
        node_name = tree_node.name
        return '[%s %s=%s]%s[/%s]' % (node_name, self.text_direction_attr_name,
                                      escape_attrvalue(text_direction), inner_skcode, node_name)


class FixedDirectionTextTagOptions(DirectionTextTagOptions):
    """ Fixed direction text tag options container class. """

    def __init__(self, text_direction, **kwargs):
        """
        Fixed direction text modifier tag constructor.
        :param text_direction: Text direction to use.
        :param kwargs: Keyword arguments for super constructor.
        """
        super(FixedDirectionTextTagOptions, self).__init__(**kwargs)
        self.text_direction = text_direction

    def get_text_direction(self, tree_node):
        """
        Get the text direction.
        :param tree_node: The current tree node instance.
        :return The text direction as set in __init__.
        """
        return self.text_direction

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)
