"""
SkCode list tag definitions code.
"""

from ..etree import TreeNode


# List types
UNORDERED_LIST_TYPE = 'bullet'
NUMERIC_LIST_TYPE = 'numeric'
UPPERCASE_LIST_TYPE = 'upper-alpha'
LOWERCASE_LIST_TYPE = 'lower-alpha'
UPPER_ROMAN_LIST_TYPE = 'upper-roman'
LOWER_ROMAN_LIST_TYPE = 'lower-roman'

# Roman numerals and value
ROMAN_NUMERALS = (
    ('M',  1000),
    ('CM', 900),
    ('D',  500),
    ('CD', 400),
    ('C',  100),
    ('XC', 90),
    ('L',  50),
    ('XL', 40),
    ('X',  10),
    ('IX', 9),
    ('V',  5),
    ('IV', 4),
    ('I',  1),
)

# Alphabet numerals (uppercase only)
ALPHABET_NUMERALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def int_to_roman_numerals(value):
    """
    Convert an integer to roman numerals.
    :param value: Input integer.
    :return: Roman numerals string
    """
    assert value >= 0, "Value can only be positive."
    if not value:
        return ''
    numerals = []
    for numeral, ivalue in ROMAN_NUMERALS:
        while ivalue <= value:
            value -= ivalue
            numerals.append(numeral)
    return ''.join(numerals)


def int_to_alphabet_numerals(value):
    """
    Convert an integer to alphabet numerals.
    :param value: Input integer.
    :return: Alphabet numerals string
    """
    assert value >= 0, "Value can only be positive."
    if not value:
        return ''
    numerals = []
    while value:
        value -= 1
        value, i = divmod(value, 26)
        numerals.append(ALPHABET_NUMERALS[i])
    return ''.join(reversed(numerals))


