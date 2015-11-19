"""
SkCode list tag definitions code.
"""

from .base import TagOptions


# List types
UNORDERED_LIST_TYPE = 'bullet'
NUMERIC_LIST_TYPE = 'numeric'
UPPERCASE_LIST_TYPE = 'upper-alpha'
LOWERCASE_LIST_TYPE = 'lower-alpha'
UPPER_ROMAN_LIST_TYPE = 'upper-roman'
LOWER_ROMAN_LIST_TYPE = 'lower-roman'

# List type alias
LIST_TYPE_ALIAS = {
    '': UNORDERED_LIST_TYPE, 
    '1': NUMERIC_LIST_TYPE,
    'A': UPPERCASE_LIST_TYPE,
    'a': LOWERCASE_LIST_TYPE,
    'I': UPPER_ROMAN_LIST_TYPE,
    'i': LOWER_ROMAN_LIST_TYPE,
}

# List type to HTML type Look-Up-Table
HTML_LIST_TYPE_LUT = {
    NUMERIC_LIST_TYPE: '1',
    UPPERCASE_LIST_TYPE: 'A',
    LOWERCASE_LIST_TYPE: 'a',
    UPPER_ROMAN_LIST_TYPE: 'I',
    LOWER_ROMAN_LIST_TYPE: 'i',
}

ROMAN_NUMERALS = (
    ('M', 1000),
    ('CM', 900),
    ('D', 500),
    ('CD',400),
    ('C', 100),
    ('XC', 90),
    ('L', 50),
    ('XL', 40),
    ('X', 10),
    ('IX', 9),
    ('V', 5),
    ('IV', 4),
    ('I', 1),
)


def int_to_roman_numerals(value):
    assert value >= 0, "Value can only be positive."
    if not value:
        return ''
    numerals = []
    for numeral, ivalue in ROMAN_NUMERALS:
        while ivalue <= value:
            value -= ivalue
            numerals.append(numeral)
    return ''.join(numerals)


ALPHABET_NUMERALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def int_to_alphabet_numerals(value):
    assert value >= 0, "Value can only be positive."
    if not value:
        return ''
    numerals = []
    while value:
        value -= 1
        value, i = divmod(value, 26)
        numerals.append(ALPHABET_NUMERALS[i])
    return ''.join(reversed(numerals))


class ListTagOptions(TagOptions):
    """ List tag options container class. """

    # Allowed list types
    allowed_list_types = (
        UNORDERED_LIST_TYPE,
        NUMERIC_LIST_TYPE,
        UPPERCASE_LIST_TYPE,
        LOWERCASE_LIST_TYPE,
        UPPER_ROMAN_LIST_TYPE,
        LOWER_ROMAN_LIST_TYPE,
    )

    # Default list type
    default_list_type = UNORDERED_LIST_TYPE

    # List type attribute name
    list_type_attr_name = 'type'

    def get_list_type(self, tree_node):
        """
        Get the type of this list.
        The type can be set by setting the list_type_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), list_type_attr_name.
        :param tree_node: The current tree node instance.
        :return The type of this list, or the default one.
        """

        # Get the list type
        list_type = tree_node.attrs.get(tree_node.name, '')
        if not list_type:
            list_type = tree_node.attrs.get(self.list_type_attr_name, self.default_list_type)

        # Check for alias, then normalize
        if list_type in LIST_TYPE_ALIAS:
            list_type = LIST_TYPE_ALIAS[list_type]
        list_type = list_type.lower()

        # Whitelist list type
        if list_type not in self.allowed_list_types:
            list_type = self.default_list_type

        # Return the type
        return list_type

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the list type
        list_type = self.get_list_type(tree_node)

        # Render the list container
        if list_type == UNORDERED_LIST_TYPE:
            return '<ul>%s</ul>\n' % inner_html
        else:
            return '<ol type="%s">%s</ol>\n' % (HTML_LIST_TYPE_LUT[list_type], inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the list type
        list_type = self.get_list_type(tree_node)
        if list_type != self.default_list_type:
            extra_attrs = ' %s="%s"' % (self.list_type_attr_name, list_type)
        else:
            extra_attrs = ''

        # Render the list container
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)


class UnorderedListTagOptions(ListTagOptions):
    """ Un-ordered list tag options container class. """

    def get_list_type(self, tree_node):
        """
        Get the type of this list.
        :param tree_node: The current tree node instance.
        :return Always UNORDERED_LIST_TYPE.
        """
        return UNORDERED_LIST_TYPE

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class OrderedListTagOptions(ListTagOptions):
    """ Ordered list tag options container class. """

    # Allowed list types
    allowed_list_types = (
        NUMERIC_LIST_TYPE,
        UPPERCASE_LIST_TYPE,
        LOWERCASE_LIST_TYPE,
        UPPER_ROMAN_LIST_TYPE,
        LOWER_ROMAN_LIST_TYPE,
    )

    # Default list type
    default_list_type = NUMERIC_LIST_TYPE


class ListElementTagOptions(TagOptions):
    """ List element tag options container class. """

    make_paragraphs_here = True
    same_tag_closes = True

    # Default parent list type
    default_list_type = UNORDERED_LIST_TYPE

    def get_parent_list_type(self, tree_node):
        """
        Get the parent list type.
        :param tree_node: The current tree node instance.
        :return The parent list type, or the default one.
        """
        parent_opts = tree_node.parent.opts
        if isinstance(parent_opts, ListTagOptions):
            return parent_opts.get_list_type(tree_node.parent)
        else:
            return self.default_list_type

    def get_element_number_from_parent(self, tree_node):
        """
        Get the current element number from the parent node.
        :param tree_node: The current tree node instance.
        :return The current element number of this list item.
        """
        parent_node_children = tree_node.parent.children
        cur_index = parent_node_children.index(tree_node)
        children_before_cur = parent_node_children[:cur_index + 1]
        return sum([1 if isinstance(child.opts, ListElementTagOptions) else 0 for child in children_before_cur])

    def get_list_bullet(self, tree_node):
        """
        Get the list bullet for this element.
        :param tree_node: The current tree node instance.
        :return The bullet for this list item, as string.
        """
        element_num = self.get_element_number_from_parent(tree_node)
        parent_list_type = self.get_parent_list_type(tree_node)
        if parent_list_type == UNORDERED_LIST_TYPE:
            return '-'
        elif parent_list_type == NUMERIC_LIST_TYPE:
            return '%d.' % element_num
        elif parent_list_type == UPPERCASE_LIST_TYPE:
            return '%s.' % int_to_alphabet_numerals(element_num)
        elif parent_list_type == LOWERCASE_LIST_TYPE:
            return '%s.' % int_to_alphabet_numerals(element_num).lower()
        elif parent_list_type == UPPER_ROMAN_LIST_TYPE:
            return '%s.' % int_to_roman_numerals(element_num)
        elif parent_list_type == LOWER_ROMAN_LIST_TYPE:
            return '%s.' % int_to_roman_numerals(element_num).lower()

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<li>%s</li>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        bullet = self.get_list_bullet(tree_node)
        indent = ' ' * (len(bullet) + 1)
        lines = []
        is_first_line = True
        for line in inner_text.splitlines():
            if is_first_line:
                is_first_line = False
                lines.append('%s %s' % (bullet, line))
            else:
                lines.append('%s %s' % (indent, line))
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)
