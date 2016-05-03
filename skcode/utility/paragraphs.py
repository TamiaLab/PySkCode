"""
SkCode auto paragraphs utility code.
"""

from ..tags import TagOptions
from ..treebuilder import (TEXT_NODE_NAME,
                           NEWLINE_NODE_NAME)


# Paragraph node type
PARAGRAPH_NODE_NAME = '_paragraph'


class ParagraphTagOptions(TagOptions):
    """ Paragraph tag options container class. """

    # HTML class for the paragraph
    html_text_class = 'text-justify'

    # HTML template for the rendering
    html_render_template = '<p class="{class_name}">{inner_html}</p>\n'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(class_name=self.html_text_class, inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return '%s\n\n' % inner_text.strip()

    def render_skcode(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered SkCode of this node.
        """
        return '%s\n\n' % inner_skcode.strip()


def make_paragraphs(tree_node,
                    paragraph_node_opts=ParagraphTagOptions()):
    """
    Group all inline nodes into paragraphs according to each node options.
    :param tree_node: Tree node to be processed.
    :param paragraph_node_opts: Node options for all created paragraph nodes.
    """
    assert tree_node, "The tree node instance is mandatory."
    assert type(paragraph_node_opts).__name__ != 'type', \
        "The ``paragraph_node_opts`` parameter must be an instance of a class, not the class type itself."

    # Process all children first
    for child_node in tree_node.children:
        make_paragraphs(child_node, paragraph_node_opts)

    # Process only block node with make_paragraphs_here option set
    if tree_node.opts.inline \
       or not tree_node.opts.make_paragraphs_here:
        return

    # Group all inline node into paragraphs
    new_children = []
    cur_paragraph = None
    prev_was_newline = False
    for child_node in tree_node.children:

        # Ignore blank lines
        if child_node.name == TEXT_NODE_NAME \
           and not child_node.content.strip():
            continue

        # Handle newlines
        if child_node.name == NEWLINE_NODE_NAME:

            # If two consecutive newline are found
            if prev_was_newline:

                # And a paragraph exist
                if cur_paragraph is not None:

                    # Close the current paragraph
                    new_children.append(cur_paragraph)
                    cur_paragraph = None
            else:

                # Set the flag for the next newline
                prev_was_newline = True

                # Keep the first newline
                if cur_paragraph is not None:
                    
                    # Move the node into the paragraph
                    child_node.parent = cur_paragraph
                    cur_paragraph.children.append(child_node)

                else:
                    new_children.append(child_node)

        # Only group inline node
        elif child_node.opts.inline:

            # This is not a newline
            prev_was_newline = False

            # Create a new paragraph if necessary
            if cur_paragraph is None:
                cur_paragraph = tree_node.new_child(PARAGRAPH_NODE_NAME, paragraph_node_opts, append=False)

            # Move the node into the paragraph
            child_node.parent = cur_paragraph
            cur_paragraph.children.append(child_node)

        # Keep other nodes as-is
        else:

            # This is not a newline
            prev_was_newline = False

            # If a paragraph exist
            if cur_paragraph:

                # Close the paragraph
                new_children.append(cur_paragraph)
                cur_paragraph = None

            # Keep the node as-is
            new_children.append(child_node)

    # Dump the last paragraph if exist
    if cur_paragraph:
        new_children.append(cur_paragraph)

    # Update children list
    tree_node.children = new_children
