"""
SkCode internal tag definitions code.
"""

from .base import TagOptions

from html import escape as escape_html
from html import unescape as unescape_html_entities


class RootTagOptions(TagOptions):
    """ Root tag options container class. """

    make_paragraphs_here = True

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Return the inner HTML as-is.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Return the inner text as-is.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode. Return the inner SkCode as-is.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        return inner_skcode


class TextTagOptions(TagOptions):
    """ Text tag options container class. """

    inline = True
    close_inlines = False

    replace_smileys = True
    replace_links = True
    replace_cosmetic = True

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Un-escape the node content before escaping it again and return it.
        This allow HTML special char in the text without causing trouble later (retro-compatibility with BBcode).
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        # FIXME Smileys and cosmetics here?
        return content

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Un-escape the node content before returning it.
        Not safe at all if used for HTML display! Use "render_html" for that.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        # FIXME Cosmetics here?
        return content

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content


class ErroneousTextTagOptions(TextTagOptions):
    """ Erroneous text tag options container class. """

    replace_smileys = False
    replace_links = False
    replace_cosmetic = False

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Get the output of the standard TextTagOptions but wrap the output
        in a big bold red text style span.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        content = super(ErroneousTextTagOptions, self).render_html(tree_node, inner_html)
        return '<span style="font-weight: bold; color: red;">%s</span>' % content


class NewlineTagOptions(TagOptions):
    """ Newline tag options container class. """

    inline = True
    close_inlines = False

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Return an ASCII newline (not an HTML line break).
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '\n'

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text. Return an ASCII newline.
        Not safe at all if used for HTML display! Use "render_html" for that.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return '\n'

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode. Return an ASCII newline.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        return '\n'


class HardNewlineTagOptions(NewlineTagOptions):
    """ Newline (hard line break variant) tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Return an HTML line break (not an ASCII newline).
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<br>\n'
