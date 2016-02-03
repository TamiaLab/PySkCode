"""
SkCode tag building code.
"""

from .tools import escape_attrvalue


def build_tag_str(tag_name, attrs=None, content='',
                  opening_tag_ch='[', closing_tag_ch=']',
                  allow_tagvalue_attr=True, standalone=False,
                  tagvalue_attr_name=None, non_ignored_empty_attrs=None):
    """
    Build a SkCode tag declaration string from the given tag attributes and options.
    :param tag_name: The tag name (mandatory).
    :param attrs: A dictionary of the tag attributes.
    A ``None`` value is interpreted as a standalone attribute.
    Empty values are ignored by default, unless the attribute name is in the ``non_ignored_empty_attrs`` list.
    :param content: The tag raw content.
    :param opening_tag_ch: The tag opening character, must be one character long exactly.
    :param closing_tag_ch: The tag closing character, must be one character long exactly.
    :param allow_tagvalue_attr: Set to ``True`` to allow the ``tagname=tagvalue`` shortcut syntax (default ``True``).
    :param standalone: Set to ``True`` to make this tag standalone (no closing tag, default ``False``).
    If set, the tag cannot have content. Self-closing syntax is **not** used for standalone tags.
    :param tagvalue_attr_name: The attribute name to be used for the ``tagname=tagvalue`` shortcut
    syntax (default to ``tag_name``).
    :param non_ignored_empty_attrs: A list of attribute names not to be ignored if empty.
    :return: The tag declaration string.
    """
    assert tag_name, "The tag name is mandatory."
    assert opening_tag_ch, "The opening tag character is mandatory."
    assert len(opening_tag_ch) == 1, "Opening tag character must be one char long exactly."
    assert closing_tag_ch, "The closing tag character is mandatory."
    assert len(closing_tag_ch) == 1, "Closing tag character must be one char long exactly."
    if standalone:
        assert not content, "Standalone tags cannot have content."

    # Handle default values
    attrs = attrs or {}
    tagvalue_attr_name = tagvalue_attr_name or tag_name
    non_ignored_empty_attrs = non_ignored_empty_attrs or ()

    # Handle the ``tagname=tagvalue`` shortcut syntax
    if allow_tagvalue_attr and tagvalue_attr_name in attrs:
        tag_value = attrs.pop(tagvalue_attr_name)
        tag_value = '=' + escape_attrvalue(tag_value) if tag_value or tagvalue_attr_name in non_ignored_empty_attrs else ''
    else:
        tag_value = ''

    # Craft the attributes string
    attrs_str = []
    for key, value in attrs.items():
        if value:
            attrs_str.append(key + '=' + escape_attrvalue(str(value)))
        elif value is None:
            attrs_str.append(key)
        elif key in non_ignored_empty_attrs:
            attrs_str.append(key + '=""')
    attrs_str = ' '.join(attrs_str)

    # Craft the tag declaration string
    if standalone:
        return ''.join((opening_tag_ch, tag_name, tag_value, ' ' if attrs_str else '', attrs_str, closing_tag_ch))
    else:
        return ''.join((opening_tag_ch, tag_name, tag_value, ' ' if attrs_str else '', attrs_str, closing_tag_ch,
                        content,
                        opening_tag_ch, '/', tag_name, closing_tag_ch))
