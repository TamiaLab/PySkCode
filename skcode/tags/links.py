"""
SkCode links tag definitions code.
"""

from html import escape as escape_html

from .base import TagOptions
from ..tools import (escape_attrvalue,
                     sanitize_url,
                     slugify)


class UrlLinkTagOptions(TagOptions):
    """ URL link tag options container class. """

    inline = True
    close_inlines = False

    def is_url_inside_tag_content(self, tree_node):
        """
        Return True if the target URL is in the tag content (not in attributes).
        :param tree_node: The current tree node instance.
        :return True if the target URL is in the tag content, not in attributes.
        """
        return tree_node.name not in tree_node.attrs

    def get_target_link(self, tree_node):
        """
        Return the target link URL.
        :param tree_node: The current tree node instance.
        :return The target link URL.
        """
        if self.is_url_inside_tag_content(tree_node):
            target_url = tree_node.get_raw_content().strip()
        else:
            target_url = tree_node.attrs.get(tree_node.name, '')
        return sanitize_url(target_url)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Handle force_rel_nofollow
        if force_rel_nofollow:
            extra_attrs = ' rel="nofollow"'
        else:
            extra_attrs = ''

        # Get the target URL
        target_url = self.get_target_link(tree_node)

        # Render the link
        if target_url:
            if self.is_url_inside_tag_content(tree_node):
                return '<a href="%s"%s>%s</a>' % (target_url, extra_attrs, target_url)
            else:
                return '<a href="%s"%s>%s</a>' % (target_url, extra_attrs, inner_html)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the target URL
        target_url = self.get_target_link(tree_node)

        # Render the link
        if target_url:
            if self.is_url_inside_tag_content(tree_node):
                return '%s' % target_url
            else:
                return '%s (%s)' % (inner_text, target_url)
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the target URL
        target_url = self.get_target_link(tree_node)

        # Render the link
        if target_url:
            node_name = tree_node.name
            if self.is_url_inside_tag_content(tree_node):
                return '[%s]%s[/%s]' % (node_name, target_url, node_name)
            else:
                return '[%s=%s]%s[/%s]' % (node_name, escape_attrvalue(target_url), inner_skcode, node_name)
        else:
            return inner_skcode


class EmailLinkTagOptions(TagOptions):
    """ Email link tag options container class. """

    inline = True
    close_inlines = False

    def is_email_inside_tag_content(self, tree_node):
        """
        Return True if the target email address is in the tag content (not in attributes).
        :param tree_node: The current tree node instance.
        :return True if the target email address is in the tag content, not in attributes.
        """
        return tree_node.name not in tree_node.attrs

    def get_email_address(self, tree_node):
        """
         Return the target email address.
        :param tree_node: The current tree node instance.
        :return The target email address.
        """
        if self.is_email_inside_tag_content(tree_node):
            email_address = tree_node.get_raw_content()
        else:
            email_address = tree_node.attrs.get(tree_node.name, '')
        # TODO remove mailto: scheme and (better) made a function sanitize_email_address()
        return sanitize_url(email_address,
                            default_scheme='mailto',
                            allowed_schemes=('mailto', ),
                            force_remove_scheme=True)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the email address
        email_address = self.get_email_address(tree_node)

        # Handle nofollow
        if force_rel_nofollow:
            extra_html = ' rel="nofollow"'
        else:
            extra_html = ''

        # Render the email link
        if email_address:
            if self.is_email_inside_tag_content(tree_node):
                return '<a href="mailto:%s"%s>%s</a>' % (email_address, extra_html, email_address)
            else:
                return '<a href="mailto:%s"%s>%s</a>' % (email_address, extra_html, inner_html)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the email address
        email_address = self.get_email_address(tree_node)

        # Render the email link
        if email_address:
            if self.is_email_inside_tag_content(tree_node):
                return '<%s>' % email_address
            else:
                return '%s (<%s>)' % (inner_text, email_address)
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the email address
        email_address = self.get_email_address(tree_node)

        # Render the email link
        if email_address:
            node_name = tree_node.name
            if self.is_email_inside_tag_content(tree_node):
                return '[%s]%s[/%s]' % (node_name, email_address, node_name)
            else:
                return '[%s=%s]%s[/%s]' % (node_name, escape_attrvalue(email_address), inner_skcode, node_name)
        else:
            return inner_skcode


class AnchorTagOptions(TagOptions):
    """ Anchor tag options container class. """

    inline = True
    close_inlines = False

    def get_anchor_id(self, tree_node):
        """
        Get the ID of this anchor from the content of the node.
        :param tree_node: the current tree node instance.
        :return The ID of this anchor, or an empty string.
        """
        return slugify(tree_node.get_raw_content())

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            return '<a id="%s"></a>' % escape_html(anchor_id)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            return '[#%s]' % anchor_id
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            node_name = tree_node.name
            return '[%s]%s[/%s]' % (node_name, anchor_id, node_name)
        else:
            return inner_skcode


class GoToAnchorTagOptions(TagOptions):
    """ "Go to anchor" tag options container class. """

    inline = True
    close_inlines = False

    # Anchor ID attribute name
    anchor_id_attr_name = 'id'

    def get_anchor_id(self, tree_node):
        """
        Get the target anchor ID of this link.
        The target anchor ID can be set by setting the anchor_id_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), anchor_id_attr_name.
        :param tree_node: the current tree node instance.
        :return The target anchor ID of this link, or an empty string.
        """
        user_anchor_id = tree_node.attrs.get(tree_node.name, '')
        if not user_anchor_id:
            user_anchor_id = tree_node.attrs.get(self.anchor_id_attr_name, '')
        return slugify(user_anchor_id)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            return '<a href="#%s">%s</a>' % (escape_html(anchor_id), inner_html)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            return '%s (#%s)' % (inner_text, anchor_id)
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)

        # Render the anchor link
        if anchor_id:
            node_name = tree_node.name
            return '[%s=%s]%s[/%s]' % (node_name, escape_attrvalue(anchor_id), inner_skcode, node_name)
        else:
            return inner_skcode
