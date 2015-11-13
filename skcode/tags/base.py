"""
SkCode base tag class definitions code.
"""


class TagOptions(object):
    """ Tag options container base class. """

    # Set to True if a newline should automatically close this tag.
    # When enabling this option, be sure to enable same_tag_closes to
    # avoid problem with nested tags not closed by newline.
    newline_closes = False

    # Set to True if another opening tag of the same type should
    # automatically close this tag.
    same_tag_closes = False
    
    # Set to True if this tag does not have a closing tag.
    # When this option is enabled, the self closing tag format is
    # allowed for the given tag along with the open tag format.
    standalone = False

    # Set to True if children tags should be parsed inside this tag
    # Set this to False for DATA/CODE blocks.
    parse_embedded = True

    # Set to True if this tag should swallow the first trailing newline.
    swallow_trailing_newline = False

    # Set to True if this tag is an inline tag, False for block tag.
    # If set this tag will be merging into paragraphs by the "make_paragraphs" utility.
    inline = False
    
    # Set to True if this tag should close any unclosed inline tag.
    close_inlines = True

    # ----- Utility options

    # Set to True if inline children node of this tag should be merged into paragraphs.
    make_paragraphs_here = False

    # ----- Utilities options

    # Set to True if smiley should be replaced inside this tag.
    # replace_smileys = False
    
    # Set to True if URLs should be replaced with link markup inside this tag.
    # replace_links = False
    
    # Set to True if cosmetic replacements (elipses, dashes, etc.) should be performed inside this tag.
    # replace_cosmetic = False

    def __init__(self, **kwargs):
        """ Set options according to kwargs. """
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def sanitize_node(self, tree_node,
                      erroneous_text_node_opts,
                      drop_erroneous=False):
        """
        Callback function for sanitizing and cleaning-up the given node.
        This function must validate it's own state and direct children type.
        This function is called in a down-to-top visit order (depth-first algorithm), starting from the last
        node of each branch and going up to the root node. This allow unwrapping of the current node
        in the parent node children list because the parent children list is checked AFTER all his children.
        In worst case scenario, an erroneous node can be unwrap up to the root node level.
        :param tree_node: The tree node to be sanitized.
        :param erroneous_text_node_opts: Erroneous text node options for unwrapping.
        :param drop_erroneous: If set, erroneous nodes (including this one) should be drop, not unwrapped.
        """
        # TODO implement default behavior
        # Default policy:
        # - inline accept only other inline
        # - allowed_parent_type option
        # - allow_same_type_nested option
        # - add tag_categories
        # - whitelist category
        # - blacklist category
        pass

    def postprocess_node(self, tree_node, root_tree_node):
        """
        Callback function for post-processing the given node.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        :param root_tree_node: The root tree node instance, can be used to store information at the document level.
        :param tree_node: The tree node being post processed.
        :return A bool True to disallow post processing of children nodes, a bool False (default implementation)
        to allow post processing of children nodes.
        """
        return False

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        raise NotImplementedError('render_html() need to be implemented in subclass.')

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        raise NotImplementedError('render_text() need to be implemented in subclass.')

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        raise NotImplementedError('render_skcode() need to be implemented in subclass.')


class WrappingTagOptions(TagOptions):
    """ Wrapping (block) tag options container class. """

    def __init__(self, wrapping_format, **kwargs):
        """
        Init class with the given wrapping format (use %s for content placeholder).
        :param wrapping_format: The format string to be used for wrapping the content of this node.
        """
        super(WrappingTagOptions, self).__init__(**kwargs)
        self.wrapping_format = wrapping_format

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML. Wrap the inner HTML code using the wrapping format.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return self.wrapping_format % inner_html

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
        Callback function for rendering SkCode. Wrap the inner SkCode with the node name tag, without arguments.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class InlineWrappingTagOptions(WrappingTagOptions):
    """ Wrapping (inline) tag options container class. """

    inline = True
    close_inlines = False
