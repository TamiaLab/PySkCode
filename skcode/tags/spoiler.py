"""
SkCode spoiler tag definitions code.
"""

from .base import TagOptions


class SpoilerTagOptions(TagOptions):
    """ Spoiler tag options container class. """

    make_paragraphs_here = True

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<div class="spoiler">%s</div>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        lines = ['!!! SPOILER !!!']
        for line in inner_text.splitlines():
            lines.append('! ' + line)
        lines.append('!!!')
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)
