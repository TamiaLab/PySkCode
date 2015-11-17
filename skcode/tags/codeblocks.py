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
                     escape_attrvalue,
                     slugify)


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

    # Figure ID attribute name
    figure_id_attr_name = 'id'

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
        return unescape_html_entities(language_name)

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
            line_num = line_num.strip()
            if not line_num:
                continue
            try:
                line_num = int(line_num)
                if line_num >= 0:
                    line_nums.append(line_num)
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
        first_line_number = tree_node.attrs.get(self.line_start_num_attr_name, '')

        # Shortcut if no line number
        if not first_line_number:
            return 1

        # Return the line number as int
        try:
            line_num = int(first_line_number)
            if line_num >= 0:
                return line_num
            else:
                return 1

        except ValueError:
            # Handle error
            return 1

    def get_filename(self, tree_node):
        """
        Return the filename of the current code block (optional).
        :param tree_node: The current tree node instance.
        :return: The filename associated with the current code block, or an empty string.
        """
        filename = tree_node.attrs.get(self.filename_attr_name, '')
        return unescape_html_entities(filename)

    def get_source_link_url(self, tree_node):
        """
        Return the source link URL of the current code block (optional).
        :param tree_node: The current tree node instance.
        :return: The source URL of the current code block, or an empty string.
        """
        src_link_url = tree_node.attrs.get(self.source_link_attr_name, '')
        return sanitize_url(src_link_url)

    def get_figure_id(self, tree_node):
        """
        Return the figure ID for this code block.
        :param tree_node: The current tree node instance.
        :return: The figure ID for this code block, or an empty string.
        """
        figure_id = tree_node.attrs.get(self.figure_id_attr_name, '')
        return slugify(figure_id)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get figure ID
        figure_id = self.get_figure_id(tree_node)

        # Handle line anchors
        if figure_id:
            lineanchors = figure_id
            anchorlinenos = True
        else:
            lineanchors = ''
            anchorlinenos = False

        # Render the source code
        try:
            lexer = get_lexer_by_name(self.get_language_name(tree_node),
                                      tabsize=self.tab_size)
        except ClassNotFound:

            # Handle unknown language name
            lexer = get_lexer_by_name(self.default_language_name,
                                      tabsize=self.tab_size)
        style = get_style_by_name(self.pygments_css_style_name)
        formatter = HtmlFormatter(style=style,
                                  linenos='table' if self.display_line_numbers else False,
                                  hl_lines=self.get_highlight_lines(tree_node),
                                  linenostart=self.get_start_line_number(tree_node),
                                  noclasses=True,
                                  lineanchors=lineanchors,
                                  anchorlinenos=anchorlinenos)
        source_code = highlight(tree_node.content, lexer, formatter)

        # Get extra filename and source link
        src_filename = self.get_filename(tree_node)
        src_link_url = self.get_source_link_url(tree_node)

        # Render the HTML block
        if src_filename or src_link_url:

            # Source code with caption
            if src_filename:
                caption = escape_html(src_filename)
            else:
                caption = 'Source : %s' % src_link_url

            # And source link
            if src_link_url:
                extra_args = ' rel="nofollow"' if force_rel_nofollow else ''
                caption = '<a href="%s"%s target="_blank">%s ' \
                          '<i class="fa fa-link"></i></a>' % (src_link_url, extra_args, caption)

            # Return the final HTML
            figure_extra = ' id="%s"' % figure_id if figure_id else ''
            return """<figure%s>
%s
<figcaption>%s</figcaption>
</figure>""" % (figure_extra, source_code, caption)

        else:
            # Source code only
            figure_extra = '<a id="%s"></a>\n' % figure_id if figure_id else ''
            return '%s%s\n' % (figure_extra, source_code)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get all attributes
        figure_id = self.get_figure_id(tree_node)
        src_filename = self.get_filename(tree_node)
        src_link_url = self.get_source_link_url(tree_node)

        # Render the code block
        lines = []
        for num, line in enumerate(tree_node.content.splitlines(), start=1):
            if not line:
                continue
            line = line.replace('\t', ' ' * self.tab_size)
            line_prefix = '%d.' % num
            lines.append('%s %s' % (line_prefix.ljust(4), line))

        # Add the caption
        figure_extra = ' [#%s]' % figure_id if figure_id else ''
        if src_filename and src_link_url:
            caption = '%s (%s)%s' % (src_filename, src_link_url, figure_extra)
            lines.append(caption)
        elif src_filename:
            caption = '%s%s' % (src_filename, figure_extra)
            lines.append(caption)
        elif src_link_url:
            caption = 'Source : %s%s' % (src_link_url, figure_extra)
            lines.append(caption)

        # Finish the job
        lines.append('')
        return '\n'.join(lines)

    def get_extra_attrs_for_render_skcode(self, tree_node, include_language_attr=True):
        """
        Return all extra attributes for SkCode rendering (avoid code duplication).
        :param tree_node: The current tree node instance.
        :param include_language_attr: Set to True (default) to include the language attribute, False to exclude it.
        :return: A string with all extra attributes ready for SkCode rendering.
        """

        # Get all attributes
        language_name = self.get_language_name(tree_node)
        if language_name != self.default_language_name and include_language_attr:
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
        if src_filename:
            extra_attrs += ' %s=%s' % (self.filename_attr_name,
                                       escape_attrvalue(src_filename))

        src_link_url = self.get_source_link_url(tree_node)
        if src_link_url:
            extra_attrs += ' %s=%s' % (self.source_link_attr_name,
                                       escape_attrvalue(src_link_url))

        figure_id = self.get_figure_id(tree_node)
        if figure_id:
            extra_attrs += ' %s=%s' % (self.figure_id_attr_name,
                                       escape_attrvalue(figure_id))

        return extra_attrs

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get all attributes
        extra_attrs = self.get_extra_attrs_for_render_skcode(tree_node)

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
        extra_attrs = self.get_extra_attrs_for_render_skcode(tree_node, include_language_attr=False)

        # Render the skcode
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs,
                                  tree_node.content, node_name)
