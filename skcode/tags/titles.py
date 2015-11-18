"""
SkCode title tag definitions code.
"""

from html import escape as escape_html

from .base import TagOptions
from ..tools import escape_attrvalue, slugify


class TitleTagOptions(TagOptions):
    """ Title tag options container class. """

    same_tag_closes = True

    # Slug ID attribute name
    slug_id_attr_name = 'id'

    def __init__(self, title_level, **kwargs):
        """
        Title tag constructor.
        :param title_level: Title level, as int, between 1 and 6 included.
        :param kwargs: Keyword arguments for super constructor.
        """
        super(TitleTagOptions, self).__init__(**kwargs)
        assert title_level > 0, "Title level must be greater than zero."
        assert title_level <= 6, "Title level must be less or equal to 6."
        self.title_level = title_level
        self.title_tagname = 'h%d' % title_level

    def get_permalink_slug(self, tree_node):
        """
        Return the permalink slug for this title.
        The permalink slug can be set by setting the slug_id_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), acronym_title_attr_name.
        :param tree_node: The current tree node instance.
        :return The permalink slug for this title, or an empty string.
        """
        
        # Get existing permalink if available
        permalink_slug = tree_node.attrs.get(tree_node.name, '')
        if not permalink_slug:
            permalink_slug = tree_node.attrs.get(self.slug_id_attr_name, '')
        return slugify(permalink_slug)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug(tree_node)
        if permalink_slug:
            inner_html = '<a id="%s">%s</a>' % (escape_html(permalink_slug), inner_html)

        # Return the HTML code
        return '<%s>%s</%s>\n' % (self.title_tagname,
                                  inner_html,
                                  self.title_tagname)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return '%s %s\n' % ('#' * self.title_level, inner_text)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug(tree_node)
        if permalink_slug:
            extra_attrs = ' id=%s' % escape_attrvalue(permalink_slug)
        else:
            extra_attrs = ''

        # Render the SkCode
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)
