"""
SkCode AST tree builder code.
"""

from .etree import (RootTreeNode,
                    ROOT_NODE_NAME,
                    TEXT_NODE_NAME,
                    NEWLINE_NODE_NAME)
from .tags import (RootTagOptions,
                   TextTagOptions,
                   ErroneousTextTagOptions,
                   NewlineTagOptions,
                   DEFAULT_RECOGNIZED_TAGS)
from .tokenizer import (tokenize_tag,
                        TOKEN_DATA,
                        TOKEN_NEWLINE,
                        TOKEN_OPEN_TAG,
                        TOKEN_CLOSE_TAG,
                        TOKEN_SELF_CLOSE_TAG)


def parse_skcode(text,
                 recognized_tags=DEFAULT_RECOGNIZED_TAGS,
                 opening_tag_ch='[', closing_tag_ch=']',
                 allow_tagvalue_attr=True, allow_self_closing_tags=True,
                 root_node_opts=RootTagOptions(),
                 text_node_opts=TextTagOptions(),
                 erroneous_text_node_opts=ErroneousTextTagOptions(),
                 newline_node_opts=NewlineTagOptions(),
                 drop_unrecognized=False,
                 texturize_unclosed_tags=False,
                 drop_erroneous=False,
                 max_nesting_depth=16):
    """
    Parse the given text as a SkCode formatted document.
    Return the resulting document tree (DOM-like parser).
    :param text: The input text to be parsed.
    :param recognized_tags: Dictionary {tag_name: options} containing all valid tags declarations.
    :param opening_tag_ch: The opening tag char (must be one char long)
    :param closing_tag_ch: The closing tag char (must be one char long)
    :param allow_tagvalue_attr: Set to True to allow the BBcode ``tagname=tagvalue`` syntax shortcut (default True).
    :param allow_self_closing_tags: Set to True to allow self closing tags syntax (default True).
    :param root_node_opts: Node options for the root node.
    :param text_node_opts: Node options for all text nodes.
    :param erroneous_text_node_opts: Node options for all erroneous text nodes.
    :param newline_node_opts: Node options for all newlines.
    :param drop_unrecognized: If set to True, any unknown tag will be drop (default to False).
    :param texturize_unclosed_tags: If set, unclosed tag will be turn into erroneous text node.
    :param drop_erroneous: If set, erroneous nodes during sanitation will be drop instead of being unwrapped.
    :param max_nesting_depth: Maximum nesting depth, set to zero to disable (default to 16).
    :return The resulting document tree at the end of the parsing stage.
    """
    assert len(opening_tag_ch) == 1, "Opening tag character must be one char long exactly."
    assert len(closing_tag_ch) == 1, "Closing tag character must be one char long exactly."
    assert root_node_opts, "Root node options is mandatory."
    assert text_node_opts, "Text node options is mandatory."
    assert erroneous_text_node_opts, "Erroneous text node options is mandatory."
    assert newline_node_opts, "Newline node options is mandatory."

    # Anti oops
    assert ROOT_NODE_NAME not in recognized_tags, \
        'The "%s" tag is reserved for internal use only.' % ROOT_NODE_NAME
    assert TEXT_NODE_NAME not in recognized_tags, \
        'The "%s" tag is reserved for internal use only.' % TEXT_NODE_NAME
    assert NEWLINE_NODE_NAME not in recognized_tags, \
        'The "%s" tag is reserved for internal use only.' % NEWLINE_NODE_NAME

    # Init parser
    root_tree_node = tree_node = RootTreeNode(root_node_opts)
    swallow_next_newline = False
    cur_nesting_depth = 0

    # Cleanup text to avoid parsing useless trailing whitespaces
    text = text.strip()

    # Shortcut for empty text
    if not text:
        return root_tree_node

    # Tokenize the text
    for token in tokenize_tag(text,
                              opening_tag_ch, closing_tag_ch,
                              allow_tagvalue_attr, allow_self_closing_tags):
        
        # Unpack the token
        token_type, tag_name, tag_attrs, token_source = token

        # Handle DATA block
        if not tree_node.opts.parse_embedded:

            # Handle swallow_trailing_newline option
            if token_type == TOKEN_NEWLINE and swallow_next_newline:
                swallow_next_newline = False
                continue

            # Ignore newline_closes option

            # Wait for closing tag
            if token_type != TOKEN_CLOSE_TAG \
               or tag_name != tree_node.name:

                # Append the raw source to the node until closing tag found
                tree_node.content += token_source
                continue

        # Handle unrecognized tags
        if tag_name and tag_name not in recognized_tags:

            # Handle swallow_trailing_newline option
            swallow_next_newline = False

            # Turn the token into raw data if not dropped
            if not drop_unrecognized:
                tree_node.new_child(TEXT_NODE_NAME, erroneous_text_node_opts,
                                    content=token_source)

        # SAX-like tree building algorithm
        elif token_type == TOKEN_DATA:

            # Handle swallow_trailing_newline option
            swallow_next_newline = False
            
            # Append to the current node
            tree_node.new_child(TEXT_NODE_NAME, text_node_opts,
                                content=token_source)
            
        elif token_type == TOKEN_NEWLINE:

            # Handle swallow_trailing_newline option
            if swallow_next_newline:
                swallow_next_newline = False
            else:
                # Append to the current node
                tree_node.new_child(NEWLINE_NODE_NAME, newline_node_opts,
                                    content=token_source)

            # Handle newline_closes option
            # Loop to handle the case when nested tag need to be closed at once
            while tree_node.opts.newline_closes and tree_node.parent is not None:
                tree_node = tree_node.parent
            
        elif token_type == TOKEN_OPEN_TAG:

            # Handle nesting depth limit
            if cur_nesting_depth >= max_nesting_depth:

                # Tag cannot be open, fallback as (erroneous) text
                tree_node.new_child(TEXT_NODE_NAME, erroneous_text_node_opts,
                                    content=token_source)

                # End of processing for this tag
                continue

            # Handle same_tag_closes option
            if tree_node.opts.same_tag_closes \
               and tag_name == tree_node.name \
               and tree_node.parent is not None:
                tree_node = tree_node.parent

            # Load tag options
            tag_opts = recognized_tags[tag_name]

            # Handle swallow_trailing_newline option
            swallow_next_newline = tag_opts.swallow_trailing_newline

            # Handle close_inlines
            if tag_opts.close_inlines:
                while tree_node.opts.inline and tree_node.parent is not None:
                    tree_node = tree_node.parent

            # Create a new child node
            new_node = tree_node.new_child(tag_name, tag_opts, attrs=tag_attrs,
                                           source_open_tag=token_source)

            # Jump to the new child node if not standalone
            if not tag_opts.standalone:
                tree_node = new_node

                # Update nesting depth limit
                cur_nesting_depth += 1
        
        elif token_type == TOKEN_CLOSE_TAG:

            # Handle swallow_trailing_newline option
            swallow_next_newline = False

            # Check if current node can be closed
            if tree_node.parent is None or tree_node.name != tag_name:

                # Tag cannot be closed, fallback as (erroneous) text
                tree_node.new_child(TEXT_NODE_NAME, erroneous_text_node_opts,
                                    content=token_source)

            else:

                # Close the current tree node
                tree_node.source_close_tag = token_source
                tree_node = tree_node.parent

                # Update nesting depth limit
                cur_nesting_depth -= 1
        
        elif token_type == TOKEN_SELF_CLOSE_TAG:

            # Load tag options
            tag_opts = recognized_tags[tag_name]

            # Handle swallow_trailing_newline option
            swallow_next_newline = tag_opts.swallow_trailing_newline

            # Detect erroneous self closing tag
            if not tag_opts.standalone:

                # Erroneous tag, fallback as (erroneous) text
                tree_node.new_child(TEXT_NODE_NAME, erroneous_text_node_opts,
                                    content=token_source)

                # Revert swallow_next_newline to False
                swallow_next_newline = False
                
            else:
                
                # Create a new child node
                tree_node.new_child(tag_name, tag_opts, attrs=tag_attrs,
                                    source_open_tag=token_source)

    # Unwrap unclosed tags and turn them into erroneous text node
    if texturize_unclosed_tags:
        while tree_node != root_tree_node and tree_node.parent is not None:
            tree_node.unwrap_as_erroneous(erroneous_text_node_opts)
            tree_node = tree_node.parent

    # Perform sanity check and post-parsing processing
    _sanitize_tree(root_tree_node, erroneous_text_node_opts, drop_erroneous)
    _postprocess_tree(root_tree_node, root_tree_node)

    # Return the resulting AST
    return root_tree_node


def _sanitize_tree(cur_tree_node, erroneous_text_node_opts, drop_erroneous):
    """
    Recursive method for sanitizing the given tree node.
    :param cur_tree_node: Current tree node.
    :param erroneous_text_node_opts: Erroneous text node options to use.
    :param drop_erroneous: Set to True if erroneous node should be dropped instead of unwrapped.
    """

    # Down to top visit order (depth-first algorithm)
    for child_node in cur_tree_node.children:
        _sanitize_tree(child_node, erroneous_text_node_opts, drop_erroneous)

    # Sanitize the node
    cur_tree_node.opts.sanitize_node(cur_tree_node,
                                     erroneous_text_node_opts,
                                     drop_erroneous)


def _postprocess_tree(cur_tree_node, root_tree_node):
    """
    Recursive method for post-processing the given tree node.
    :param cur_tree_node: Current tree node.
    :param root_tree_node: Root tree node instance (for document level information storage).
    """

    # Post-process the node
    go_down = cur_tree_node.opts.postprocess_node(cur_tree_node, root_tree_node)

    # Go down if allowed
    if go_down:
        for child_node in cur_tree_node.children:
            _postprocess_tree(child_node, root_tree_node)
