"""
SkCode figures tag definitions code.
"""

from .base import TagOptions
from ..tools import slugify
from ..render import render_inner_text


class FigureCaptionTagOptions(TagOptions):
    """ Figure caption tag options container class. """

    canonical_tag_name = 'figcaption'
    alias_tag_names = ()

    # Figure caption CSS class name
    caption_css_class_name = 'caption'

    # HTML template for the rendering
    render_html_template = '<figcaption class="{class_name}">{inner_html}</figcaption>\n'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(class_name=self.caption_css_class_name, inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # No text rendering (done in parent)
        return ''


class FigureDeclarationTagOptions(TagOptions):
    """ Figure declaration tag options container class. """

    make_paragraphs_here = True

    canonical_tag_name = 'figure'
    alias_tag_names = ()

    # Figure ID attribute name
    figure_id_attr_name = 'id'

    # Figure caption class
    figure_caption_class = FigureCaptionTagOptions

    # Figure CSS class name
    figure_css_class_name = 'thumbnail'

    # HTML template for the rendering
    render_html_template = '<figure class="{class_name}" id="{figure_id}">{inner_html}</figure>\n'

    def get_figure_id(self, tree_node):
        """
        Get the ID of this figure.
        The ID can be set by setting the ``figure_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``figure_id_attr_name``.
        :param tree_node: The current tree node instance.
        :return: The ID of this figure, or an empty string.
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
            if isinstance(child.opts, self.figure_caption_class):
                return child
        return None

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the figure ID
        figure_id = self.get_figure_id(tree_node)

        # Render the figure
        return self.render_html_template.format(class_name=self.figure_css_class_name,
                                                figure_id=figure_id, inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

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
            caption_text = render_inner_text(figure_caption_node, **kwargs)

            # Render all line of the caption
            for line in caption_text.strip().splitlines():
                lines.append('| ' + line)
            lines.append('+----------')

        # Finish the job
        lines.append('')
        return '\n'.join(lines)

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for retrieving all attributes required for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tagvalue
        attribute name for the shortcut syntax (if required). Example: {'title': 'foobar'}, 'title'
        """
        # Get the figure ID
        figure_id = self.get_figure_id(tree_node)
        return {
                   self.figure_id_attr_name: figure_id
               }, self.figure_id_attr_name
