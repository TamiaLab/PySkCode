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


class ListTagOptions(TagOptions):
    """ List tag options container class. """

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

    def get_list_type(self, tree_node):
        """
        Get the type of this list.
        The type can be set by setting the ``list_type_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``list_type_attr_name``.
        :param tree_node: The current tree node instance.
        :return The type of this list, or the default one.
        """

        # Get the list type
        list_type = tree_node.attrs.get(tree_node.name, '')
        if not list_type:
            list_type = tree_node.attrs.get(self.list_type_attr_name, self.default_list_type)

        # Check for alias, then normalize
        if list_type in self.list_type_alias:
            list_type = self.list_type_alias[list_type]
        list_type = list_type.lower()

        # White list list type
        if list_type not in self.allowed_list_types:
            list_type = self.default_list_type

        # Return the type
        return list_type

    def get_list_first_number(self, tree_node):
        """
        Get the first number of the list for ordering.
        :param tree_node: The current tree node instance.
        :return: The first number of the list, or 1.
        """
        first_number = tree_node.attrs.get(self.list_start_number_attr_name, '')
        if not first_number:
            return 1
        try:
            first_number = int(first_number)
            if first_number > 0:
                return first_number
        except ValueError:
            return 1
        return 1

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the list type
        list_type = self.get_list_type(tree_node)

        # Render the list container
        if list_type == UNORDERED_LIST_TYPE:
            return self.html_render_template_ul.format(inner_html=inner_html)
        else:

            # Get list first number
            first_list_number = self.get_list_first_number(tree_node)

            # Render the ordered list
            if first_list_number != 1:
                return self.html_render_template_ol_start_number.format(list_type=self.html_list_type_lut[list_type],
                                                                        list_start=first_list_number,
                                                                        inner_html=inner_html)
            else:
                return self.html_render_template_ol.format(list_type=self.html_list_type_lut[list_type],
                                                           inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        return inner_text

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get the list type
        list_type = self.get_list_type(tree_node)
        return {
                   self.list_type_attr_name: self.alias_list_type_lut[list_type]
               }, self.list_type_attr_name

    def get_skcode_non_ignored_empty_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attribute names not to be ignored when empty.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A tuple of all attribute names not to be ignored when empty.
        """
        return self.list_type_attr_name,


class UnorderedListTagOptions(ListTagOptions):
    """ Un-ordered list tag options container class. """

    canonical_tag_name = 'ul'
    alias_tag_names = ()

    def get_list_type(self, tree_node):
        """
        Get the type of this list.
        :param tree_node: The current tree node instance.
        :return Always ``UNORDERED_LIST_TYPE``.
        """
        return UNORDERED_LIST_TYPE

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        return {}, None


class OrderedListTagOptions(ListTagOptions):
    """ Ordered list tag options container class. """

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


class ListElementTagOptions(TagOptions):
    """ List element tag options container class. """

    same_tag_closes = True
    make_paragraphs_here = True

    canonical_tag_name = 'li'
    alias_tag_names = ('*', )

    # Default parent list type
    default_list_type = UNORDERED_LIST_TYPE

    # Base option class of all lists
    base_list_class = ListTagOptions

    # HTML template for rendering
    html_render_template = '<li>{inner_html}</li>\n'

    def get_parent_list_type(self, tree_node):
        """
        Get the parent list type.
        :param tree_node: The current tree node instance.
        :return The parent list type, or the default one.
        """
        assert tree_node.parent, "A list element cannot be a root tree node."
        parent_opts = tree_node.parent.opts
        if isinstance(parent_opts, self.base_list_class):
            return parent_opts.get_list_type(tree_node.parent)
        else:
            return self.default_list_type

    def get_parent_list_first_number(self, tree_node):
        """
        Get the parent list first number.
        :param tree_node: The current tree node instance.
        :return The parent list first number, or 1.
        """
        assert tree_node.parent, "A list element cannot be a root tree node."
        parent_opts = tree_node.parent.opts
        if isinstance(parent_opts, self.base_list_class):
            return parent_opts.get_list_first_number(tree_node.parent)
        else:
            return 1

    def get_element_number_from_parent(self, tree_node):
        """
        Get the current element number from the parent node.
        :param tree_node: The current tree node instance.
        :return The current element number of this list item.
        """
        assert tree_node.parent, "A list element cannot be a root tree node."
        parent_node_children = tree_node.parent.children
        cur_index = parent_node_children.index(tree_node)
        children_before_cur = parent_node_children[:cur_index]
        count = sum([1 if isinstance(child.opts, ListElementTagOptions) else 0 for child in children_before_cur])
        return count + self.get_parent_list_first_number(tree_node)

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

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        bullet = self.get_list_bullet(tree_node)
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
