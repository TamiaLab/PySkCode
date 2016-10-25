"""
SkCode Post scriptum tag definitions code.
"""

from ..etree import TreeNode


class PostScriptumTreeNode(TreeNode):
    """ Post scriptum tree node class. """

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

    def get_is_important_flag(self):
        """
        Get the "is important" flag.
        The flag can be set by set the ``is_important_attr_name`` attribute or by setting the
        tag name value to ``is_important_tagname_value``.
        The lookup order is: ``is_important_attr_name`` attribute (first), tag name value, ``False``.
        :return A boolean True if the Post scriptum is important, False if not.
        """
        return self.has_attribute_switch_set(self.is_important_attr_name, self.is_important_tagname_value)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        if self.get_is_important_flag():
            return self.html_render_important_template.format(inner_html=inner_html)
        else:
            return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        if self.get_is_important_flag():
            return self.text_render_important_template.format(inner_text=inner_text.strip())
        else:
            return self.text_render_template.format(inner_text=inner_text.strip())
