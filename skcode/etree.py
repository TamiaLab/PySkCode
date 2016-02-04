"""
SkCode tree element code.
"""

# Reserved tag names
ROOT_NODE_NAME = '_root'
TEXT_NODE_NAME = '_text'
NEWLINE_NODE_NAME = '_newline'


class TreeNode(object):
    """
    Simple tree node container class.
    A tree node is made of:
    - a root node (document) instance,
    - a parent node instance (``None`` for root node),
    - a name,
    - an options class (delegation-like pattern, for dynamic node typing),
    - an attributes dictionary,
    - a raw content string (for text nodes),
    - a list child nodes,
    - an open and closing tag source string (for storing raw SkCode of the node tag).
    """

    is_root = False

    def __init__(self, root_tree_node, parent, name, opts, attrs=None, content='',
                 children=None, source_open_tag='', source_close_tag=''):
        """
        Create a new tree node instance.
        :param root_tree_node: The root tree node instance (mandatory). Use to store document-level data.
        N.B. Child nodes root tree node instance will be reset recursively to this root tree node instance to
        allow merging of two different tree.
        :param parent: The node parent instance (mandatory). Set to ``None`` for the root node.
        N.B. Use the ``RootTreeNode`` class for the root tree node.
        :param name: The node name (mandatory).
        :param opts: The node options class (mandatory).
        :param attrs: the node attributes dictionary (default to an empty dictionary).
        :param content: The node raw content (default to an empty string).
        :param children: The node children list (default to an empty list).
        N.B. Child nodes parent instance will be reset to this node instance.
        :param source_open_tag: The SkCode source text for the opening tag of this node (default to an empty string).
        :param source_close_tag: The SkCode source text for the closing tag of this node (default to an empty string).
        """
        assert root_tree_node, "The root tree node instance is mandatory."
        if not self.is_root:
            assert parent, "The parent node instance is mandatory for non-root nodes."
        assert name, "Node name must be specified."
        assert opts, "Node options must be specified."

        # Store value as attributes
        self.root_tree_node = root_tree_node
        self.parent = parent
        self.name = name
        self.opts = opts
        self.attrs = attrs or {}
        self.content = content
        self.children = children or []
        self.source_open_tag = source_open_tag
        self.source_close_tag = source_close_tag

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

    def new_child(self, *args, append=True, **kwargs):
        """
        Create a new child node from the given arguments.
        Auto set the parent attribute of the newly created child node to this node instance and append the child
        node to the children list of this node.
        :param args: Positional arguments for the ``TreeNode`` class constructor.
        :param append: If set to ``True``, the newly created child will be added to the node children list.
        :param kwargs: Keyword arguments for the ``TreeNode`` class constructor.
        :return: The newly created node instance.
        """
        new_child_node = TreeNode(self.root_tree_node, self, *args, **kwargs)
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

    def unwrap_as_erroneous(self, erroneous_text_node_opts):
        """
        Unwrap this node and dump his raw source code as erroneous text.
        :param erroneous_text_node_opts: Options to be used when creating the new erroneous text node.
        """
        assert self.parent, "Cannot unwrap a node without parent."
        assert erroneous_text_node_opts, "Erroneous text node options is mandatory."

        # Get the current node index in the parent children list
        my_parent = self.parent
        index_cur = my_parent.children.index(self)

        # Get all nodes before and after the current node
        nodes_before_cur = my_parent.children[:index_cur]
        nodes_after_cur = my_parent.children[index_cur + 1:]

        # Craft the new children list
        new_children = []
        new_children.extend(nodes_before_cur)

        # Add the opening tag source of this node
        if self.source_open_tag:
            new_children.append(TreeNode(self.root_tree_node, my_parent, TEXT_NODE_NAME, erroneous_text_node_opts,
                                         content=self.source_open_tag))

        # Rebase all children of this node
        for child_node in self.children:
            child_node.parent = my_parent
            new_children.append(child_node)

        # Add the closing tag source of this node
        if self.source_close_tag:
            new_children.append(TreeNode(self.root_tree_node, my_parent, TEXT_NODE_NAME, erroneous_text_node_opts,
                                         content=self.source_close_tag))

        # Finish the job
        new_children.extend(nodes_after_cur)
        my_parent.children = new_children
        self.children = []

    def delete_from_parent(self):
        """
        Remove this node from his parent children list.
        """
        assert self.parent, "Cannot delete a node without parent."

        # Commit suicide
        self.parent.children.remove(self)

    # TODO Found an user-friendly way to pass function calls to self.opts with first args=self
    # TODO Make the opts class provide attributes and members to the node to avoid avoid calling x.opts.y each time


class RootTreeNode(TreeNode):
    """
    Root tree node container class.
    Subclass of the ``TreeNode`` class which set ``parent=None`` and ``name=ROOT_NODE_NAME``.
    This class is S.P.E.C.I.A.L. Unwrap and delete operations are not supported.
    Attributes dictionary is not used for rendering, but instead, as a document-level data container.
    """

    is_root = True

    def __init__(self, opts, attrs=None, children=None):
        """
        Create a new root tree node.
        :param opts: The root node options class (mandatory).
        :param attrs: The root node attributes dictionary (default to an empty dictionary).
        :param children: The root node children list (default to an empty list).
        """
        super(RootTreeNode, self).__init__(self, None, ROOT_NODE_NAME, opts, attrs, children=children)

    def unwrap_as_erroneous(self, erroneous_text_node_opts):
        """
        This method is not implemented for the root tree node.
        Calling this method will only raise an error for bad-code debugging purposes.
        :param erroneous_text_node_opts: Not used.
        """
        raise NotImplementedError('Root tree node cannot be unwrapped.')

    def delete_from_parent(self):
        """
        This method is not implemented for the root tree node.
        Calling this method will only raise an error for bad-code debugging purposes
        """
        raise NotImplementedError('Root tree node cannot be deleted.')


def debug_print_ast(tree_node, ident_level=0, expected_parent=None, print_fnct=print):
    """
    Print the given AST tree to stdout for debugging purposes.
    :param tree_node: The tree node to be printed to stdout.
    :param ident_level: The current indentation level (default to 0).
    :param expected_parent: The excepted parent instance (for fast error detection during debug).
    :param print_fnct: Function to use for printing to stdout (default to ``print``).
    """

    # Print info about the current tree node
    print_fnct('%sTreeNode(name=%s, attrs=%s, content=%s,'
               ' len(children)=%d, opts=%s)' % ('    ' * ident_level,
                                                tree_node.name,
                                                tree_node.attrs,
                                                repr(tree_node.content),
                                                len(tree_node.children),
                                                tree_node.opts.__class__.__name__),
               '!! Parent mismatch !!' if tree_node.parent != expected_parent else '')

    # Process all children
    for child_node in tree_node.children:
        debug_print_ast(child_node, ident_level + 1, tree_node, print_fnct)
