"""
SkCode elements tree code.
"""

from html import escape as escape_html


class TreeNode(object):
    """
    Tree node container class.

    A tree node is made of:
    - a root node instance (used to store document-level information),
    - a parent node instance (or ``None`` for root node),
    - a name (``None`` for internal-use only nodes),
    - an attributes dictionary,
    - a raw content string (for raw text nodes),
    - a list child nodes,
    - the opening and closing tag source strings (for error displaying).
    """

    # ----- Node naming options

    # Canonical tag name (string, mandatory)
    canonical_tag_name = None

    # Alias tag names (tuple of strings, can be empty)
    alias_tag_names = ()

    # ----- Node parsing options

    # Set to ``True`` if a newline should automatically close this tag.
    # When enabling this option, be sure to enable ``same_tag_closes`` to
    # avoid problem with nested tags not closed by newline.
    newline_closes = False

    # Set to ``True`` if another opening tag of the same type should
    # automatically close this tag.
    # When enabling this option, be sure to enable ``weak_parent_close`` to
    # avoid problem with unclosed tag taking down the closing tag of his parent.
    same_tag_closes = False

    # Set to ``True`` if the parent closing tag should
    # automatically close this tag (if not already closed).
    weak_parent_close = False

    # Set to ``True`` if this tag does not have a closing tag.
    # When this option is enabled, the self closing tag format is
    # allowed for the given tag along with the open tag format.
    standalone = False

    # Set to ``True`` if children tags should be parsed inside this tag
    # Setting this to ``False`` will make the tag act like a DATA/CODE tag.
    parse_embedded = True

    # Set to ``True`` if this tag is an inline tag, or to ``False`` for a block tag.
    # If set, this tag will be merging into paragraphs by the ``make_paragraphs`` utility.
    inline = False

    # Set to ``True`` if this tag should close any unclosed inline tag.
    close_inlines = True

    # ----- Utilities options

    # Set to ``True`` if any inline children nodes of this tag should be merged into paragraphs.
    make_paragraphs_here = False

    # ----- Internal use variables

    is_root = False

    def __init__(self,
                 root_tree_node, parent, name,
                 attrs=None, content='', children=None,
                 source_open_tag='', source_close_tag='',
                 error_message=''):
        """
        Create a new tree node instance.
        :param root_tree_node: The root tree node instance (mandatory). Use to store document-level data.
        N.B. Child nodes root tree node instance will be reset recursively to this root tree node instance to
        allow merging of two different tree.
        :param parent: The node parent instance (mandatory). Set to ``None`` for the root node.
        N.B. Use the ``RootTreeNode`` class for the root tree node.
        :param name: The node name (mandatory for non-internal use nodes).
        :param attrs: the node attributes dictionary (default to an empty dictionary).
        :param content: The node raw content (default to an empty string).
        :param children: The node children list (default to an empty list).
        N.B. Child nodes parent instance will be reset to this node instance.
        :param source_open_tag: The source text for the opening tag of this node (default to an empty string).
        :param source_close_tag: The source text for the closing tag of this node (default to an empty string).
        :param error_message: The error message, if any error need to be reported. Default to an empty string.
        """
        assert root_tree_node, "The root tree node instance is mandatory."
        if not self.is_root:
            assert parent, "The parent node instance is mandatory for non-root nodes."

        # Store value as attributes
        self.root_tree_node = root_tree_node
        self.parent = parent
        self.name = name
        self.attrs = attrs or {}
        self.content = content
        self.children = children or []
        self.source_open_tag = source_open_tag
        self.source_close_tag = source_close_tag
        self.error_message = error_message

        # Rebase children parent and root tree node
        for child in self.children:
            child.parent = self
        self.reset_root_tree_node(root_tree_node)

    def reset_root_tree_node(self, new_root_tree_node):
        """
        Reset the root tree node instance of this node and all child nodes recursively.
        :param new_root_tree_node: The new root tree node instance
        """
        self.root_tree_node = new_root_tree_node
        for child in self.children:
            child.reset_root_tree_node(new_root_tree_node)

    def new_child(self, name, node_cls, append=True, **kwargs):
        """
        Create a new child node from the given arguments.
        Auto set the parent attribute of the newly created child node to this node instance and append the child
        node to the children list of this node if ``append=True``.
        :param name: The tag name of the new tre node.
        :param node_cls: The class to be used to create the new tree node.
        :param append: If set to ``True``, the newly created child will be added to the node children list.
        :param kwargs: Keyword arguments for the tree node class constructor.
        :return: The newly created node instance.
        """
        new_child_node = node_cls(self.root_tree_node, self, name, **kwargs)
        if append:
            self.children.append(new_child_node)
        return new_child_node

    def get_raw_content(self, recursive=True):
        """
        Return the raw content of this node and of children nodes if ``recursive=True``.
        :param recursive: Set to ``True`` to include any child nodes content (default ``True``).
        :return The raw content of this node and of children nodes, if requested.
        """
        content = self.content
        if recursive:
            for child_node in self.children:
                content += child_node.get_raw_content()
        return content

    def search_in_tree(self, node_cls):
        """
        Walk down the tree and yield any node matching the given class.
        :param node_cls: The class type to search for (or a tuple of class types).
        """

        # Check the current tree node first
        if isinstance(self, node_cls):
            yield self

        # Check all children nodes
        for child in self.children:
            yield from child.search_in_tree(node_cls)

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        This function must validate it's own state and direct children type / ordering.
        This function is called in a down-to-top visit order (depth-first algorithm), starting from the last
        node of each branch and going up to the root node. This allow unwrapping of the current node
        in the parent node children list because the parent children list is checked AFTER all his children.
        In worst case scenario, an erroneous node can be unwrap up to the root node level.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
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

    def post_process_node(self):
        """
        Callback function for post-processing the given node.
        This function is called in a top-to-down visit order, starting from the root node and going down to each
        leaf node.
        :return Returning a bool ``False`` disallow post processing of children nodes. Returning a bool ``True``
        allow post processing of children nodes. Default return value is ``True``.
        """
        return True

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        raise NotImplementedError('render_html() need to be implemented in subclass')

    def render_error_html(self, inner_html, html_error_template, **kwargs):
        """
        Callback function for rendering HTML when the node is erroneous.
        :param inner_html: The inner HTML of this tree node.
        :param html_error_template: The HTML template for rendering the erroneous parts of the output.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        output_html = []
        if self.source_open_tag:
            output_html.append(html_error_template.format(error_message=self.error_message,
                                                          source=self.source_open_tag))

        output_html.append(inner_html or escape_html(self.get_raw_content()))

        if self.source_close_tag:
            output_html.append(html_error_template.format(error_message=self.error_message,
                                                          source=self.source_close_tag))

        return '\n'.join(output_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        raise NotImplementedError('render_text() need to be implemented in subclass')


class RootTreeNode(TreeNode):
    """
    Root tree node container class.
    Subclass of the ``TreeNode`` class which set ``parent=None``.
    This class is special, unwrap and delete operations are not supported.
    Attributes dictionary is not used for rendering, but instead, as a document-level data container.
    """

    make_paragraphs_here = True

    is_root = True

    def __init__(self, attrs=None, children=None):
        """
        Create a new root tree node.
        :param attrs: The root node attributes dictionary (default to an empty dictionary).
        :param children: The root node children list (default to an empty list).
        """
        super(RootTreeNode, self).__init__(self, None, None, attrs=attrs, children=children)

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return inner_html

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


def debug_print_ast(tree_node, indent_level=0, expected_parent=None, print_fnct=print):
    """
    Print the given AST tree to stdout for debugging purposes.
    :param tree_node: The tree node to be printed to stdout.
    :param indent_level: The current indentation level (default to 0).
    :param expected_parent: The excepted parent instance (for fast error detection during debug).
    :param print_fnct: Function to use for printing to stdout (default to ``print``).
    """

    # Print info about the current tree node
    print_fnct('{indent}{classname}(name="{name}", attrs={attrs}, '
               'content={content}, len(children)={nchild})'.format(
                    indent='    ' * indent_level,
                    classname=tree_node.__class__.__name__,
                    name=tree_node.name,
                    attrs=tree_node.attrs,
                    content=repr(tree_node.content),
                    nchild=len(tree_node.children)),
               '!! Parent mismatch !!' if tree_node.parent != expected_parent else '')

    # Process all children
    for child_node in tree_node.children:
        debug_print_ast(child_node, indent_level + 1, tree_node, print_fnct)
