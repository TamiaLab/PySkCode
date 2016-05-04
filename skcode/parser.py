"""
SkCode tag parsing code.
"""

# Character charsets
WHITESPACE_CHARSET = frozenset(' \t\r\n')
IDENTIFIER_CHARSET = frozenset('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789_*')


def skip_nb_char_then_whitespaces(text, offset, nb_char_to_skip=0):
    """
    Skip ``nb_char_to_skip`` char (default 0), then any whitespaces.
    Return the new offset and the new current char.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :param nb_char_to_skip: The number of char to be skipped.
    :return The new offset and the current char.
    """
    assert offset >= 0, "Input text offset must be greater or equal to zero."
    assert nb_char_to_skip >= 0, "The number of char to be skipped must be greater or equal to zero."

    # Skip char
    offset += nb_char_to_skip
    ch = text[offset]
    
    # Skip whitespaces
    while ch in WHITESPACE_CHARSET:
        offset += 1
        ch = text[offset]

    # Return new values
    return offset, ch


def get_identifier(text, offset, ch):
    """
    Get the identifier starting in the text at the given offset.
    Return the identifier (normalized as lower case), the new offset and the current char.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :param ch: The current char.
    :return The identifier normalized as lowercase, the new offset and the current char.
    """
    assert offset >= 0, "Input text offset must be greater or equal to zero."
    assert ch not in WHITESPACE_CHARSET, "The current char should not be a whitespace, call this function after " \
                                         "skipping any whitespaces."

    identifier = ''

    # Get any identifier char
    while ch in IDENTIFIER_CHARSET:

        # Store the char
        identifier += ch
        
        # Process the next char
        offset += 1
        ch = text[offset]

    # Normalize the identifier and return new values
    return identifier.lower(), offset, ch


def get_attribute_value(text, offset, ch, opening_tag_ch, closing_tag_ch):
    """
    Get the attribute value starting in the text at the given offset.
    Return the attribute value (stripped), the new offset and the current char.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :param ch: The current char.
    :param opening_tag_ch: The opening tag char.
    :param closing_tag_ch: The closing tag char.
    :return The attribute's value with trailing whitespaces removed, the new offset and the current char.
    """
    assert offset >= 0, "Input text offset must be greater or equal to zero."
    assert ch not in WHITESPACE_CHARSET, "The current char should not be a whitespace, call this function after " \
                                         "skipping any whitespaces."
    assert len(opening_tag_ch) == 1, "Opening tag character must be one char long exactly."
    assert len(closing_tag_ch) == 1, "Closing tag character must be one char long exactly."

    attr_value = ''
    
    # Handle quoted and unquoted value
    if ch == '\'' or ch == '"':

        # Store quoting char for later use
        quoting_ch = ch

        # Process the next char
        offset += 1
        ch = text[offset]

        # Get attribute value
        while ch != quoting_ch:

            # Handle escape sequences
            if ch == '\\':

                # Process the next char
                offset += 1
                ch = text[offset]

                # Only the quoting char and the backslash char can be escaped
                if ch != quoting_ch and ch != '\\':
                    attr_value += '\\'
                
            # Store the char
            attr_value += ch

            # Process the next char
            offset += 1
            ch = text[offset]

        # Skip last quoting sign
        offset += 1
        ch = text[offset]

    else:

        # Get raw attribute value
        while ch != closing_tag_ch and ch != opening_tag_ch and ch not in WHITESPACE_CHARSET:

            # Store the char
            attr_value += ch

            # Process the next char
            offset += 1
            ch = text[offset]

    # Check format
    if ch != closing_tag_ch and ch not in WHITESPACE_CHARSET:
        raise ValueError('A whitespace is mandatory after the attribute '
                         'value if not followed by the closing tag char')

    # Strip the attribute value and return new values
    return attr_value.strip(), offset, ch


