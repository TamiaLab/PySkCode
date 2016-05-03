"""
SkCode footnotes utility code.
"""

from .walketree import walk_tree_for_cls
from ..tags.footnotes import FootnoteDeclarationTagOptions
from ..render import (render_inner_html,
                      render_inner_text)


def extract_footnotes(document_tree,
                      footnote_declaration_ops_cls=FootnoteDeclarationTagOptions):
    """
    Extract all footnotes declaration present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param footnote_declaration_ops_cls: The options class used for footnote declarations.
    :return: A list of all footnote node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    # TODO Replace *_cls with the new categories based system

    # List of footnotes found
    footnotes = []

    # For each footnote declaration
    for tree_node in walk_tree_for_cls(document_tree, footnote_declaration_ops_cls):

        # Store the footnote
        footnotes.append(tree_node)

    # Return the list
    return footnotes


def render_footnotes_html(footnotes,
                          wrapping_div_class_name='footnotes',
                          wrapping_p_class_name='footnotes-details',
                          **kwargs):
    """
    Render the extra HTML for the footnote declarations.
    :param footnotes: A list of footnotes to be rendered.
    :param wrapping_div_class_name: The CSS class name of the wrapping div (default to 'footnotes').
    :param wrapping_p_class_name: The CSS class name of the wrapping div (default to 'footnotes-details').
    :param kwargs: Extra keywords arguments for the ``render_inner_html`` function.
    :return: The rendered extra HTML for the footnotes details.
    """

    # Shortcut if no footnotes
    if not footnotes:
        return ''

    # Output HTML
    html_output = ['<div class="{class_name}">'.format(class_name=wrapping_div_class_name)]

    # For each footnote
    for footnote_node in footnotes:

        # Get the footnote ID
        footnote_id = footnote_node.opts.get_footnote_id(footnote_node, footnote_node.root_tree_node)

        # Craft the footnote declaration HTML
        footnote_declaration_html = '<a id="{refid}" href="#{backrefid}"><sup>[{fnid}]</sup></a>'.format(
            refid=footnote_node.opts.get_footnote_ref_id(footnote_id),
            backrefid=footnote_node.opts.get_footnote_backref_id(footnote_id),
            fnid=footnote_id)

        # Render the footnote
        footnote_html = render_inner_html(footnote_node, **kwargs)

        # Add the footnote HTML to the output
        html_output.append('<p class="{class_name}">'.format(class_name=wrapping_p_class_name))
        html_output.append(footnote_declaration_html)
        html_output.append(footnote_html)
        html_output.append('</p>')

    # Close the footnotes div
    html_output.append('</div>')

    # Return the final HTML
    return '\n'.join(html_output)


def render_footnotes_text(footnotes):
    """
    Render the extra text for the footnote declarations.
    :param footnotes: A list of footnotes to be rendered.
    :return: The rendered extra text for the footnotes details.
    """

    # Shortcut if no footnotes
    if not footnotes:
        return ''

    # Output HTML
    text_output = []

    # For each footnote
    for footnote_node in footnotes:

        # Get the footnote ID
        footnote_id = footnote_node.opts.get_footnote_id(footnote_node, footnote_node.root_tree_node)

        # Render the footnote
        footnote_text = render_inner_text(footnote_node)

        # Craft the footnote declaration
        footnote_declaration_text = '[^%s]: ' % footnote_id

        # Add the footnote text to the output
        text_output.append(footnote_declaration_text + footnote_text.strip())
        text_output.append('\n')

    # Close the footnotes div
    text_output.append('\n')

    # Return the final text
    return ''.join(text_output)
