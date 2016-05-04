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
                     slugify)
from ..utility.relative_urls import get_relative_url_base


class CodeBlockTagOptions(TagOptions):
    """ Code block tag options container class. """

    parse_embedded = False
    swallow_trailing_newline = True

    canonical_tag_name = 'code'
    alias_tag_names = ()

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

    # CSS class of the wrapping div
    wrapping_div_class_name = 'codetable'

    # HTML template of the wrapping div
    wrapping_div_html_template = """<div class="{class_name}">
    {source_code}
</div>"""

    # HTML template for the source caption text
    source_caption_html_template = 'Source : {}'

    # HTML template for the source link
    source_link_html_template = '<a href="{src_link}"{extra_args} target="_blank">{caption} ' \
                                '<i class="fa fa-link" aria-hidden="true"></i></a>'

    # HTML template for the source code (with caption)
    code_html_template = """<div class="panel panel-default" id="{figure_id}">
    <div class="panel-body">
        {source_code}
    </div>
    <div class="panel-footer">
        {caption}
    </div>
</div>"""

    # HTML template for the source code (without caption)
    code_only_html_template = '<a id="{figure_id}"></a>\n{source_code}'

    def get_language_name(self, tree_node):
        """
        Return the language name of this code block for syntax highlighting.
        The language name can be set by setting the ``language_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``language_attr_name``.
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
        relative_url_base = get_relative_url_base(tree_node.root_tree_node)
        return sanitize_url(src_link_url,
                            absolute_base_url=relative_url_base)

    def get_figure_id(self, tree_node):
        """
        Return the figure ID for this code block.
        :param tree_node: The current tree node instance.
        :return: The figure ID for this code block, or an empty string.
        """
        figure_id = tree_node.attrs.get(self.figure_id_attr_name, '')
        return slugify(figure_id)

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

        # Get figure ID
        figure_id = self.get_figure_id(tree_node)

        # Handle line anchors
        lineanchors = figure_id
        anchorlinenos = bool(figure_id)

        # Render the source code
        try:
            lexer = get_lexer_by_name(self.get_language_name(tree_node), tabsize=self.tab_size)
        except ClassNotFound:

            # Handle unknown language name
            lexer = get_lexer_by_name(self.default_language_name, tabsize=self.tab_size)

        style = get_style_by_name(self.pygments_css_style_name)
        formatter = HtmlFormatter(style=style,
                                  linenos='table' if self.display_line_numbers else False,
                                  hl_lines=self.get_highlight_lines(tree_node),
                                  linenostart=self.get_start_line_number(tree_node),
                                  noclasses=True,
                                  lineanchors=lineanchors,
                                  anchorlinenos=anchorlinenos)
        source_code = highlight(tree_node.content, lexer, formatter)

        # Wrap table in div for horizontal scrolling
        source_code = self.wrapping_div_html_template.format(class_name=self.wrapping_div_class_name,
                                                             source_code=source_code)

        # Get extra filename and source link
        src_filename = self.get_filename(tree_node)
        src_link_url = self.get_source_link_url(tree_node)

        # Render the HTML block
        if src_filename or src_link_url:

            # Source code with caption
            caption = self.source_caption_html_template.format(escape_html(src_filename) if src_filename else src_link_url)

            # And source link
            if src_link_url:
                extra_args = ' rel="nofollow"' if force_rel_nofollow else ''
                caption = self.source_link_html_template.format(src_link=src_link_url,
                                                                extra_args=extra_args,
                                                                caption=caption)

            # Return the final HTML
            return self.code_html_template.format(figure_id=figure_id, source_code=source_code, caption=caption)

        elif figure_id:
            # Source code only with anchor
            return self.code_only_html_template.format(figure_id=figure_id, source_code=source_code)

        else:
            # Source code only
            return source_code

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get all attributes
        figure_id = self.get_figure_id(tree_node)
        src_filename = self.get_filename(tree_node)
        src_link_url = self.get_source_link_url(tree_node)
        get_start_line_number = self.get_start_line_number(tree_node)
        hl_lines = self.get_highlight_lines(tree_node)

        # Render the code block
        lines = []
        for num, line in enumerate(tree_node.content.strip('\r\n').splitlines(), start=get_start_line_number):
            line = line.replace('\t', ' ' * self.tab_size)
            line_prefix = '%d>' % num if num in hl_lines else '%d.' % num
            lines.append('%s %s' % (line_prefix.ljust(4), line))

        # Add the caption
        figure_extra = ' [#%s]' % figure_id if figure_id else ''
        if src_filename and src_link_url:
            caption = 'Source : %s (%s)%s' % (src_filename, src_link_url, figure_extra)
            lines.append(caption)
        elif src_filename:
            caption = 'Source : %s%s' % (src_filename, figure_extra)
            lines.append(caption)
        elif src_link_url:
            caption = 'Source : %s%s' % (src_link_url, figure_extra)
            lines.append(caption)

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
        language_name = self.get_language_name(tree_node)
        language_name = language_name if language_name != self.default_language_name else ''
        hl_lines = self.get_highlight_lines(tree_node)
        linenostart = self.get_start_line_number(tree_node)
        linenostart = linenostart if linenostart != 1 else ''
        src_filename = self.get_filename(tree_node)
        src_link_url = self.get_source_link_url(tree_node)
        figure_id = self.get_figure_id(tree_node)
        return {
                   self.language_attr_name: language_name,
                   self.hl_lines_attr_name: ','.join(str(line) for line in hl_lines),
                   self.line_start_num_attr_name: str(linenostart),
                   self.filename_attr_name: src_filename,
                   self.source_link_attr_name: src_link_url,
                   self.figure_id_attr_name: figure_id
               }, self.language_attr_name

    def get_skcode_inner_content(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving the inner content of this node for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The inner content for SkCode rendering.
        """
        return tree_node.content


class FixedCodeBlockTagOptions(CodeBlockTagOptions):
    """ Fixed language code block tag options container class. """

    canonical_tag_name = None
    alias_tag_names = ()

    def __init__(self, language_name, canonical_tag_name=None, **kwargs):
        """
        Fixed language code block tag constructor.
        :param language_name: The language name to use.
        :param canonical_tag_name: The canonical name of this tag, default to the language name string.
        :param kwargs: Keyword arguments for super constructor.
        """
        assert language_name, "The language name is mandatory."
        self.canonical_tag_name = canonical_tag_name or language_name
        super(FixedCodeBlockTagOptions, self).__init__(**kwargs)
        self.language_name = language_name

    def get_language_name(self, tree_node):
        """
        Return the language name of this code block for syntax highlighting.
        :param tree_node: The current tree node instance.
        :return The language name of this code block, as set in ``__init__``.
        """
        return self.language_name

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        attrs, name = super(FixedCodeBlockTagOptions, self).get_skcode_attributes(tree_node, inner_skcode, **kwargs)
        attrs.pop(self.language_attr_name)
        return attrs, None
