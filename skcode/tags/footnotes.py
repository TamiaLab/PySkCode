"""
SkCode footnotes tag definitions code.
"""

from gettext import gettext as _

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
    footnote_id_html_format = 'footnote-{}'

    # Footnote ID format for HTML rendering (back ref to declaration)
    footnote_id_html_format_backref = 'footnote-backref-{}'

    # Cached footnote counter attribute name (for this node)
    cached_footnote_counter_attr_name = '_cached_footnote_counter'

    # Last footnote counter attribute name (for the root node)
    last_footnote_counter_attr_name = '_last_footnote_counter'

    # Format string for the footnote counter
    footnote_counter_format = 'footnote-{}'

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
            return self.footnote_counter_format.format(getattr(self, self.cached_footnote_counter_attr_name))

        # Get the current counter value
        counter = getattr(self.root_tree_node, self.last_footnote_counter_attr_name, 0)

        # Increment and store the counter
        counter += 1
        setattr(self.root_tree_node, self.last_footnote_counter_attr_name, counter)

        # Store the ID in the node cache to avoid multiple ID generation
        setattr(self, self.cached_footnote_counter_attr_name, counter)

        # Return the ID for this footnote
        return self.footnote_counter_format.format(counter)

    def get_footnote_id(self):
        """
        Get the ID of this footnote.
        The ID can be set by setting the ``footnote_id_attr_name`` attribute of the tag or simply
        by setting the tag name attribute. If not set at all, an auto-generated ID will be used.
        The lookup order is: tag name (first), ``footnote_id_attr_name``, the auto generated ID.
        :return: The ID of this footnote.
        """
        footnote_id = self.get_attribute_value('', self.footnote_id_attr_name)
        if not footnote_id:
            footnote_id = self.get_footnote_id_from_counter()
        return slugify(footnote_id)

    def get_footnote_ref_id(self, footnote_id):
        """
        Get the footnote reference ID (HTML escaped).
        :param footnote_id: The raw footnote ID.
        :return: The footnote reference ID.
        """
        return escape_html(self.footnote_id_html_format.format(footnote_id))

    def get_footnote_backref_id(self, footnote_id):
        """
        Get the footnote back-reference ID (HTML escaped).
        :param footnote_id: The raw footnote ID.
        :return: The footnote back-reference ID.
        """
        return escape_html(self.footnote_id_html_format_backref.format(footnote_id))

    def pre_process_node(self):
        """
        Callback function for pre-processing the given node. Allow registration of IDs, references, etc.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        """
        footnote_id = self.get_footnote_id()
        if footnote_id in self.root_tree_node.known_ids:
            self.error_message = _('ID already used previously')
        else:
            self.root_tree_node.known_ids.add(footnote_id)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        footnote_id = self.get_footnote_id()
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
        footnote_id = self.get_footnote_id()
        return self.text_render_template.format(footnote_id=footnote_id)


class FootnoteReferenceTreeNode(TreeNode):
    """ Footnote reference tree node class. """

    inline = True
    close_inlines = False
    parse_embedded = False

    canonical_tag_name = 'fnref'
    alias_tag_names = ()

    # Footnote ID format for HTML rendering
    footnote_id_html_format = 'footnote-{}'

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
        return escape_html(self.footnote_id_html_format.format(footnote_id))

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(FootnoteReferenceTreeNode, self).sanitize_node(breadcrumb)
        footnote_id = self.get_footnote_id()
        if not footnote_id:
            self.error_message = _('Missing footnote ID')
        elif footnote_id not in self.root_tree_node.known_ids:
            self.error_message = _('Unknown footnote ID')

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
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
        footnote_id = self.get_footnote_id()
        return self.text_render_template.format(footnote_id=footnote_id) if footnote_id else inner_text
