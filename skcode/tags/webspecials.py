"""
SkCode web special tag definitions code.
"""

from ..etree import TreeNode


class HorizontalLineTreeNode(TreeNode):
    """ Horizontal line tree node class. """

    standalone = True

    canonical_tag_name = 'hr'
    alias_tag_names = ()

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<hr>\n'

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '----------\n'


class LineBreakTreeNode(TreeNode):
    """ Line break tree node class. """

    standalone = True
    inline = True
    close_inlines = False

    canonical_tag_name = 'br'
    alias_tag_names = ()

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<br>\n'

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '\n'


class CutHereTreeNode(TreeNode):
    """ "Cut here" tree node class. """

    standalone = True

    canonical_tag_name = 'cuthere'
    alias_tag_names = ()

    # The delimiter string for latter HTML splitting
    delimiter_string_html = '<!-- Cut Here -->'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '\n' + self.delimiter_string_html + '\n'

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return ''
