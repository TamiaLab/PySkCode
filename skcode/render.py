"""
SkCode rendering code.
"""


def render_inner_html(tree_node, force_rel_nofollow=True):
    """
    Render all children of the given AST tree as HTML.
    :param tree_node: The parent tree node with children to be rendered.
    :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
    :return The rendered children tree as HTML.
    """

    # Get inner HTML
    inner_html = []
    for child_node in tree_node.children:
        inner_html.append(render_to_html(child_node, force_rel_nofollow))

    # Return the inner HTML as string
    return ''.join(inner_html)


def render_to_html(tree_node, force_rel_nofollow=True):
    """
    Render the given AST tree as HTML.
    :param tree_node: The document tree node to be rendered.
    :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
    :return The rendered document tree as HTML.
    """

    # Get inner HTML
    inner_html = render_inner_html(tree_node, force_rel_nofollow)

    # Render the node
    return tree_node.opts.render_html(tree_node, inner_html, force_rel_nofollow)


def render_inner_text(tree_node):
    """
    Render all children of the given AST tree as text.
    :param tree_node: The parent tree node with children to be rendered.
    :return The rendered children tree as text.
    """

    # Get inner text
    inner_text = []
    for child_node in tree_node.children:
        inner_text.append(render_to_text(child_node))

    # Return the inner text as string
    return ''.join(inner_text)


def render_to_text(tree_node):
    """
    Render the given AST tree as text.
    :param tree_node: The document tree node to be rendered.
    :return The rendered document tree as text.
    """

    # Get inner text
    inner_text = render_inner_text(tree_node)

    # Render the node
    return tree_node.opts.render_text(tree_node, inner_text)


def render_inner_skcode(tree_node):
    """
    Render all children the given AST tree as SkCode.
    :param tree_node: The parent tree node with children to be rendered.
    :return The rendered children tree as SkCode.
    """

    # Get inner skcode
    inner_skcode = []
    for child_node in tree_node.children:
        inner_skcode.append(render_to_skcode(child_node))

    # Return the inner skcode as string
    return ''.join(inner_skcode)


def render_to_skcode(tree_node):
    """
    Render the given AST tree as SkCode.
    :param tree_node: The document tree node to be rendered.
    :return The rendered document tree as SkCode.
    """

    # Get inner skcode
    inner_skcode = render_inner_skcode(tree_node)

    # Render the node
    return tree_node.opts.render_skcode(tree_node, inner_skcode)
