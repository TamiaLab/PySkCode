"""
SkCode acronym tag definitions code.
"""

import string

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions


class AcronymTagOptions(TagOptions):
    """ Acronym tag options container class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'abbr'
    alias_tag_names = ('acronym', )

    # Acronym title attribute name
    acronym_title_attr_name = 'title'

    # HTML template for rendering
    html_render_template = '<abbr title="{title}">{inner_html}</abbr>'

    # Text template for rendering
    text_render_template = '{inner_text} ({title})'

    def get_acronym_title(self, tree_node):
        """
        Get the title for this acronym.
        The title can be set by setting the ``acronym_title_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``acronym_title_attr_name``.
        :param tree_node: The current tree node instance.
        :return The acronym title if set, or an empty string.
        """
        abbr_title = tree_node.attrs.get(tree_node.name, '')
        if not abbr_title:
            abbr_title = tree_node.attrs.get(self.acronym_title_attr_name, '')
        return unescape_html_entities(abbr_title)

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        abbr_title = self.get_acronym_title(tree_node)
        if abbr_title:
            return self.html_render_template.format(title=escape_html(abbr_title), inner_html=inner_html)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        abbr_title = self.get_acronym_title(tree_node)
        if abbr_title:
            end_of_str = inner_text[-1] if inner_text[-1] in string.whitespace else ''
            inner_text = inner_text.rstrip()
            return self.text_render_template.format(title=abbr_title, inner_text=inner_text) + end_of_str
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
        return {
                   self.acronym_title_attr_name: self.get_acronym_title(tree_node)
               }, self.acronym_title_attr_name
