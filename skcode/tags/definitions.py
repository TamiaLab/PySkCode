"""
SkCode definitions list tag definitions code.
"""

from ..etree import TreeNode


class DefinitionListTreeNode(TreeNode):
    """ Definitions list tree node class. """

    # FIXME Maybe post-process the tree to assert term/definition order

    canonical_tag_name = 'dl'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<dl>{inner_html}</dl>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class DefinitionListTermTreeNode(TreeNode):
    """ Definitions list term tree node class. """

    canonical_tag_name = 'dt'
    alias_tag_names = ()

    # HTML template for the rendering
    render_html_template = '<dt>{inner_html}</dt>\n'

    # Text template for the rendering
    render_text_template = '{inner_text} : '

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return self.render_text_template.format(inner_text=inner_text.strip())


class DefinitionListTermDefinitionTreeNode(TreeNode):
    """ Definition list term definition tree node class. """

    canonical_tag_name = 'dd'
    alias_tag_names = ()

    make_paragraphs_here = True

    # HTML template for the rendering
    render_html_template = '<dd>{inner_html}</dd>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.render_html_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text.strip()
