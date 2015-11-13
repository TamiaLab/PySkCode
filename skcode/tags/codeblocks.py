"""
SkCode code block tag definitions code (require Pygments library).
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

from .base import TagOptions
from ..tools import (sanitize_url,
                     escape_attrvalue)


class CodeBlockTagOptions(TagOptions):
    """ Code block tag options container class. """

    parse_embedded = False
    swallow_trailing_newline = True

    # Tabulation size in spaces
    tab_size = 4

    # Pygments CSS style name
    pygments_css_style_name = 'default'

    # Display line numbers
    display_line_numbers = True

    # Default language name
    default_language_name = 'text'

    # Language attribute name
    language_attr_name = 'language'

    # Highlight lines attribute name
    hl_lines_attr_name = 'hl_lines'

    # Start line number attribute name
    line_start_num_attr_name = 'linenostart'

    # Filename attribute name
    filename_attr_name = 'filename'

    # Source link attribute name
    source_link_attr_name = 'src'

    def get_language_name(self, tree_node):
        """
        Return the language name of this code block for syntax highlighting.
        The language name can be set by setting the language_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), language_attr_name.
        :param tree_node: The current tree node instance.
        :return The language name of this code block, or the default one if not specified.
        """
        language_name = tree_node.attrs.get(tree_node.name, '')
        if not language_name:
            language_name = tree_node.attrs.get(self.language_attr_name, self.default_language_name)
        return language_name

    def get_highlight_lines(self, tree_node):
        """
        Return the list of lines which has to be highlighted.
        :param tree_node: The current tree node instance.
        :return A list of line numbers as int.
        """

        # Get the list as string
        highlight_lines = tree_node.attrs.get(self.hl_lines_attr_name, '')

        # Shortcut if no line
        line_nums = []
        if not highlight_lines:
            return line_nums

        # Turn all line number into int
        for line_num in highlight_lines.split(','):
            try:
                line_nums.append(int(line_num))
            except ValueError:
                continue

        # Return the list
        return line_nums

    def get_start_line_number(self, tree_node):
        """
        Return the line number of the first line.
        :param tree_node: The current tree node instance.
        :return: The line number to be used for the first line, or 1 if not specified.
        """

        # Get the line number as string
        first_line_number = tree_node.attrs.get(self.line_start_num_attr_name, None)

        # Shortcut if no line number
        if first_line_number is None:
            return 1

        # Return the line number as int
        try:
            return int(first_line_number)

        except ValueError:
            # Handle error
            return 1

    def get_filename(self, tree_node):
        """
        Return the filename of the current code block (optional).
        :param tree_node: The current tree node instance.
        :return: The filename associated with the current code block, or an empty string.
        """
        return tree_node.attrs.get(self.filename_attr_name, '')

    def get_source_link_url(self, tree_node):
        """
        Return the source link URL of the current code block (optional).
        :param tree_node: The current tree node instance.
        :return: The source URL of the current code block, or an empty string.
        """
        return tree_node.attrs.get(self.source_link_attr_name, '')

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Render the source code
        try:
            lexer = get_lexer_by_name(self.get_language_name(tree_node),
                                      stripall=True,
                                      tabsize=self.tab_size)
        except ClassNotFound:

            # Handle unknown language name
            lexer = get_lexer_by_name(self.default_language_name,
                                      stripall=True,
                                      tabsize=self.tab_size)
        style = get_style_by_name(self.pygments_css_style_name)
        formatter = HtmlFormatter(style=style,
                                  linenos='table' if self.display_line_numbers else False,
                                  hl_lines=self.get_highlight_lines(tree_node),
                                  linenostart=self.get_start_line_number(tree_node),
                                  noclasses=True)
        source_code = highlight(tree_node.content, lexer, formatter)

        # Get extra filename and source link
        src_filename = self.get_filename(tree_node)
        src_filename = unescape_html_entities(src_filename)
        src_filename = escape_html(src_filename)

        src_link_url = self.get_source_link_url(tree_node)
        src_link_url = sanitize_url(src_link_url)

        # Render the HTML block
        if src_filename or src_link_url:

            # Source code with caption
            if src_filename:
                caption = src_filename
            else:
                caption = 'Source : %s' % src_link_url

            # And source link
            if src_link_url:
                extra_args = ' rel="nofollow"' if force_rel_nofollow else ''
                caption = '<a href="%s"%s target="_blank">%s ' \
                          '<i class="fa fa-link"></i></a>' % (src_link_url, extra_args, caption)

            return """<figure>
    <figcaption>%s</figcaption>
