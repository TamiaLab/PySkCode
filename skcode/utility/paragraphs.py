"""
SkCode auto paragraphs utility code.
"""

from ..etree import TreeNode
from ..tags import TextTreeNode, NewlineTreeNode


class ParagraphTreeNode(TreeNode):
    """ Paragraph tree node class. """

    # HTML class for the paragraph
    html_text_class = 'text-justify'

    # HTML template for the rendering
    html_render_template = '<p class="{class_name}">{inner_html}</p>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(class_name=self.html_text_class, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text.strip() + '\n\n'


def make_paragraphs(tree_node,
                    paragraph_node_cls=ParagraphTreeNode,
                    text_node_cls=TextTreeNode,
                    newline_node_cls=NewlineTreeNode):
    """
    Group all inline nodes into paragraphs according to each node options.
    :param tree_node: Tree node to be processed.
    :param paragraph_node_cls: The tree node class for all newly created paragraph nodes.
    :param text_node_cls: The tree node class for all text nodes.
    :param newline_node_cls: The tree node class for all newlines.
    """
    assert tree_node, "The tree node instance is mandatory."

    # Process all children first
    for child_node in tree_node.children:
        make_paragraphs(child_node, paragraph_node_cls, text_node_cls, newline_node_cls)

    # Process only block node with make_paragraphs_here option set
    if tree_node.inline or not tree_node.make_paragraphs_here:
        return

    # Group all inline node into paragraphs
    new_children = []
    cur_paragraph = None
    prev_was_newline = False
    for child_node in tree_node.children:

        # Ignore blank lines
        if isinstance(child_node, text_node_cls) and not child_node.content.strip() and not child_node.error_message:
            continue

        # Handle newlines
        if isinstance(child_node, newline_node_cls):

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
        elif child_node.inline:

            # This is not a newline
            prev_was_newline = False

            # Create a new paragraph if necessary
            if cur_paragraph is None:
                cur_paragraph = tree_node.new_child(None, paragraph_node_cls, append=False)

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