class ListTreeNode(TreeNode):
    """ List tree node class. """

    canonical_tag_name = 'list'
    alias_tag_names = ()

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

    # List start number attribute name
    list_start_number_attr_name = 'start'

    # List type alias
    list_type_alias = {
        '': UNORDERED_LIST_TYPE,
        '+': UNORDERED_LIST_TYPE,
        '-': UNORDERED_LIST_TYPE,
        '.': UNORDERED_LIST_TYPE,
        '1': NUMERIC_LIST_TYPE,
        'A': UPPERCASE_LIST_TYPE,
        'a': LOWERCASE_LIST_TYPE,
        'I': UPPER_ROMAN_LIST_TYPE,
        'i': LOWER_ROMAN_LIST_TYPE,
    }

    # List type to HTML type Look-Up-Table
    html_list_type_lut = {
        NUMERIC_LIST_TYPE: '1',
        UPPERCASE_LIST_TYPE: 'A',
        LOWERCASE_LIST_TYPE: 'a',
        UPPER_ROMAN_LIST_TYPE: 'I',
        LOWER_ROMAN_LIST_TYPE: 'i',
    }

    # List type to alias type Look-Up-Table
    alias_list_type_lut = {
        UNORDERED_LIST_TYPE: '',
        NUMERIC_LIST_TYPE: '1',
        UPPERCASE_LIST_TYPE: 'A',
        LOWERCASE_LIST_TYPE: 'a',
        UPPER_ROMAN_LIST_TYPE: 'I',
        LOWER_ROMAN_LIST_TYPE: 'i',
    }

    # HTML template for rendering unordered list
    html_render_template_ul = '<ul>{inner_html}</ul>\n'

    # HTML template for rendering ordered list
    html_render_template_ol = '<ol type="{list_type}">{inner_html}</ol>\n'

    # HTML template for rendering ordered list with a custom starting number
    html_render_template_ol_start_number = '<ol type="{list_type}" start="{list_start}">{inner_html}</ol>\n'

    def get_list_type(self):
        """
        Get the type of this list.
        The type can be set by setting the ``list_type_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``list_type_attr_name``.
        :return The type of this list, or the default one.
        """

        # Get the list type
        list_type = self.attrs.get(self.name, '')
        if not list_type:
            list_type = self.attrs.get(self.list_type_attr_name, self.default_list_type)

        # Check for alias, then normalize
        if list_type in self.list_type_alias:
            list_type = self.list_type_alias[list_type]
        list_type = list_type.lower()

        # White list list type
        if list_type not in self.allowed_list_types:
            list_type = self.default_list_type

        # Return the type
        return list_type

    def get_list_first_number(self):
        """
        Get the first number of the list for ordering.
        :return: The first number of the list, or 1.
        """
        first_number = self.attrs.get(self.list_start_number_attr_name, '')
        if not first_number:
            return 1
        try:
            first_number = int(first_number)
            if first_number > 0:
                return first_number
        except ValueError:
            return 1
        return 1

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the list type
        list_type = self.get_list_type()

        # Render the list container
        if list_type == UNORDERED_LIST_TYPE:
            return self.html_render_template_ul.format(inner_html=inner_html)
        else:

            # Get list first number
            first_list_number = self.get_list_first_number()

            # Render the ordered list
            if first_list_number != 1:
                return self.html_render_template_ol_start_number.format(list_type=self.html_list_type_lut[list_type],
                                                                        list_start=first_list_number,
                                                                        inner_html=inner_html)
            else:
                return self.html_render_template_ol.format(list_type=self.html_list_type_lut[list_type],
                                                           inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text


class UnorderedListTreeNode(ListTreeNode):
    """ Un-ordered list tree node class. """

    canonical_tag_name = 'ul'
    alias_tag_names = ()

    def get_list_type(self):
        """
        Get the type of this list.
        :return Always ``UNORDERED_LIST_TYPE``.
        """
        return UNORDERED_LIST_TYPE


class OrderedListTreeNode(ListTreeNode):
    """ Ordered list tree node class. """

    canonical_tag_name = 'ol'
    alias_tag_names = ()

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


class ListElementTreeNode(TreeNode):
    """ List element tree node class. """

    same_tag_closes = True
    weak_parent_close = True
    make_paragraphs_here = True

    canonical_tag_name = 'li'
    alias_tag_names = ('*', )

    # Default parent list type
    default_list_type = UNORDERED_LIST_TYPE

    # Base option class of all lists
    base_list_class = ListTreeNode

    # HTML template for rendering
    html_render_template = '<li>{inner_html}</li>\n'

    def get_parent_list_type(self):
        """
        Get the parent list type.
        :return The parent list type, or the default one.
        """
        if isinstance(self.parent, self.base_list_class):
            return self.parent.get_list_type()
        else:
            return self.default_list_type

    def get_parent_list_first_number(self):
        """
        Get the parent list first number.
        :return The parent list first number, or 1.
        """
        if isinstance(self.parent, self.base_list_class):
            return self.parent.get_list_first_number()
        else:
            return 1

    def get_element_number_from_parent(self):
        """
        Get the current element number from the parent node.
        :return The current element number of this list item.
        """
        parent_node_children = self.parent.children
        cur_index = parent_node_children.index(self)
        children_before_cur = parent_node_children[:cur_index]
        count = sum([1 if isinstance(child, ListElementTreeNode) else 0 for child in children_before_cur])
        return count + self.get_parent_list_first_number()

    def get_list_bullet(self):
        """
        Get the list bullet for this element.
        :return The bullet for this list item, as string.
        """
        element_num = self.get_element_number_from_parent()
        parent_list_type = self.get_parent_list_type()
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

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        bullet = self.get_list_bullet()
        indent = ' ' * len(bullet)
        lines = []
        is_first_line = True
        for line in inner_text.strip().splitlines():
            if is_first_line:
                is_first_line = False
                lines.append('%s %s' % (bullet, line))
            else:
                lines.append('%s %s' % (indent, line))
        if is_first_line:
            lines.append('%s' % bullet)
        lines.append('')
        return '\n'.join(lines)
