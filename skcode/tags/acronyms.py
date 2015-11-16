"""
SkCode acronym tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions
from ..tools import escape_attrvalue


class AcronymTagOptions(TagOptions):
    """ Acronym tag options container class. """

    inline = True
    close_inlines = False

    # Acronym title attribute name
    acronym_title_attr_name = 'title'

    def get_acronym_title(self, tree_node):
        """
        Get the title for this acronym.
        The title can be set by setting the acronym_title_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), acronym_title_attr_name.
        :param tree_node: The current tree node instance.
        :return The acronym title if set, or an empty string.
        """
        abbr_title = tree_node.attrs.get(tree_node.name, '')
        if not abbr_title:
            abbr_title = tree_node.attrs.get(self.acronym_title_attr_name, '')
        return unescape_html_entities(abbr_title)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        abbr_title = self.get_acronym_title(tree_node)
        if not abbr_title:
            return inner_html
        else:
            return '<abbr title="%s">%s</abbr>' % (escape_html(abbr_title), inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        abbr_title = self.get_acronym_title(tree_node)
        if not abbr_title:
            return inner_text
        else:
            return '%s (%s)' % (inner_text, abbr_title)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        abbr_title = self.get_acronym_title(tree_node)
        return '[%s %s=%s]%s[/%s]' % (node_name, self.acronym_title_attr_name,
                                      escape_attrvalue(abbr_title), inner_skcode, node_name)
