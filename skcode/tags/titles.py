"""
SkCode title tag definitions code.
"""

from html import escape as escape_html

from .base import TagOptions
from ..tools import slugify


class TitleTagOptions(TagOptions):
    """ Title tag options container class. """

    canonical_tag_name = None
    alias_tag_names = ()

    # Slug ID attribute name
    slug_id_attr_name = 'id'

    # HTML template for rendering (with permalink)
    html_render_template = '<{title_tagname}><a id="{slug_id}">{inner_html}</a></{title_tagname}>\n'

    # Text template for rendering (with permalink)
    text_render_template = '{title_level}[{slug_id}] {inner_text}\n'

    # HTML template for rendering (without permalink)
    html_render_no_permalink_template = '<{title_tagname}>{inner_html}</{title_tagname}>\n'

    # Text template for rendering (without permalink)
    text_render_no_permalink_template = '{title_level} {inner_text}\n'

    def __init__(self, title_level, canonical_tag_name=None, **kwargs):
        """
        Title tag constructor.
        :param title_level: Title level, as int, between 1 and 6 included.
        :param canonical_tag_name: The canonical name of this tag, default to the "hN" (with N = title level) string.
        :param kwargs: Keyword arguments for super constructor.
        """
        assert 6 >= title_level > 0, "Title level must be between zero and 6 (included)."
        self.canonical_tag_name = canonical_tag_name or 'h%d' % title_level
        super(TitleTagOptions, self).__init__(**kwargs)
        self.title_level = title_level
        self.title_tagname = 'h%d' % title_level

    def get_permalink_slug(self, tree_node):
        """
        Return the permalink slug for this title.
        The permalink slug can be set by setting the ``slug_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``acronym_title_attr_name``.
        :param tree_node: The current tree node instance.
        :return The permalink slug for this title, or an empty string.
        """

        # Get existing permalink if available
        permalink_slug = tree_node.attrs.get(tree_node.name, '')
        if not permalink_slug:
            permalink_slug = tree_node.attrs.get(self.slug_id_attr_name, '')
        return slugify(permalink_slug)

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug(tree_node)
        if permalink_slug:
            return self.html_render_template.format(title_tagname=self.title_tagname,
                                                    slug_id=escape_html(permalink_slug),
                                                    inner_html=inner_html)
        else:
            return self.html_render_no_permalink_template.format(title_tagname=self.title_tagname,
                                                                 inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug(tree_node)
        if permalink_slug:
            return self.text_render_template.format(title_level='#' * self.title_level,
                                                    slug_id=permalink_slug,
                                                    inner_text=inner_text)
        else:
            return self.text_render_no_permalink_template.format(title_level='#' * self.title_level,
                                                                 inner_text=inner_text)

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get permalink if available
        permalink_slug = self.get_permalink_slug(tree_node)
        return {
                   self.slug_id_attr_name: permalink_slug
               }, self.slug_id_attr_name
