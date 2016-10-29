"""
SkCode links tag definitions code.
"""

from gettext import gettext as _

from html import escape as escape_html
from html import unescape as unescape_html_entities

from ..etree import TreeNode
from ..tools import sanitize_url, slugify
from ..utility.relative_urls import get_relative_url_base


class UrlLinkTreeNode(TreeNode):
    """ URL link tree node class. """

    canonical_tag_name = 'url'
    alias_tag_names = ('link', )

    inline = True
    close_inlines = False

    # Special attribute name for the manual "nofollow" flag
    nofollow_attr_name = 'nofollow'

    # Title attribute name
    title_attr_name = 'title'

    # HTML template for rendering
    html_render_template = '<a href="{src_link}"{extra_args}>{inner_html}</a>'

    def is_url_inside_tag_content(self):
        """
        Return ``True`` if the target URL is in the tag content (not in attributes).
        """
        return self.name not in self.attrs

    def get_nofollow_flag(self):
        """
        Return ``True`` if the "nofollow" flag is set.
        """
        return self.nofollow_attr_name in self.attrs

    def get_target_link(self):
        """
        Return the target link URL.
        """
        if self.is_url_inside_tag_content():
            target_url = self.get_raw_content().strip()
        else:
            target_url = self.attrs.get(self.name, '')
        relative_url_base = get_relative_url_base(self.root_tree_node)
        return sanitize_url(target_url, absolute_base_url=relative_url_base)

    def get_title_link(self):
        """
        Return the title of this link, or an empty string.
        """
        link_title = self.attrs.get(self.title_attr_name, '')
        return unescape_html_entities(link_title)

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(UrlLinkTreeNode, self).sanitize_node(breadcrumb)
        if not self.get_target_link():
            self.error_message = _('Missing or erroneous target URL')

    def render_html(self, inner_html, force_rel_nofollow=True, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param force_rel_nofollow: If set to ``True``, all links in the rendered HTML will have the attribute
        "rel=nofollow" to avoid search engines to scrawl them (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Handle force_rel_nofollow
        extra_attrs = ' rel="nofollow"' if force_rel_nofollow or self.get_nofollow_flag() else ''

        # Add title if specified
        link_title = self.get_title_link()
        if link_title:
            extra_attrs += ' title="{}"'.format(escape_html(link_title))

        # Get the target URL
        target_url = self.get_target_link()

        # Render the link
        if not target_url:
            return inner_html
        if self.is_url_inside_tag_content():
            inner_html = target_url
        return self.html_render_template.format(src_link=target_url,
                                                extra_args=extra_attrs,
                                                inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the target URL
        target_url = self.get_target_link()

        # Render the link
        if not target_url:
            return inner_text
        if self.is_url_inside_tag_content():
            return target_url
        else:
            return '{} ({})'.format(inner_text, target_url)


class EmailLinkTreeNode(TreeNode):
    """ Email link tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'email'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<a href="mailto:{email_address}"{extra_args}>{inner_html}</a>'

    def is_email_inside_tag_content(self):
        """
        Return ``True`` if the target email address is in the tag content (not in attributes).
        """
        return self.name not in self.attrs

    def get_email_address(self):
        """
        Return the target email address.
        """
        if self.is_email_inside_tag_content():
            email_address = self.get_raw_content().strip()
        else:
            email_address = self.attrs.get(self.name, '')
        return sanitize_url(email_address,
                            default_scheme='mailto',
                            allowed_schemes=('mailto', ),
                            force_remove_scheme=True,
                            fix_non_local_urls=False)

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(EmailLinkTreeNode, self).sanitize_node(breadcrumb)
        if not self.get_email_address():
            self.error_message = _('Missing or erroneous target email address')

    def render_html(self, inner_html, force_rel_nofollow=True, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param force_rel_nofollow: If set to ``True``, all links in the rendered HTML will have the attribute
        "rel=nofollow" to avoid search engines to scrawl them (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the email address
        email_address = self.get_email_address()

        # Handle nofollow
        extra_html = ' rel="nofollow"' if force_rel_nofollow else ''

        # Render the email link
        if not email_address:
            return inner_html
        if self.is_email_inside_tag_content():
            inner_html = email_address
        return self.html_render_template.format(email_address=email_address,
                                                extra_args=extra_html,
                                                inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the email address
        email_address = self.get_email_address()

        # Render the email link
        if not email_address:
            return inner_text
        if self.is_email_inside_tag_content():
            return '<{}>'.format(email_address)
        else:
            return '{} (<{}>)'.format(inner_text, email_address)


class AnchorTreeNode(TreeNode):
    """ Anchor tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'anchor'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<a id="{anchor_id}"></a>'

    def get_anchor_id(self):
        """
        Get the ID of this anchor from the content of the node, or an empty string.
        """
        return slugify(self.get_raw_content())

    def pre_process_node(self):
        """
        Callback function for pre-processing the given node. Allow registration of IDs, references, etc.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        """
        anchor_id = self.get_anchor_id()
        if not anchor_id:
            self.error_message = _('Missing anchor ID')
        elif anchor_id in self.root_tree_node.known_ids:
            self.error_message = _('ID already used previously')
        else:
            self.root_tree_node.known_ids.add(anchor_id)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        anchor_id = self.get_anchor_id()
        return self.html_render_template.format(anchor_id=anchor_id) if anchor_id else inner_html

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        anchor_id = self.get_anchor_id()
        return '[#{}]'.format(anchor_id) if anchor_id else inner_text


class GoToAnchorTreeNode(TreeNode):
    """ "Go to anchor" tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'goto'
    alias_tag_names = ()

    # Anchor ID attribute name
    anchor_id_attr_name = 'id'

    # HTML template for rendering
    html_render_template = '<a href="#{anchor_id}">{inner_html}</a>'

    def get_anchor_id(self):
        """
        Get the target anchor ID of this link.
        The target anchor ID can be set by setting the ``anchor_id_attr_name`` attribute
        of the tag or simply by setting the tag name attribute.
        The lookup order is: tag name (first), ``anchor_id_attr_name``.
        :return The target anchor ID of this link, or an empty string.
        """
        user_anchor_id = self.get_attribute_value('', self.anchor_id_attr_name)
        return slugify(user_anchor_id)

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(GoToAnchorTreeNode, self).sanitize_node(breadcrumb)
        anchor_id = self.get_anchor_id()
        if not anchor_id:
            self.error_message = _('Missing anchor ID')
        elif anchor_id not in self.root_tree_node.known_ids:
            self.error_message = _('Unknown anchor ID')

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        anchor_id = self.get_anchor_id()
        return self.html_render_template.format(anchor_id=anchor_id,
                                                inner_html=inner_html) if anchor_id else inner_html

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        anchor_id = self.get_anchor_id()
        return '{inner_text} (#{anchor_id})'.format(inner_text=inner_text,
                                                    anchor_id=anchor_id) if anchor_id else inner_text
