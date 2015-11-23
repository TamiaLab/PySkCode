"""
SkCode footnotes utility code.
"""

from html import escape as escape_html

from .walketree import walk_tree_for_cls
from ..tags.footnotes import (FootnoteDeclarationTagOptions,
                              FOOTNOTE_ID_HTML_FORMAT,
                              FOOTNOTE_ID_HTML_FORMAT_BACKREF)
from ..render import (render_inner_html,
                      render_inner_text)


def extract_footnotes(document_tree,
                      footnote_declaration_ops_cls=FootnoteDeclarationTagOptions):
    """
    Extract all footnotes declaration present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param footnote_declaration_ops_cls: The options class used for footnote declarations.
    :return: A nested list like [(footnote_id, footnote_node), ]
    """

    # Map [(footnote_id: footnote_node), ] of footnotes found
    footnotes = []

    # For each footnote declaration
    for tree_node in walk_tree_for_cls(document_tree, footnote_declaration_ops_cls):

        # Get the footnote ID from the node
        footnote_id = tree_node.opts.get_footnote_id(tree_node)

        # Store the footnote entry
        footnotes.append((footnote_id,  tree_node))

    # Return the dict
    return footnotes


def render_footnotes_html(footnotes, **kwargs):
    """
    Render the extra HTML for the footnote declarations.
    :param footnotes: A nested list like [(footnote_id, footnote_node), ] to be rendered.
    :param kwargs: Extra keywords arguments for the ``render_inner_html`` function.
    :return: The rendered HTML section for the footnotes declarations.
    """

    # Shortcut if no footnotes
    if not footnotes:
        return ''

    # Output HTML
    html_output = ['<div class="footnotes">']

    # For each footnote
    for footnote_id, footnote_node in footnotes:

        # Render the footnote
        footnote_html = render_inner_html(footnote_node, **kwargs)

        # Craft the footnote declaration HTML
        footnote_declaration_html = '<a id="%s" href="#%s"><sup>[%s]</sup></a> ' % (
            escape_html(FOOTNOTE_ID_HTML_FORMAT % footnote_id),
            escape_html(FOOTNOTE_ID_HTML_FORMAT_BACKREF % footnote_id),
            footnote_id)

        # Add the footnote HTML to the output
        html_output.append('<p>')
        html_output.append(footnote_declaration_html)
        html_output.append(footnote_html)
        html_output.append('</p>')

    # Close the footnotes div
    html_output.append('</div>')

    # Return the final HTML
    return '\n'.join(html_output)


def render_footnotes_text(footnotes):
    """
    Render the extra text section for the footnote declarations.
    :param footnotes: A nested list like [(footnote_id, footnote_node), ] to be rendered.
    :return: The rendered text section for the footnotes declarations.
    """

    # Shortcut if no footnotes
    if not footnotes:
        return ''

    # Output HTML
    text_output = []

    # For each footnote
    for footnote_id, footnote_node in footnotes:

        # Render the footnote
        footnote_text = render_inner_text(footnote_node)

        # Craft the footnote declaration
        footnote_declaration_text = '[^%s]: ' % footnote_id

        # Add the footnote text to the output
        text_output.append(footnote_declaration_text)
        text_output.append(footnote_text)
        text_output.append('\n')

    # Close the footnotes div
    text_output.append('\n')

    # Return the final text
    return ''.join(text_output)
