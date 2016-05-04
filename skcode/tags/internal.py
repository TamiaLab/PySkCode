"""
SkCode internal tag definitions code.
"""

from .base import TagOptions

from ..utility.smileys import do_smileys_replacement
from ..utility.cosmetics import do_cosmetics_replacement

from html import escape as escape_html
from html import unescape as unescape_html_entities


class RootTagOptions(TagOptions):
    """ Root tag options container class. """

    canonical_tag_name = '_root'
    alias_tag_names = ()

    make_paragraphs_here = True

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text

    def render_skcode(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        return inner_skcode


class TextTagOptions(TagOptions):
    """ Text tag options container class. """

    inline = True
    close_inlines = False

    canonical_tag_name = '_text'
    alias_tag_names = ()

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = escape_html(content)
        content = self.do_custom_html_processing(tree_node.root_tree_node, content)
        return content

    def do_custom_html_processing(self, root_tree_node, input_text):
        """
        Do some custom HTML processing for cosmetics and smiley replacement.
        :param root_tree_node: The root tree node instance.
        :param input_text: Input text.
        :return: Input text with smileys and cosmetics replaced.
        """
        output_text = do_smileys_replacement(root_tree_node, input_text)
        output_text = do_cosmetics_replacement(root_tree_node, output_text)
        return output_text

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        content = self.do_custom_text_processing(tree_node.root_tree_node, content)
        return content

    def do_custom_text_processing(self, root_tree_node, input_text):
        """
        Do some custom text processing for cosmetics replacement.
        :param root_tree_node: The root tree node instance.
        :param input_text: Input text.
        :return: Input text with cosmetics replaced.
        """
        output_text = do_cosmetics_replacement(root_tree_node, input_text)
        return output_text

    def render_skcode(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        content = tree_node.content
        content = unescape_html_entities(content)
        return content


class ErroneousTextTagOptions(TextTagOptions):
    """ Erroneous text tag options container class. """

    canonical_tag_name = '_error'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<span style="font-weight: bold; color: red;">{}</span>'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        content = super(ErroneousTextTagOptions, self).render_html(tree_node, inner_html, **kwargs)
        return self.html_render_template.format(content)

    def do_custom_html_processing(self, root_tree_node, input_text):
        """
        Do nothing.
        :param root_tree_node: The root tree node instance.
        :param input_text: Input text.
        :return: Input text as-is.
        """
        return input_text

    def do_custom_text_processing(self, root_tree_node, input_text):
        """
        Do nothing.
        :param root_tree_node: The root tree node instance.
        :param input_text: Input text.
        :return: Input text as-is.
        """
        return input_text


class NewlineTagOptions(TagOptions):
    """ Newline tag options container class. """

    inline = True
    close_inlines = False

    canonical_tag_name = '_newline'
    alias_tag_names = ()

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '\n'

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return ' '

    def render_skcode(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        return '\n'


class HardNewlineTagOptions(NewlineTagOptions):
    """ Newline (hard line break variant) tag options container class. """

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<br>\n'

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '\n'

    def render_skcode(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        return '\n'
