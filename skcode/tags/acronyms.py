"""
SkCode acronym tag definitions code.
"""

import string

from gettext import gettext as _

from html import escape as escape_html
from html import unescape as unescape_html_entities

from ..etree import TreeNode


class AcronymTreeNode(TreeNode):
    """ Acronym tree node class. """

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

    def get_acronym_title(self):
        """
        Get the title for this acronym.
        The title can be set by setting the ``acronym_title_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``acronym_title_attr_name``.
        :return The acronym title if set, or an empty string.
        """
        abbr_title = self.get_attribute_value('', self.acronym_title_attr_name)
        return unescape_html_entities(abbr_title)

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(AcronymTreeNode, self).sanitize_node(breadcrumb)
        if not self.get_acronym_title():
            self.error_message = _('Missing acronym definition')

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        abbr_title = self.get_acronym_title()
        if not abbr_title:
            return inner_html
        return self.html_render_template.format(title=escape_html(abbr_title), inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        abbr_title = self.get_acronym_title()
        if not abbr_title:
            return inner_text
        end_of_str = inner_text[-1] if inner_text[-1] in string.whitespace else ''
        return self.text_render_template.format(title=abbr_title, inner_text=inner_text.rstrip()) + end_of_str
