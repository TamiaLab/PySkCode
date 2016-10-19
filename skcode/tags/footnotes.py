"""
SkCode footnotes tag definitions code.
"""

from html import escape as escape_html

from ..etree import TreeNode
from ..tools import slugify


class FootnoteDeclarationTreeNode(TreeNode):
    """ Footnote declaration tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'footnote'
    alias_tag_names = ('fn', )

    # Footnote ID attribute name
    footnote_id_attr_name = 'id'

    # Footnote ID format for HTML rendering
    footnote_id_html_format = 'footnote-%s'

    # Footnote ID format for HTML rendering (back ref to declaration)
    footnote_id_html_format_backref = 'footnote-backref-%s'

    # Cached footnote counter attribute name (for this node)
    cached_footnote_counter_attr_name = '_cached_footnote_counter'

    # Last footnote counter attribute name (for the root node)
    last_footnote_counter_attr_name = '_last_footnote_counter'

    # HTML template for rendering
    html_render_template = '<a id="{backward_id}" href="#{forward_id}"><sup>[{footnote_id}]</sup></a>'

    # Text template for rendering
    text_render_template = '[^{footnote_id}]'

    def get_footnote_id_from_counter(self):
        """
        Get the footnote ID from the counter stored in the root tree node or in the tree node cache.
        :return: The footnote ID retrieved from the root tree node counter.
        """

        # Get the ID from the node cache if exists
        if hasattr(self, self.cached_footnote_counter_attr_name):
            return str(getattr(self, self.cached_footnote_counter_attr_name))

        # Get the current counter value
        counter = getattr(self.root_tree_node, self.last_footnote_counter_attr_name, 0)

        # Increment and store the counter
        counter += 1
        setattr(self.root_tree_node, self.last_footnote_counter_attr_name, counter)

        # Store the ID in the node cache to avoid multiple ID generation
        setattr(self, self.cached_footnote_counter_attr_name, counter)

        # Return the ID for this footnote
        return str(counter)

    def get_footnote_id(self, use_auto_generated_id=True):
        """
        Get the ID of this footnote.
        The ID can be set by setting the ``footnote_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute. If not set at all, an auto-generated ID will be used if
        ``use_auto_generated_id=True`` (default).
        The lookup order is: tag name (first), ``footnote_id_attr_name``, the auto generated ID.
        :param use_auto_generated_id: Set to ``True`` to use an auto-generated ID if no user ID is available
        (default ``True``).
        :return: The ID of this footnote.
        """
        footnote_id = self.attrs.get(self.name, '')
        if not footnote_id:
            footnote_id = self.attrs.get(self.footnote_id_attr_name, '')
        if not footnote_id and use_auto_generated_id:
            footnote_id = self.get_footnote_id_from_counter()
        return slugify(footnote_id)

    def get_footnote_ref_id(self, footnote_id):
        """
        Get the footnote reference ID (HTML escaped).
        :param footnote_id: The raw footnote ID.
        :return: The footnote reference ID.
        """
        return escape_html(self.footnote_id_html_format % footnote_id)

    def get_footnote_backref_id(self, footnote_id):
        """
        Get the footnote back-reference ID (HTML escaped).
        :param footnote_id: The raw footnote ID.
        :return: The footnote back-reference ID.
        """
        return escape_html(self.footnote_id_html_format_backref % footnote_id)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the footnote ID
        footnote_id = self.get_footnote_id()

        # Render the footnote
        return self.html_render_template.format(
            backward_id=self.get_footnote_backref_id(footnote_id),
            forward_id=self.get_footnote_ref_id(footnote_id),
            footnote_id=footnote_id
        )

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the footnote ID
        footnote_id = self.get_footnote_id()

        # Render the footnote
        return self.text_render_template.format(footnote_id=footnote_id)


class FootnoteReferenceTreeNode(TreeNode):
    """ Footnote reference tree node class. """

    inline = True
    close_inlines = False

    canonical_tag_name = 'fnref'
    alias_tag_names = ()

    # Footnote ID format for HTML rendering
    footnote_id_html_format = 'footnote-%s'

    # HTML template for rendering
    html_render_template = '<a href="#{forward_id}"><sup>[{footnote_id}]</sup></a>'

    # Text template for rendering
    text_render_template = '[^{footnote_id}]'

    def get_footnote_id(self):
        """
        Get the target ID of this footnote reference from the content of the node.

        :return: The target ID of this footnote reference.
        """
        return slugify(self.get_raw_content())

    def get_footnote_ref_id(self, footnote_id):
        """
        Get the footnote reference ID (HTML escaped).
        :param footnote_id: The raw footnote ID.
        :return: The footnote reference ID.
        """
        return escape_html(self.footnote_id_html_format % footnote_id)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the footnote ID
        footnote_id = self.get_footnote_id()
        return self.html_render_template.format(
            forward_id=self.get_footnote_ref_id(footnote_id),
            footnote_id=footnote_id) if footnote_id else inner_html

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the footnote ID
        footnote_id = self.get_footnote_id()
        return self.text_render_template.format(footnote_id=footnote_id) if footnote_id else inner_text
