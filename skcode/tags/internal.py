"""
SkCode internal tag definitions code.
"""

from ..etree import TreeNode

from ..utility.smileys import do_smileys_replacement
from ..utility.cosmetics import do_cosmetics_replacement

from html import escape as escape_html
from html import unescape as unescape_html_entities


class TextTreeNode(TreeNode):
    """ Text tree node class. """

    inline = True
    close_inlines = False

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        content = self.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        content = do_smileys_replacement(self.root_tree_node, content)
        content = do_cosmetics_replacement(self.root_tree_node, content)
        return content

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        content = self.content
        content = unescape_html_entities(content)
        content = do_cosmetics_replacement(self.root_tree_node, content)
        return content


class NewlineTreeNode(TreeNode):
    """ Newline tree node class. """

    inline = True
    close_inlines = False

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '\n'

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return ' '


class HardNewlineTreeNode(NewlineTreeNode):
    """ Newline (hard line break variant) tree node class. """

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
