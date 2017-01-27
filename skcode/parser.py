"""
SkCode tag parsing code.
"""

import string


# Character charsets
WHITESPACE_CHARSET = frozenset(string.whitespace)
IDENTIFIER_CHARSET = frozenset(string.ascii_letters + string.digits + '_*')


def skip_whitespaces(text: str, offset: int):
    """
    Skip any whitespaces.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :return The new offset in the input text.
    """
    while text[offset] in WHITESPACE_CHARSET:
        offset += 1
    return offset


def get_identifier(text: str, offset: int):
    """
    Get the identifier string starting in the text at the given offset.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :return The identifier normalized as lowercase and the new offset in the input text.
    """
    identifier = ''

    # Get any identifier char
    while text[offset] in IDENTIFIER_CHARSET:
        identifier += text[offset]
        
        # Process the next char
        offset += 1

    # Normalize the identifier and return new values
    return identifier.lower(), offset


def get_attribute_value(text: str, offset: int, opening_tag_ch: str, closing_tag_ch: str):
    """
    Get the attribute value starting in the text at the given offset.
    :param text: The input text.
    :param offset: The current offset in the input text.
    :param opening_tag_ch: The opening tag char (must be one char long).
    :param closing_tag_ch: The closing tag char (must be one char long).
    :return The attribute value with trailing whitespaces removed and the new offset in the input text.
    """
    attribute_value = ''
    
    # Handle quoted and unquoted value
    if text[offset] == "'" or text[offset] == '"':
        quoting_ch = text[offset]

        # Process the next char
        offset += 1

        # Get attribute value
        while text[offset] != quoting_ch:

            # Handle escape sequences
            if text[offset] == '\\':

                # Process the next char
                offset += 1

                # Only the quoting char and the backslash char can be escaped
                if text[offset] != quoting_ch and text[offset] != '\\':
                    attribute_value += '\\'
                
            # Store the char
            attribute_value += text[offset]

            # Process the next char
            offset += 1

        # Skip last quoting sign
        offset += 1

    else:

        # Get raw attribute value
        ch = text[offset]
        while ch != closing_tag_ch and ch != opening_tag_ch and ch not in WHITESPACE_CHARSET:
            attribute_value += ch

            # Process the next char
            offset += 1
            ch = text[offset]

    # Check format
    if text[offset] != closing_tag_ch and text[offset] not in WHITESPACE_CHARSET:
        raise ValueError('A whitespace is mandatory after the attribute '
                         'value if not followed by the closing tag char')

    # Strip the attribute value and return new values
    return attribute_value.strip(), offset


def parse_tag(text: str, start_offset: int,
              opening_tag_ch='[', closing_tag_ch=']',
              allow_tagvalue_attr=True, allow_self_closing_tags=True):
    """
    Parse the text starting at ``start_offset`` to extract a valid tag, if any.
    Return the tag name, the ``is_closing_tag`` and ``is_self_closing_tag`` flags,
    the tag attributes (as a dictionary) and the offset just after the end of the tag.
    If something goes wrong (malformed tag, unexpected end-of-file, etc.) an exception
    of type``IndexError`` (unexpected end-of-file) or ``ValueError`` (malformed tag) is raised.
    :param text: The input text.
    :param start_offset: The offset in the input text to start with.
    :param opening_tag_ch: The opening tag char (must be one char long, default '[').
    :param closing_tag_ch: The closing tag char (must be one char long, default ']').
    :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut
    (default is ``True``).
    :param allow_self_closing_tags: Set to ``True`` to allow the self closing tags syntax (default is ``True``).
    :return A tuple ``(tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1)`` on success, or an
    exception on error (see possible exception in the docstring above).
    """
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
    offset = skip_whitespaces(text, start_offset + 1)

    # Check for closing tag
    if text[offset] == '/':

        # Look like a closing tag for me
        is_closing_tag = True

        # Skip slash and whitespaces
        offset = skip_whitespaces(text, offset + 1)

    # Get the tag name
    tag_name, offset = get_identifier(text, offset)

    # Detect invalid tag early
    if not tag_name:
        raise ValueError('Invalid tag format: no tag name found')

    # Skip whitespaces
    offset = skip_whitespaces(text, offset)

    # Check for closing char if is_closing_tag is set (closing tags have no attribute)
    if is_closing_tag and text[offset] != closing_tag_ch:
        raise ValueError('Invalid tag format: closing tags cannot have attribute')

    # Check for tag value
    if text[offset] == '=':

        # Check for support
        if not allow_tagvalue_attr:
            raise ValueError('Invalid tag format: tagname=tagvalue shortcut support disabled by caller.')

        # Skip equal sign and whitespaces
        offset = skip_whitespaces(text, offset + 1)

        # Get the tag value
        tag_value, offset = get_attribute_value(text, offset, opening_tag_ch, closing_tag_ch)

        # Store the tag value
        tag_attrs[tag_name] = tag_value

        # Skip whitespaces
        offset = skip_whitespaces(text, offset)

    # Named attributes handling
    while text[offset] != closing_tag_ch and text[offset] != '/':

        # Get the attribute name
        attr_name, offset = get_identifier(text, offset)

        # Detect erroneous attribute name
        if not attr_name:
            raise ValueError('Invalid tag format: no attribute name found or invalid character found')

        # Skip whitespaces
        offset = skip_whitespaces(text, offset)

        # Check for attr value
        if text[offset] == '=':

            # Skip equal sign and whitespaces
            offset = skip_whitespaces(text, offset + 1)
            
            # Get the attribute value
            attr_value, offset = get_attribute_value(text, offset, opening_tag_ch, closing_tag_ch)
            
            # Store the tag value
            tag_attrs[attr_name] = attr_value

            # Skip whitespaces
            offset = skip_whitespaces(text, offset)

        else:

            # Attribute without value
            tag_attrs[attr_name] = ''

    # Handle self closing tag
    if text[offset] == '/':

        # Check for support
        if not allow_self_closing_tags:
            raise ValueError('Invalid tag format: self closing tags support disabled by caller.')

        # Look like a self closing tag for me
        is_self_closing_tag = True

        # Skip slash and whitespaces
        offset = skip_whitespaces(text, offset + 1)

    # Assert end of tag
    if text[offset] != closing_tag_ch:
        raise ValueError('Invalid tag format: malformed end of tag')
    
    # Emit the tag
    return tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset + 1
