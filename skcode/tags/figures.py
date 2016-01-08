"""
SkCode figures tag definitions code.
"""

from html import escape as escape_html

from .base import TagOptions
from ..tools import (escape_attrvalue,
                     slugify)
from skcode.render import render_inner_text


class FigureDeclarationTagOptions(TagOptions):
    """ Figure declaration tag options container class. """

    make_paragraphs_here = True

    # Figure ID attribute name
    figure_id_attr_name = 'id'

    def get_figure_id(self, tree_node):
        """
        Get the ID of this figure.
        The ID can be set by setting the figure_id_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), figure_id_attr_name.
        :param tree_node: The current tree node instance.
        :return: The ID of this figure.
        """
        figure_id = tree_node.attrs.get(tree_node.name, '')
        if not figure_id:
            figure_id = tree_node.attrs.get(self.figure_id_attr_name, '')
        return slugify(figure_id)

    def get_figure_caption_node(self, tree_node):
        """
        Return the first figure caption node found in direct children of the tree node.
        :param tree_node: The current tree node instance.
        :return: The first figure caption node instance found, or None.
        """
        for child in tree_node.children:
            if isinstance(child.opts, FigureCaptionTagOptions):
                return child
        return None

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the figure ID
        figure_id = self.get_figure_id(tree_node)

        # Render the figure
        figure_attr = '' if not figure_id else ' id="%s"' % escape_html(figure_id)
        return '<figure class="thumbnail"%s>%s</figure>\n' % (figure_attr, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the figure ID
        figure_id = self.get_figure_id(tree_node)

        # Render all lines of the figure
        lines = ['+----------']
        for line in inner_text.strip().splitlines():
            lines.append('| ' + line)
        lines.append('+----------')

        # Get the figure caption
        figure_caption_node = self.get_figure_caption_node(tree_node)

        # Add the caption if provided
        if figure_caption_node is not None:

            # Render the caption inner text
            caption_text = render_inner_text(figure_caption_node)

            # Render all line of the caption
            for line in caption_text.strip().splitlines():
                lines.append('| ' + line)
            lines.append('+----------')

        # Finish the job
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the figure ID
        figure_id = self.get_figure_id(tree_node)

        # Render the figure
        extra_attrs = ' %s=%s' % (self.figure_id_attr_name,
                                  escape_attrvalue(figure_id)) if figure_id else ''
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)


class FigureCaptionTagOptions(TagOptions):
    """ Figure caption tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<figcaption class="caption">%s</figcaption>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # No text rendering (done in parent)
        return ''

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)
