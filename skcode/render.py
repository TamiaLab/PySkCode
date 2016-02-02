"""
SkCode rendering code.
"""


def render_inner_html(tree_node, **kwargs):
    """
    Render all children of the given tree node as HTML.
    :param tree_node: The parent tree node with children to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_html`` callback method.
    :return The rendered children tree as HTML.
    """

    # Get the inner HTML
    inner_html = []
    for child_node in tree_node.children:
        inner_html.append(render_to_html(child_node, **kwargs))

    # Return the inner HTML as string
    return ''.join(inner_html)


def render_to_html(tree_node, **kwargs):
    """
    Render the given tree node and children recursively as HTML.
    :param tree_node: The tree node to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_html`` callback method.
    :return The rendered document tree as HTML.
    """

    # Get the inner HTML
    inner_html = render_inner_html(tree_node, **kwargs)

    # Render the node
    return tree_node.opts.render_html(tree_node, inner_html, **kwargs)


def render_inner_text(tree_node, **kwargs):
    """
    Render all children of the given tree node as text.
    :param tree_node: The parent tree node with children to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_text`` callback method.
    :return The rendered children tree as text.
    """

    # Get the inner text
    inner_text = []
    for child_node in tree_node.children:
        inner_text.append(render_to_text(child_node, **kwargs))

    # Return the inner text as string
    return ''.join(inner_text)


def render_to_text(tree_node, **kwargs):
    """
    Render the given tree node and children recursively as text.
    :param tree_node: The tree node to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_text`` callback method.
    :return The rendered document tree as text.
    """

    # Get the inner text
    inner_text = render_inner_text(tree_node, **kwargs)

    # Render the node
    return tree_node.opts.render_text(tree_node, inner_text, **kwargs)


def render_inner_skcode(tree_node, **kwargs):
    """
    Render all children the given tree node as SkCode.
    :param tree_node: The parent tree node with children to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_skcode`` callback method.
    :return The rendered children tree as SkCode.
    """

    # Get the inner SkCode
    inner_skcode = []
    for child_node in tree_node.children:
        inner_skcode.append(render_to_skcode(child_node, **kwargs))

    # Return the inner SkCode as string
    return ''.join(inner_skcode)


def render_to_skcode(tree_node, **kwargs):
    """
    Render the given tree node and children recursively as SkCode.
    :param tree_node: The document tree node to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_skcode`` callback method.
    :return The rendered document tree as SkCode.
    """

    # Get inner SkCode
    inner_skcode = render_inner_skcode(tree_node, **kwargs)

    # Render the node
    return tree_node.opts.render_skcode(tree_node, inner_skcode, **kwargs)
