"""
SkCode definitions list tag definitions code.
"""

from .base import TagOptions


class DefinitionListTagOptions(TagOptions):
    """ Definitions list tag options container class. """

    # FIXME Maybe post-process the tree to assert term/definition order

    canonical_tag_name = 'dl'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<dl>{inner_html}</dl>\n'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class DefinitionListTermTagOptions(TagOptions):
    """ Definitions list term tag options container class. """

    canonical_tag_name = 'dt'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<dt>{inner_html}</dt>\n'

    # Text template for the rendering
    render_text_template = '{inner_text} : '

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return self.render_text_template.format(inner_text=inner_text.strip())


class DefinitionListTermDefinitionTagOptions(TagOptions):
    """ Definition list term definition tag options container class. """

    canonical_tag_name = 'dd'
    alias_tag_names = ()

    make_paragraphs_here = True

    # HTML template for the rendering
    render_html_template = '<dd>{inner_html}</dd>\n'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text.strip()
