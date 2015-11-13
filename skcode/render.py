"""
SkCode rendering code.
"""


def render_to_html(tree_node, force_rel_nofollow=True):
    """
    Render the given AST tree as HTML.
    :param tree_node: The document tree node to be rendered.
    :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
    :return The rendered document tree as HTML.
    """

    # Get inner HTML
    inner_html = []
    for child_node in tree_node.children:
        inner_html.append(render_to_html(child_node))

    # Render the node
    return tree_node.opts.render_html(tree_node, ''.join(inner_html),
                                      force_rel_nofollow=force_rel_nofollow)


def render_to_text(tree_node):
    """
    Render the given AST tree as text.
    :param tree_node: The document tree node to be rendered.
    :return The rendered document tree as text.
    """

    # Get inner text
    inner_text = []
    for child_node in tree_node.children:
        inner_text.append(render_to_text(child_node))

    # Render the node
    return tree_node.opts.render_text(tree_node, ''.join(inner_text))


def render_to_skcode(tree_node):
    """
    Render the given AST tree as SkCode.
    :param tree_node: The document tree node to be rendered.
    :return The rendered document tree as SkCode.
    """

    # Get inner skcode
    inner_skcode = []
    for child_node in tree_node.children:
        inner_skcode.append(render_to_skcode(child_node))

    # Render the node
    return tree_node.opts.render_skcode(tree_node, ''.join(inner_skcode))
