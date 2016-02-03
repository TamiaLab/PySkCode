"""
SkCode links tag definitions code.
"""

from .base import TagOptions
from ..tools import (sanitize_url,
                     slugify)


class UrlLinkTagOptions(TagOptions):
    """ URL link tag options container class. """

    inline = True
    close_inlines = False

    def is_url_inside_tag_content(self, tree_node):
        """
        Return ``True`` if the target URL is in the tag content (not in attributes).
        :param tree_node: The current tree node instance.
        :return ``True`` if the target URL is in the tag content, not in attributes.
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
        # TODO Add relative-absolute URL conversion
        return sanitize_url(target_url)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param force_rel_nofollow: If set to ``True``, all links in the rendered HTML will have the atribute
        "rel=nofollow" to avoid search engines to scrawl them (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Handle force_rel_nofollow
        extra_attrs = ' rel="nofollow"' if force_rel_nofollow else ''

        # Get the target URL
        target_url = self.get_target_link(tree_node)

        # Render the link
        if target_url:
            return '<a href="%s"%s>%s</a>' % (target_url, extra_attrs,
                                              target_url if self.is_url_inside_tag_content(tree_node) else inner_html)
        else:
            return inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
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

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        if self.is_url_inside_tag_content(tree_node):
            return {}, None
        else:
            # Get the target URL
            target_url = self.get_target_link(tree_node)
            return {
                       tree_node.name: target_url
                   }, tree_node.name


class EmailLinkTagOptions(TagOptions):
    """ Email link tag options container class. """

    inline = True
    close_inlines = False

    def is_email_inside_tag_content(self, tree_node):
        """
        Return ``True`` if the target email address is in the tag content (not in attributes).
        :param tree_node: The current tree node instance.
        :return ``True`` if the target email address is in the tag content, not in attributes.
        """
        return tree_node.name not in tree_node.attrs

    def get_email_address(self, tree_node):
        """
        Return the target email address.
        :param tree_node: The current tree node instance.
        :return The target email address.
        """
        if self.is_email_inside_tag_content(tree_node):
            email_address = tree_node.get_raw_content().strip()
        else:
            email_address = tree_node.attrs.get(tree_node.name, '')
        return sanitize_url(email_address,
                            default_scheme='mailto',
                            allowed_schemes=('mailto', ),
                            force_remove_scheme=True,
                            fix_non_local_urls=False)

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param force_rel_nofollow: If set to ``True``, all links in the rendered HTML will have the atribute
        "rel=nofollow" to avoid search engines to scrawl them (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the email address
        email_address = self.get_email_address(tree_node)

        # Handle nofollow
        extra_html = ' rel="nofollow"' if force_rel_nofollow else ''

        # Render the email link
        if email_address:
            return '<a href="mailto:%s"%s>%s</a>' % (
                email_address, extra_html,
                email_address if self.is_email_inside_tag_content(tree_node) else inner_html
            )
        else:
            return inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
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

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        if self.is_email_inside_tag_content(tree_node):
            return {}, None
        else:
            # Get the email address
            email_address = self.get_email_address(tree_node)
            return {
                       tree_node.name: email_address
                   }, tree_node.name


class AnchorTagOptions(TagOptions):
    """ Anchor tag options container class. """

    inline = True
    close_inlines = False

    def get_anchor_id(self, tree_node):
        """
        Get the ID of this anchor from the content of the node.
        :param tree_node: The current tree node instance.
        :return The ID of this anchor, or an empty string.
        """
        return slugify(tree_node.get_raw_content())

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return Rendered HTML of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)
        return '<a id="%s"></a>' % anchor_id if anchor_id else inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return Rendered text of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)
        return '[#%s]' % anchor_id if anchor_id else inner_text

    def get_skcode_inner_content(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for retrieving the inner content for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The inner content for SkCode rendering.
        """
        return self.get_anchor_id(tree_node) or inner_skcode


class GoToAnchorTagOptions(TagOptions):
    """ "Go to anchor" tag options container class. """

    inline = True
    close_inlines = False

    # Anchor ID attribute name
    anchor_id_attr_name = 'id'

    def get_anchor_id(self, tree_node):
        """
        Get the target anchor ID of this link.
        The target anchor ID can be set by setting the ``anchor_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``anchor_id_attr_name``.
        :param tree_node: The current tree node instance.
        :return The target anchor ID of this link, or an empty string.
        """
        user_anchor_id = tree_node.attrs.get(tree_node.name, '')
        if not user_anchor_id:
            user_anchor_id = tree_node.attrs.get(self.anchor_id_attr_name, '')
        return slugify(user_anchor_id)

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)
        return '<a href="#%s">%s</a>' % (anchor_id, inner_html) if anchor_id else inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)
        return '%s (#%s)' % (inner_text, anchor_id) if anchor_id else inner_text

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get the anchor ID
        anchor_id = self.get_anchor_id(tree_node)
        return {
                   self.anchor_id_attr_name: anchor_id
               }, self.anchor_id_attr_name
