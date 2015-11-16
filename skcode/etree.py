"""
SkCode tree element code.
"""

# Reserved tag names
ROOT_NODE_NAME = 'root'
TEXT_NODE_NAME = 'text'
NEWLINE_NODE_NAME = 'newline'


class TreeNode(object):
    """
    Simple tree node container class.
    """

    def __init__(self, parent, name, opts, attrs=None, content='',
                 children=None, source_open_tag='', source_close_tag=''):
        """
        Create a new tree node.
        :param parent: Node parent instance (mandatory).
        :param name: Node name (mandatory).
        :param opts: Node options (mandatory).
        :param attrs: Node attributes (default to empty dictionary).
        :param content: Node content (default to empty string).
        :param children: Node children list (default to empty list).
        :param source_open_tag: Node source for opening tag (default to empty string).
        :param source_close_tag: Node source for closing tag (default to empty string).
        """
        assert name, "Node name must be specified."
        assert opts, "Node options must be specified."

        # Store value as attributes
        self.parent = parent
        self.name = name
        self.opts = opts
        self.attrs = attrs or {}
        self.content = content
        self.children = children or []
        self.source_open_tag = source_open_tag
        self.source_close_tag = source_close_tag

        # Rebase children parent
        for child in self.children:
            child.parent = self

    def new_child(self, *args, **kwargs):
        """
        Create a new child node from the given arguments.
        Auto set the parent attribute and append the newly created child node to the parent children list.
        :param args: Positional arguments for the TreeNode class constructor.
        :param kwargs: Keyword arguments for the TreeNode class constructor.
        :return: The newly created node instance.
        """
        new_child_node = TreeNode(self, *args, **kwargs)
        self.children.append(new_child_node)
        return new_child_node

    def get_raw_content(self):
        """
        Get the raw content of this tag, including any child content.
        """
        content = self.content
        for child_node in self.children:
            content += child_node.get_raw_content()
        return content

    def unwrap_as_erroneous(self, erroneous_text_node_opts):
        """
        Unwrap this node and dump his raw source code as erroneous text.
        :param erroneous_text_node_opts: Options to be used when creating the new erroneous text node.
        """

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
            new_children.append(TreeNode(my_parent, TEXT_NODE_NAME, erroneous_text_node_opts,
                                         content=self.source_open_tag))

        # Rebase all children of this node
        for child_node in self.children:
            child_node.parent = my_parent
            new_children.append(child_node)

        # Add the closing tag source of this node
        if self.source_close_tag:
            new_children.append(TreeNode(my_parent, TEXT_NODE_NAME, erroneous_text_node_opts,
                                         content=self.source_close_tag))

        # Finish the job
        new_children.extend(nodes_after_cur)
        my_parent.children = new_children

    def delete_from_parent(self):
        """
        Remove this node from his parent children list.
        """

        # Commit suicide
        self.parent.children.remove(self)


class RootTreeNode(TreeNode):
    """ Root tree node subclass of TreeNode. """

    def __init__(self, opts, attrs=None, children=None):
        """
        Create a new root tree node.
        :param opts: Root node options (mandatory).
        :param attrs: Root node attributes (default to empty dictionary).
        :param children: Root node children list (default to empty list).
        """
        super(RootTreeNode, self).__init__(None, ROOT_NODE_NAME, opts, attrs, children=children)

    def unwrap_as_erroneous(self, erroneous_text_node_opts):
        """
        Unwrap this node and dump his raw source code as erroneous text.
        This method is not implemented for the root tree node.
        :param erroneous_text_node_opts: Options to be used when creating the new erroneous text node.
        """
        raise NotImplementedError('Root tree node cannot be unwrapped.')

    def delete_from_parent(self):
        """
        Remove this node from his parent children list.
        This method is not implemented for the root tree node.
        """
        raise NotImplementedError('Root tree node cannot be deleted.')


def debug_print_ast(tree_node, ident_level=0, expected_parent=None):
    """
    Print the given AST tree to stdout for debugging purposes.
    :param tree_node: The tree node to be printed to stdout.
    :param ident_level: The current indentation level (default to 0).
    :param expected_parent: The excepted parent instance (for fast error detection during debug).
    """

    # Print info about the current tree node
    print('%sTreeNode(name=%s, attrs=%s, content=%s,'
          ' len(children)=%d, opts=%s)' % ('    ' * ident_level,
                                           tree_node.name,
                                           tree_node.attrs,
                                           repr(tree_node.content),
                                           len(tree_node.children),
                                           tree_node.opts.__class__.__name__),
          '!! Parent mismatch !!' if expected_parent is not None and tree_node.parent != expected_parent else '')

    # Process all children
    for child_node in tree_node.children:
        debug_print_ast(child_node, ident_level + 1, tree_node)
