"""
SkCode Post scriptum tag definitions code.
"""

from .base import TagOptions


class PostScriptumTagOptions(TagOptions):
    """ Post scriptum tag options container class. """

    canonical_tag_name = 'postscriptum'
    alias_tag_names = ('ps', )

    # "Is important" title attribute name
    is_important_attr_name = 'important'

    # "Is important" title attribute name
    is_important_tagname_value = 'important'

    # HTML template for rendering
    html_render_template = '<p class="text-justify"><em>PS {inner_html}</em></p>\n'

    # Text template for rendering
    text_render_template = 'PS {inner_text}\n\n'

    # HTML template for rendering (important)
    html_render_important_template = '<p class="text-justify"><strong>PS {inner_html}</strong></p>\n'

    # Text template for rendering (important)
    text_render_important_template = 'PS {inner_text}\n\n'

    def get_is_important_flag(self, tree_node):
        """
        Get the "is important" flag.
        The flag can be set by set the ``is_important_attr_name`` attribute or by setting the
        tag name value to ``is_important_tagname_value``.
        The lookup order is: ``is_important_attr_name`` attribute (first), tag name value, ``False``.
        :param tree_node: The current tree node instance.
        :return A boolean True if the Post scriptum is important, False if not.
        """
        return self.is_important_attr_name in tree_node.attrs \
               or tree_node.attrs.get(tree_node.name, '').lower() == self.is_important_tagname_value

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        if self.get_is_important_flag(tree_node):
            return self.html_render_important_template.format(inner_html=inner_html)
        else:
            return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        if self.get_is_important_flag(tree_node):
            return self.text_render_important_template.format(inner_text=inner_text.strip())
        else:
            return self.text_render_template.format(inner_text=inner_text.strip())

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        is_important = self.get_is_important_flag(tree_node)
        return {
                   self.is_important_attr_name: None
               } if is_important else {}, None