%s
</figure>""" % (caption, source_code)

        else:
            # Source code only
            return '%s\n' % source_code

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        lines = []
        for num, line in enumerate(tree_node.content.splitlines(), start=1):
            line = line.replace('\t', ' ' * self.tab_size)
            line_prefix = '%d.' % num
            lines.append('%s %s' % (line_prefix.ljust(4), line))
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get all attributes
        language_name = self.get_language_name(tree_node)
        if language_name != self.default_language_name:
            extra_attrs = ' %s=%s' % (self.language_attr_name,
                                      escape_attrvalue(language_name))
        else:
            extra_attrs = ''

        hl_lines = self.get_highlight_lines(tree_node)
        if hl_lines:
            extra_attrs += ' %s=%s' % (self.hl_lines_attr_name,
                                       escape_attrvalue(','.join(hl_lines)))

        linenostart = self.get_start_line_number(tree_node)
        if linenostart != 1:
            extra_attrs += ' %s="%d"' % (self.line_start_num_attr_name,
                                         linenostart)

        src_filename = self.get_filename(tree_node)
        src_filename = unescape_html_entities(src_filename)
        if src_filename:
            extra_attrs += ' %s=%s' % (self.filename_attr_name,
                                       escape_attrvalue(src_filename))

        src_link_url = self.get_source_link_url(tree_node)
        src_link_url = sanitize_url(src_link_url)
        if src_link_url:
            extra_attrs += ' %s=%s' % (self.source_link_attr_name,
                                       escape_attrvalue(src_link_url))

        # Render the skcode
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs,
                                  tree_node.content, node_name)


class FixedCodeBlockTagOptions(CodeBlockTagOptions):
    """ Fixed language code block tag options container class. """

    def __init__(self, language_name, **kwargs):
        """
        Fixed language code block tag constructor.
        :param language_name: The language name to use.
        :param kwargs: Keyword arguments for super constructor.
        """
        super(FixedCodeBlockTagOptions, self).__init__(**kwargs)
        self.language_name = language_name

    def get_language_name(self, tree_node):
        """
        Return the language name of this code block for syntax highlighting.
        :param tree_node: The current tree node instance.
        :return The language name of this code block, as set in __init__.
        """
        return self.language_name

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get all attributes
        hl_lines = self.get_highlight_lines(tree_node)
        if hl_lines:
            extra_attrs = ' %s=%s' % (self.hl_lines_attr_name,
                                      escape_attrvalue(','.join(hl_lines)))
        else:
            extra_attrs = ''

        linenostart = self.get_start_line_number(tree_node)
        if linenostart != 1:
            extra_attrs += ' %s="%d"' % (self.line_start_num_attr_name,
                                         linenostart)

        src_filename = self.get_filename(tree_node)
        src_filename = unescape_html_entities(src_filename)
        if src_filename:
            extra_attrs += ' %s=%s' % (self.filename_attr_name,
                                       escape_attrvalue(src_filename))

        src_link_url = self.get_source_link_url(tree_node)
        src_link_url = sanitize_url(src_link_url)
        if src_link_url:
            extra_attrs += ' %s=%s' % (self.source_link_attr_name,
                                       escape_attrvalue(src_link_url))

        # Render the skcode
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs,
                                  tree_node.content, node_name)
