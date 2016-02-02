"""
SkCode base tag class definitions code.
"""

from ..builder import build_tag_str


class TagOptions(object):
    """
    Tag options container base class.
    This class is used along with the ``TreeNode`` class in a delegation-like pattern for dynamic node typing.
    This base class define a common API for all nodes, which allow parsing, sanitizing, post-processing, and rendering
    of the node this class is attached to.

    This weird looking dynamic-typing pattern is used instead of a classic subclassing pattern to allow dynamic
    modifications of the node options. Only the option class define the behavior of the node.
    """

    # Set to ``True`` if a newline should automatically close this tag.
    # When enabling this option, be sure to enable ``same_tag_closes`` to
    # avoid problem with nested tags not closed by newline.
    newline_closes = False

    # Set to ``True`` if another opening tag of the same type should
    # automatically close this tag.
    same_tag_closes = False

    # Set to ``True`` if this tag does not have a closing tag.
    # When this option is enabled, the self closing tag format is
    # allowed for the given tag along with the open tag format.
    standalone = False

    # Set to ``True`` if children tags should be parsed inside this tag
    # Setting this to ``False`` will make the tag act like a DATA/CODE tag.
    parse_embedded = True

    # Set to ``True`` if this tag should swallow the first trailing newline.
    swallow_trailing_newline = False

    # Set to ``True`` if this tag is an inline tag, or to ``False`` for a block tag.
    # If set, this tag will be merging into paragraphs by the ``make_paragraphs`` utility.
    inline = False

    # Set to ``True`` if this tag should close any unclosed inline tag.
    close_inlines = True

    # ----- Utility options

    # Set to ``True`` if any inline children nodes of this tag should be merged into paragraphs.
    make_paragraphs_here = False

    def __init__(self, **kwargs):
        """
        Override defaults options according to kwargs.
        :param kwargs: a dictionary ``{key: value}`` of all options to be override.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def sanitize_node(self, tree_node, breadcrumb, erroneous_text_node_opts, drop_erroneous=False):
        """
        Callback function for sanitizing and cleaning-up the given node.
        This function must validate it's own state and direct children type / ordering.
        This function is called in a down-to-top visit order (depth-first algorithm), starting from the last
        node of each branch and going up to the root node. This allow unwrapping of the current node
        in the parent node children list because the parent children list is checked AFTER all his children.
        In worst case scenario, an erroneous node can be unwrap up to the root node level.
        :param tree_node: The tree node to be sanitized.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        :param erroneous_text_node_opts: The options class to be used for all erroneous text.
        :param drop_erroneous: If set to ``True``, any erroneous nodes (including this one) should be drop
        instead of being unwrapped.
        """
        # TODO implement default behavior
        # Default policy:
        # - inline accept only other inline
        # - allowed_parent_type option
        # - allow_same_type_nested option
        # - add tag_categories
        # - white list category
        # - blacklist category
        pass

    def post_process_node(self, tree_node):
        """
        Callback function for post-processing the given node.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        :param tree_node: The tree node being post processed.
        :return Returning a bool ``False`` disallow post processing of children nodes. Returning a bool ``True``
        allow post processing of children nodes. Default return value is ``True``.
        """
        return True

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        raise NotImplementedError('render_html() need to be implemented in subclass.')

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        raise NotImplementedError('render_text() need to be implemented in subclass.')

    def render_skcode(self, tree_node, inner_skcode,
                      opening_tag_ch='[', closing_tag_ch=']',
                      allow_tagvalue_attr=True, **kwargs):
        """
        Callback function for rendering SkCode.
        The default implementation call the ``get_skcode_tag_name`` method to get the tag name,
        the ``get_skcode_attributes`` method to get any attributes, the ``get_skcode_non_ignored_empty_attributes``
        method to get any non-ignored-if-empty attribute names and the ``get_skcode_inner_content`` method to get the
        inner content of the tag.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param opening_tag_ch: The opening tag char (must be one char long, default '[').
        :param closing_tag_ch: The closing tag char (must be one char long, default ']').
        :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut
        (default ``True``).
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        tag_name = self.get_skcode_tag_name(tree_node, inner_skcode, **kwargs)
        attrs, tag_value_attr_name = self.get_skcode_attributes(tree_node, inner_skcode, **kwargs)
        content = self.get_skcode_inner_content(tree_node, inner_skcode, **kwargs)
        non_ignored_empty_attrs = self.get_skcode_non_ignored_empty_attributes(tree_node, inner_skcode, **kwargs)
        return build_tag_str(tag_name, attrs=attrs, content=content,
                             opening_tag_ch=opening_tag_ch, closing_tag_ch=closing_tag_ch,
                             allow_tagvalue_attr=allow_tagvalue_attr, standalone=self.standalone,
                             tagvalue_attr_name=tag_value_attr_name, non_ignored_empty_attrs=non_ignored_empty_attrs)

    def get_skcode_tag_name(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving the tag name of this node for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The tag name of this node for SkCode rendering.
        Default implementation return the ``tree_node.name`` value.
        """
        return tree_node.name

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        Default implementation return ``{}, None``.
        """
        return {}, None

    def get_skcode_non_ignored_empty_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attribute names not to be ignored when empty.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A tuple of all attribute names not to be ignored when empty.
        Default implementation return an empty tuple.
        """
        return ()

    def get_skcode_inner_content(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving the inner content of this node for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The inner content for SkCode rendering.
        Default implementation return the ``inner_skcode`` value.
        """
        return inner_skcode


class WrappingTagOptions(TagOptions):
    """
    Wrapping (block) tag options container class.
    Simple subclass of ``TagOptions`` which wrap the HTML output of children nodes with a format string.
    """

    def __init__(self, wrapping_format, **kwargs):
        """
        Initialize the wrapper with the given wrapping format (use ``%s`` for the content placeholder).
        :param wrapping_format: The format string to be used for wrapping the HTML content of this node.
        """
        assert wrapping_format, "The wrapping format string is mandatory."
        assert '%s' in wrapping_format, "The wrapping format string must contain %s for inner content place holding."
        super(WrappingTagOptions, self).__init__(**kwargs)
        self.wrapping_format = wrapping_format

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.wrapping_format % inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class InlineWrappingTagOptions(WrappingTagOptions):
    """
    Wrapping (inline) tag options container class.
    Inline variant of the ``WrappingTagOptions`` options class.
    """

    inline = True
    close_inlines = False
