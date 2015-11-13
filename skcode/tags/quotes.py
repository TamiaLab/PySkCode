"""
SkCode quote tag definitions code.
"""

import calendar
from datetime import datetime

from html import escape as escape_html

from .base import TagOptions
from ..tools import escape_attrvalue, sanitize_url


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
        The author name can be set by setting the author_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), author_attr_name.
        :param tree_node: The current tree node instance.
        :return The quote author name, or an empty string.
        """
        author_name = tree_node.attrs.get(tree_node.name, '')
        if not author_name:
            author_name = tree_node.attrs.get(self.author_attr_name, '')
        return author_name

    def get_quote_link(self, tree_node):
        """
        Return the quote source link URL.
        :param tree_node: The current tree node instance.
        :return The quote source link URL (not sanitized), or an empty string.
        """
        return tree_node.attrs.get(self.link_attr_name, '')

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

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Wrap the inner HTML code using the wrapping format.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the author name
        author_name = self.get_quote_author_name(tree_node)
        if author_name:

            # Craft author name citation
            author_html = '<cite>%s</cite>' % escape_html(author_name)

            # Get source URL
            src_link = self.get_quote_link(tree_node)
            src_link = sanitize_url(src_link)

            # Craft source link if any, and handle force_rel_nofollow
            if src_link:
                if force_rel_nofollow:
                    extra_attrs = ' rel="nofollow"'
                else:
                    extra_attrs = ''
                author_html = '<a href="%s"%s>%s</a>' % (src_link, extra_attrs, author_html)

            # Get and craft the source date
            src_date = self.get_quote_date(tree_node)
            if src_date:
                author_html = '%s - <time datetime="%s">%s</time>' % (author_html,
                                                                      src_date.isoformat(),
                                                                      src_date.strftime(self.datetime_format))

            # Craft the final HTML
            extra_html = '\n<small>%s %s</small>' % (self.write_by_word, author_html)
        else:
            extra_html = ''

        # Render the quote
        return '<blockquote>%s%s</blockquote>\n' % (inner_html, extra_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Return the inner text as-is.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Craft the quote content
        lines = []
        for line in inner_text.splitlines():
            lines.append('> ' + line)

        # Add author name one last line
        author_name = self.get_quote_author_name(tree_node)
        if author_name:
            # FIXME Maybe unescape?
            author_text = '%s' % author_name

            # Add source link
            src_link = self.get_quote_link(tree_node)
            if src_link:
                # FIXME Avoid HTML encoding in render_text
                author_text = '%s (%s)' % (author_text, sanitize_url(src_link))

            # Add source date
            src_date = self.get_quote_date(tree_node)
            if src_date:
                author_text = '%s - %s' % (author_text,
                                           src_date.strftime(self.datetime_format))

            # Append result
            lines.append('>')
            lines.append('> -- %s %s' % (self.write_by_word, author_text))

        # Finish the job
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode. Wrap the inner SkCode with the node name tag, without arguments.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the author name
        author_name = self.get_quote_author_name(tree_node)
        if author_name:
            extra_attrs = ' %s=%s' % (self.author_attr_name,
                                      escape_attrvalue(author_name))
        else:
            extra_attrs = ''

        # Get the source link
        src_link = self.get_quote_link(tree_node)
        if src_link:
            extra_attrs += ' %s=%s' % (self.link_attr_name,
                                       sanitize_url(src_link))

        # Get the source date
        src_date = self.get_quote_date(tree_node)
        if src_date:
            extra_attrs += ' %s="%d"' % (self.date_attr_name,
                                         calendar.timegm(src_date.timetuple()))

        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)
