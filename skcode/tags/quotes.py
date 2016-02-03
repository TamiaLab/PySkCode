"""
SkCode quote tag definitions code.
"""

import calendar
from datetime import datetime

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions
from ..tools import sanitize_url
from ..utility.relative_urls import get_relative_url_base


class QuoteTagOptions(TagOptions):
    """ Quote tag options container class. """

    make_paragraphs_here = True

    # Author attribute name
    author_attr_name = 'author'

    # Source link attribute name
    link_attr_name = 'link'

    # Date attribute name
    date_attr_name = 'date'

    # Translation of "write by"
    write_by_word = 'par'

    # Date and time format for display
    datetime_format = '%d/%m/%Y %H:%M:%S'

    def get_quote_author_name(self, tree_node):
        """
        Return the quote author name.
        The author name can be set by setting the ``author_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``author_attr_name``.
        :param tree_node: The current tree node instance.
        :return The quote author name, or an empty string.
        """
        author_name = tree_node.attrs.get(tree_node.name, '')
        if not author_name:
            author_name = tree_node.attrs.get(self.author_attr_name, '')
        return unescape_html_entities(author_name)

    def get_quote_link(self, tree_node):
        """
        Return the quote source link URL.
        :param tree_node: The current tree node instance.
        :return The quote source link URL (not sanitized), or an empty string.
        """
        quote_link = tree_node.attrs.get(self.link_attr_name, '')
        relative_url_base = get_relative_url_base(tree_node.root_tree_node)
        return sanitize_url(quote_link,
                            convert_relative_to_absolute=bool(relative_url_base),
                            absolute_base_url=relative_url_base)

    def get_quote_date(self, tree_node):
        """
        Return the quote source date (unix timestamp).
        :param tree_node: The current tree node instance.
        :return The quote source date as datetime object or None
        """

        # Get the raw timestamp
        timestamp = tree_node.attrs.get(self.date_attr_name, '')

        # Shortcut if no timestamp
        if not timestamp:
            return None

        # Convert string to datetime
        try:
            timestamp = int(timestamp)
            return datetime.utcfromtimestamp(timestamp)
        except ValueError:
            return None

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param force_rel_nofollow: If set to ``True``, all links in the rendered HTML will have the atribute
        "rel=nofollow" to avoid search engines to scrawl them (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the author name
        author_name = self.get_quote_author_name(tree_node)
        if author_name:

            # Craft author name citation
            author_html = '<cite>%s</cite>' % escape_html(author_name)

            # Craft source link if any, and handle force_rel_nofollow
            src_link = self.get_quote_link(tree_node)
            if src_link:
                extra_attrs = ' rel="nofollow"' if force_rel_nofollow else ''
                author_html = '<a href="%s"%s>%s</a>' % (src_link, extra_attrs, author_html)

            # Get and craft the source date
            src_date = self.get_quote_date(tree_node)
            if src_date is not None:
                author_html = '%s - <time datetime="%s">%s</time>' % (author_html,
                                                                      src_date.isoformat(),
                                                                      src_date.strftime(self.datetime_format))

            # Craft the final HTML
            extra_html = '\n<small>%s %s</small>' % (self.write_by_word, author_html)
        else:
            extra_html = ''

        # Render the quote
        return '<blockquote>%s%s</blockquote>\n' % (inner_html, extra_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Craft the quote content
        lines = []
        for line in inner_text.splitlines():
            lines.append('> ' + line)

        # Add author name one last line
        author_name = self.get_quote_author_name(tree_node)
        if author_name:
            author_text = author_name

            # Add source link
            src_link = self.get_quote_link(tree_node)
            if src_link:
                author_text = '%s (%s)' % (author_text, src_link)

            # Add source date
            src_date = self.get_quote_date(tree_node)
            if src_date is not None:
                author_text = '%s - %s' % (author_text,
                                           src_date.strftime(self.datetime_format))

            # Append result
            lines.append('>')
            lines.append('> -- %s %s' % (self.write_by_word, author_text))

        # Finish the job
        lines.append('')
        return '\n'.join(lines)

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get all attributes
        author_name = self.get_quote_author_name(tree_node)
        src_link = self.get_quote_link(tree_node)
        src_date = self.get_quote_date(tree_node)
        return {
                   self.author_attr_name: author_name,
                   self.link_attr_name: src_link,
                   self.date_attr_name: str(calendar.timegm(src_date.timetuple())) if src_date else ''
               }, self.author_attr_name
