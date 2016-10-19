"""
SkCode spoiler tag definitions code.
"""

from ..etree import TreeNode


class SpoilerTreeNode(TreeNode):
    """ Spoiler tree node class. """

    canonical_tag_name = 'spoiler'
    alias_tag_names = ('hide', )

    make_paragraphs_here = True

    # CSS class name for the spoiler ``div`` element
    css_class_name = 'spoiler'

    # HTML template for rendering
    html_render_template = '<div class="{class_name}">{inner_html}</div>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(class_name=self.css_class_name, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        lines = ['!!! SPOILER !!!']
        for line in inner_text.splitlines():
            lines.append('! ' + line)
        lines.append('!!!')
        lines.append('')
        return '\n'.join(lines)
