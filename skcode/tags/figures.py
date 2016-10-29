"""
SkCode figures tag definitions code.
"""

from gettext import gettext as _

from ..etree import TreeNode
from ..tools import slugify
from ..render import render_inner_text


class FigureCaptionTreeNode(TreeNode):
    """ Figure caption tree node class. """

    canonical_tag_name = 'figcaption'
    alias_tag_names = ()

    # Figure caption CSS class name
    caption_css_class_name = 'caption'

    # HTML template for the rendering
    render_html_template = '<figcaption class="{class_name}">{inner_html}</figcaption>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(class_name=self.caption_css_class_name, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # No text rendering (done in parent)
        return ''


class FigureDeclarationTreeNode(TreeNode):
    """ Figure declaration tree node class. """

    make_paragraphs_here = True

    canonical_tag_name = 'figure'
    alias_tag_names = ()

    # Figure ID attribute name
    figure_id_attr_name = 'id'

    # Figure caption class
    figure_caption_class = FigureCaptionTreeNode

    # Figure CSS class name
    figure_css_class_name = 'thumbnail'

    # HTML template for the rendering
    render_html_template = '<figure class="{class_name}" id="{figure_id}">{inner_html}</figure>\n'

    # Cached figure counter attribute name (for this node)
    cached_figure_counter_attr_name = '_cached_figure_counter'

    # Last figure counter attribute name (for the root node)
    last_figure_counter_attr_name = '_last_figure_counter'

    # Format string for the figure counter
    figure_counter_format = 'figure-{}'

    def get_figure_id_from_counter(self):
        """
        Get the figure ID from the counter stored in the root tree node or in the tree node cache.
        :return: The figure ID retrieved from the root tree node counter.
        """

        # Get the ID from the node cache if exists
        if hasattr(self, self.cached_figure_counter_attr_name):
            return self.figure_counter_format.format(getattr(self, self.cached_figure_counter_attr_name))

        # Get the current counter value
        counter = getattr(self.root_tree_node, self.last_figure_counter_attr_name, 0)

        # Increment and store the counter
        counter += 1
        setattr(self.root_tree_node, self.last_figure_counter_attr_name, counter)

        # Store the ID in the node cache to avoid multiple ID generation
        setattr(self, self.cached_figure_counter_attr_name, counter)

        # Return the ID for this figure
        return self.figure_counter_format.format(counter)

    def get_figure_id(self):
        """
        Get the ID of this figure.
        The ID can be set by setting the ``figure_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute. If not set at all, an auto-generated ID will be used.
        The lookup order is: tag name (first), ``figure_id_attr_name``, the auto generated ID.
        :return: The ID of this figure, or an empty string.
        """
        figure_id = self.get_attribute_value('', self.figure_id_attr_name)
        if not figure_id:
            figure_id = self.get_figure_id_from_counter()
        return slugify(figure_id)

    def get_figure_caption_node(self):
        """
        Return the first figure caption node found in direct children of the tree node.
        :return: The first figure caption node instance found, or ``None``.
        """
        for child in self.children:
            if isinstance(child, self.figure_caption_class):
                return child
        return None

    def pre_process_node(self):
        """
        Callback function for pre-processing the given node. Allow registration of IDs, references, etc.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        """
        figure_id = self.get_figure_id()
        if figure_id in self.root_tree_node.known_ids:
            self.error_message = _('ID already used previously')
        else:
            self.root_tree_node.known_ids.add(figure_id)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        figure_id = self.get_figure_id()
        return self.render_html_template.format(class_name=self.figure_css_class_name,
                                                figure_id=figure_id, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
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
        figure_caption_node = self.get_figure_caption_node()

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
