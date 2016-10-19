"""
SkCode title tag definitions code.
"""

from html import escape as escape_html

from ..etree import TreeNode
from ..tools import slugify


class TitleBaseTreeNode(TreeNode):
    """ Title tree node class. """

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

    # Title level (integer)
    title_level = 0

    # HTML title tag name
    html_tagname = ''

    def get_permalink_slug(self):
        """
        Return the permalink slug for this title.
        The permalink slug can be set by setting the ``slug_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``acronym_title_attr_name``.

        :return The permalink slug for this title, or an empty string.
        """

        # Get existing permalink if available
        permalink_slug = self.attrs.get(self.name, '')
        if not permalink_slug:
            permalink_slug = self.attrs.get(self.slug_id_attr_name, '')
        return slugify(permalink_slug)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug()
        if permalink_slug:
            return self.html_render_template.format(title_tagname=self.html_tagname,
                                                    slug_id=escape_html(permalink_slug),
                                                    inner_html=inner_html)
        else:
            return self.html_render_no_permalink_template.format(title_tagname=self.html_tagname,
                                                                 inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Add permalink if available
        permalink_slug = self.get_permalink_slug()
        if permalink_slug:
            return self.text_render_template.format(title_level='#' * self.title_level,
                                                    slug_id=permalink_slug,
                                                    inner_text=inner_text)
        else:
            return self.text_render_no_permalink_template.format(title_level='#' * self.title_level,
                                                                 inner_text=inner_text)


def generate_title_cls(index):
    """
    Generate the title class for the given title level index.
    :param index: The title level index.
    :return: The generated class type.
    """
    tag_name = 'h{}'.format(index)

    class TitleTreeNode(TitleBaseTreeNode):
        """ Level N title tree node """

        canonical_tag_name = tag_name
        alias_tag_names = ()

        html_tagname = tag_name
        title_level = index

    return TitleTreeNode