def parse_tag(text, start_offset=0, opening_tag_ch='[', closing_tag_ch=']',
              allow_tagvalue_attr=True, allow_self_closing_tags=True):
    """
    Parse the text starting at ``start_offset`` to extract a valid tag, if any.
    Return the tag name, the ``is_closing_tag`` and ``is_self_closing_tag`` flags,
    the tag attributes (as a dictionary) and the offset just after the end of the tag.
    If something goes wrong (malformed tag, unexpected end-of-file, etc.) an exception
    of type``IndexError`` (unexpected end-of-file) or ``ValueError`` (malformed tag) is raised.
    :param text: The input text.
    :param start_offset: The offset in the input text to start with (default 0).
    :param opening_tag_ch: The opening tag char (must be one char long, default '[').
    :param closing_tag_ch: The closing tag char (must be one char long, default ']').
    :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut
    (default ``True``).
    :param allow_self_closing_tags: Set to ``True`` to allow the self closing tags syntax (default ``True``).
    :return A tuple ``(tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1)`` on success, or an
    exception on error (see possible exception in the docstring above).
    """

    # Fail if the  first char is not the opening tag char
    assert text, "No text input given (mandatory)."
    assert start_offset >= 0, "Starting offset must be greater or equal to zero."
    assert start_offset < len(text), "Starting offset must be lower than the size of the text."
    assert len(opening_tag_ch) == 1, "Opening tag character must be one char long exactly."
    assert len(closing_tag_ch) == 1, "Closing tag character must be one char long exactly."
    assert text[start_offset] == opening_tag_ch, "Unexpected call to parse_tag, no opening tag char at starting offset."

    # Init tag variables
    tag_attrs = {}
    is_closing_tag = is_self_closing_tag = False

    # Skip the opening char and whitespaces
    offset, ch = skip_nb_char_then_whitespaces(text, start_offset, 1)

    # Check for closing tag
    if ch == '/':

        # Look like a closing tag for me
        is_closing_tag = True

        # Skip slash and whitespaces
        offset, ch = skip_nb_char_then_whitespaces(text, offset, 1)

    # Get the tag name
    tag_name, offset, ch = get_identifier(text, offset, ch)

    # Detect invalid tag early
    if not tag_name:
        raise ValueError('Invalid tag format: no tag name found')

    # Skip whitespaces
    while ch in WHITESPACE_CHARSET:
        offset += 1
        ch = text[offset]

    # Check for closing char if is_closing_tag is set (closing tags have no attribute)
    if is_closing_tag and ch != closing_tag_ch:
        raise ValueError('Invalid tag format: closing tags cannot have attribute')

    # Check for tag value
    if ch == '=':

        # Check for support
        if not allow_tagvalue_attr:
            raise ValueError('Invalid tag format: tagname=tagvalue shortcut support disabled by caller.')

        # Skip equal sign and whitespaces
        offset, ch = skip_nb_char_then_whitespaces(text, offset, 1)

        # Get the tag value
        tag_value, offset, ch = get_attribute_value(text, offset, ch, opening_tag_ch, closing_tag_ch)

        # Store the tag value
        tag_attrs[tag_name] = tag_value

        # Skip whitespaces
        while ch in WHITESPACE_CHARSET:
            offset += 1
            ch = text[offset]

    # Named attributes handling
    while ch != closing_tag_ch and ch != '/':

        # Get the attribute name
        attr_name, offset, ch = get_identifier(text, offset, ch)

        # Detect erroneous attribute name
        if not attr_name:
            raise ValueError('Invalid tag format: no attribute name found or invalid character found')

        # Skip whitespaces
        while ch in WHITESPACE_CHARSET:
            offset += 1
            ch = text[offset]

        # Check for attr value
        if ch == '=':

            # Skip equal sign and whitespaces
            offset, ch = skip_nb_char_then_whitespaces(text, offset, 1)
            
            # Get the attribute value
            attr_value, offset, ch = get_attribute_value(text, offset, ch, opening_tag_ch, closing_tag_ch)
            
            # Store the tag value
            tag_attrs[attr_name] = attr_value

            # Skip whitespaces
            while ch in WHITESPACE_CHARSET:
                offset += 1
                ch = text[offset]

        else:

            # Attribute without value
            tag_attrs[attr_name] = ''

    # Handle self closing tag
    if ch == '/':

        # Check for support
        if not allow_self_closing_tags:
            raise ValueError('Invalid tag format: self closing tags support disabled by caller.')

        # Look like a self closing tag for me
        is_self_closing_tag = True

        # Skip slash and whitespaces
        offset, ch = skip_nb_char_then_whitespaces(text, offset, 1)

    # Assert end of tag
    if ch != closing_tag_ch:
        raise ValueError('Invalid tag format: malformed end of tag')
    
    # Emit the tag
    return tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1
