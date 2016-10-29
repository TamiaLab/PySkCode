"""
SkCode lists tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    ListTreeNode,
    ListElementTreeNode,
    OrderedListTreeNode,
    UnorderedListTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.tags.lists import (
    UNORDERED_LIST_TYPE,
    NUMERIC_LIST_TYPE,
    UPPERCASE_LIST_TYPE,
    LOWERCASE_LIST_TYPE,
    UPPER_ROMAN_LIST_TYPE,
    LOWER_ROMAN_LIST_TYPE,
    ROMAN_NUMERALS,
    ALPHABET_NUMERALS,
    int_to_alphabet_numerals,
    int_to_roman_numerals
)


class NumeralHelpersTestCase(unittest.TestCase):
    """ Tests suite for the numerals helper routines. """

    def test_module_constants(self):
        """ Test the modules constants """
        self.assertEqual((
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
        ), ROMAN_NUMERALS)
        self.assertEqual('ABCDEFGHIJKLMNOPQRSTUVWXYZ', ALPHABET_NUMERALS)

    def test_int_to_roman_numerals_assertion(self):
        """ Test the ``int_to_roman_numerals`` helper routine. """
        with self.assertRaises(AssertionError) as e:
            int_to_roman_numerals(-1)
        self.assertEqual('Value can only be positive.', str(e.exception))

    def test_int_to_roman_numerals_no_value(self):
        """ Test the ``int_to_roman_numerals`` helper routine. """
        self.assertEqual('', int_to_roman_numerals(0))

    def test_int_to_roman_numerals(self):
        """ Test the ``int_to_roman_numerals`` helper routine. """
        self.assertEqual('I', int_to_roman_numerals(1))
        self.assertEqual('IV', int_to_roman_numerals(4))
        self.assertEqual('V', int_to_roman_numerals(5))
        self.assertEqual('IX', int_to_roman_numerals(9))
        self.assertEqual('X', int_to_roman_numerals(10))
        self.assertEqual('XL', int_to_roman_numerals(40))
        self.assertEqual('L', int_to_roman_numerals(50))
        self.assertEqual('XC', int_to_roman_numerals(90))
        self.assertEqual('C', int_to_roman_numerals(100))
        self.assertEqual('CD', int_to_roman_numerals(400))
        self.assertEqual('D', int_to_roman_numerals(500))
        self.assertEqual('CM', int_to_roman_numerals(900))
        self.assertEqual('M', int_to_roman_numerals(1000))
        self.assertEqual('LXIV', int_to_roman_numerals(64))
        self.assertEqual('CCXXVI', int_to_roman_numerals(226))
        self.assertEqual('CMXCVIII', int_to_roman_numerals(998))
        self.assertEqual('MDCCXII', int_to_roman_numerals(1712))
        self.assertEqual('MMXIV', int_to_roman_numerals(2014))

    def test_int_to_alphabet_numerals_assertion(self):
        """ Test the ``int_to_alphabet_numerals`` helper routine. """
        with self.assertRaises(AssertionError) as e:
            int_to_alphabet_numerals(-1)
        self.assertEqual('Value can only be positive.', str(e.exception))

    def test_int_to_alphabet_numerals_no_value(self):
        """ Test the ``int_to_alphabet_numerals`` helper routine. """
        self.assertEqual('', int_to_alphabet_numerals(0))

    def test_int_to_alphabet_numerals(self):
        """ Test the ``int_to_alphabet_numerals`` helper routine. """
        self.assertEqual('A', int_to_alphabet_numerals(1))
        self.assertEqual('B', int_to_alphabet_numerals(2))
        self.assertEqual('C', int_to_alphabet_numerals(3))
        self.assertEqual('Z', int_to_alphabet_numerals(26))
        self.assertEqual('AA', int_to_alphabet_numerals(27))
        self.assertEqual('AB', int_to_alphabet_numerals(28))
        self.assertEqual('AZ', int_to_alphabet_numerals(52))


class ListsTagTestCase(unittest.TestCase):
    """ Tests suite for the lists tag module. """

    def test_module_constants(self):
        """ Test the modules constants """
        self.assertEqual('bullet', UNORDERED_LIST_TYPE)
        self.assertEqual('numeric', NUMERIC_LIST_TYPE)
        self.assertEqual('upper-alpha', UPPERCASE_LIST_TYPE)
        self.assertEqual('lower-alpha', LOWERCASE_LIST_TYPE)
        self.assertEqual('upper-roman', UPPER_ROMAN_LIST_TYPE)
        self.assertEqual('lower-roman', LOWER_ROMAN_LIST_TYPE)

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(ListTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(ListTreeNode.newline_closes)
        self.assertFalse(ListTreeNode.same_tag_closes)
        self.assertFalse(ListTreeNode.weak_parent_close)
        self.assertFalse(ListTreeNode.standalone)
        self.assertTrue(ListTreeNode.parse_embedded)
        self.assertFalse(ListTreeNode.inline)
        self.assertTrue(ListTreeNode.close_inlines)
        self.assertEqual('list', ListTreeNode.canonical_tag_name)
        self.assertEqual((), ListTreeNode.alias_tag_names)
        self.assertFalse(ListTreeNode.make_paragraphs_here)
        self.assertEqual((
            UNORDERED_LIST_TYPE,
            NUMERIC_LIST_TYPE,
            UPPERCASE_LIST_TYPE,
            LOWERCASE_LIST_TYPE,
            UPPER_ROMAN_LIST_TYPE,
            LOWER_ROMAN_LIST_TYPE,
        ), ListTreeNode.allowed_list_types)
        self.assertEqual(UNORDERED_LIST_TYPE, ListTreeNode.default_list_type)
        self.assertEqual('type', ListTreeNode.list_type_attr_name)
        self.assertEqual('start', ListTreeNode.list_start_number_attr_name)
        self.assertEqual({
            '': UNORDERED_LIST_TYPE,
            '+': UNORDERED_LIST_TYPE,
            '-': UNORDERED_LIST_TYPE,
            '.': UNORDERED_LIST_TYPE,
            '1': NUMERIC_LIST_TYPE,
            'A': UPPERCASE_LIST_TYPE,
            'a': LOWERCASE_LIST_TYPE,
            'I': UPPER_ROMAN_LIST_TYPE,
            'i': LOWER_ROMAN_LIST_TYPE,
        }, ListTreeNode.list_type_alias)
        self.assertEqual({
            NUMERIC_LIST_TYPE: '1',
            UPPERCASE_LIST_TYPE: 'A',
            LOWERCASE_LIST_TYPE: 'a',
            UPPER_ROMAN_LIST_TYPE: 'I',
            LOWER_ROMAN_LIST_TYPE: 'i',
        }, ListTreeNode.html_list_type_lut)
        self.assertEqual({
            UNORDERED_LIST_TYPE: '',
            NUMERIC_LIST_TYPE: '1',
            UPPERCASE_LIST_TYPE: 'A',
            LOWERCASE_LIST_TYPE: 'a',
            UPPER_ROMAN_LIST_TYPE: 'I',
            LOWER_ROMAN_LIST_TYPE: 'i',
        }, ListTreeNode.alias_list_type_lut)
        self.assertEqual('<ul>{inner_html}</ul>\n', ListTreeNode.html_render_template_ul)
        self.assertEqual('<ol type="{list_type}">{inner_html}</ol>\n', ListTreeNode.html_render_template_ol)
        self.assertEqual('<ol type="{list_type}" start="{list_start}">{inner_html}</ol>\n',
                         ListTreeNode.html_render_template_ol_start_number)

    def test_get_list_type_with_tagname_set(self):
        """ Test the ``get_list_type`` method with the tag name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'list': 'numeric'})
        output_result = tree_node.get_list_type()
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_type_attr_set(self):
        """ Test the ``get_list_type`` method with the type attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': 'numeric'})
        output_result = ListTreeNode.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_tagname_and_type_attr_set(self):
        """ Test the ``get_list_type`` method with the tag name and type attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'list': '1', 'type': 'A'})
        output_result = tree_node.get_list_type()
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_no_type_set(self):
        """ Test the ``get_list_type`` method with no type set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={})
        output_result = tree_node.get_list_type()
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)

    def test_get_list_type_alias_type(self):
        """ Test the ``get_list_type`` method with an type name alias set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': '1'})
        output_result = tree_node.get_list_type()
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_type_uppercase(self):
        """ Test the ``get_list_type`` method with an type name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': 'numeRIC'})
        output_result = tree_node.get_list_type()
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_invalid_type(self):
        """ Test the ``get_list_type`` method with an invalid type name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': 'test'})
        output_result = tree_node.get_list_type()
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)

    def test_get_list_first_number_with_number(self):
        """ Test the ``get_list_first_number`` method with a positive number. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '3'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(3, output_result)

    def test_get_list_first_number_with_non_number(self):
        """ Test the ``get_list_first_number`` method with a non number value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': 'abcd'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_negative_number(self):
        """ Test the ``get_list_first_number`` method with a negative number. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '-3'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_zero(self):
        """ Test the ``get_list_first_number`` method with zero. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '0'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_no_value(self):
        """ Test the ``get_list_first_number`` method with no value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': ''})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)

    def test_sanitize_node(self):
        """ Test the ``sanitize_node`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '3'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(3, output_result)
        self.assertEqual('', tree_node.error_message)
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '-3'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)
        self.assertEqual('First line number must be positive', tree_node.error_message)
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': 'abcd'})
        output_result = tree_node.get_list_first_number()
        self.assertEqual(1, output_result)
        self.assertEqual('abcd is not a number', tree_node.error_message)

    def test_render_html_unordered(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = '<ul>test</ul>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_ordered(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': '1'})
        output_result = tree_node.render_html('test')
        expected_result = '<ol type="1">test</ol>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_ordered_with_start_number(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': '1', 'start': '3'})
        output_result = tree_node.render_html('test')
        expected_result = '<ol type="1" start="3">test</ol>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', ListTreeNode)
        output_result = tree_node.render_text('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)


class UnorderedListsTagTestCase(unittest.TestCase):
    """ Tests suite for the unordered lists tag module. """

    def test_subclassing(self):
        """ Test the modules constants """
        self.assertTrue(issubclass(UnorderedListTreeNode, ListTreeNode))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(UnorderedListTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(UnorderedListTreeNode.newline_closes)
        self.assertFalse(UnorderedListTreeNode.same_tag_closes)
        self.assertFalse(UnorderedListTreeNode.weak_parent_close)
        self.assertFalse(UnorderedListTreeNode.standalone)
        self.assertTrue(UnorderedListTreeNode.parse_embedded)
        self.assertFalse(UnorderedListTreeNode.inline)
        self.assertTrue(UnorderedListTreeNode.close_inlines)
        self.assertEqual('ul', UnorderedListTreeNode.canonical_tag_name)
        self.assertEqual((), UnorderedListTreeNode.alias_tag_names)
        self.assertFalse(UnorderedListTreeNode.make_paragraphs_here)

    def test_get_list_type(self):
        """ Test the ``get_list_type`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('list', UnorderedListTreeNode, attrs={'list': 'numeric'})
        output_result = tree_node.get_list_type()
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)


class OrderedListsTagTestCase(unittest.TestCase):
    """ Tests suite for the ordered lists tag module. """

    def test_subclassing(self):
        """ Test the modules constants """
        self.assertTrue(issubclass(OrderedListTreeNode, ListTreeNode))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(OrderedListTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(OrderedListTreeNode.newline_closes)
        self.assertFalse(OrderedListTreeNode.same_tag_closes)
        self.assertFalse(OrderedListTreeNode.weak_parent_close)
        self.assertFalse(OrderedListTreeNode.standalone)
        self.assertTrue(OrderedListTreeNode.parse_embedded)
        self.assertFalse(OrderedListTreeNode.inline)
        self.assertTrue(OrderedListTreeNode.close_inlines)
        self.assertEqual('ol', OrderedListTreeNode.canonical_tag_name)
        self.assertEqual((), OrderedListTreeNode.alias_tag_names)
        self.assertFalse(OrderedListTreeNode.make_paragraphs_here)

        self.assertEqual((
            NUMERIC_LIST_TYPE,
            UPPERCASE_LIST_TYPE,
            LOWERCASE_LIST_TYPE,
            UPPER_ROMAN_LIST_TYPE,
            LOWER_ROMAN_LIST_TYPE,
        ), OrderedListTreeNode.allowed_list_types)
        self.assertEqual(NUMERIC_LIST_TYPE, OrderedListTreeNode.default_list_type)


class ListElementTagTestCase(unittest.TestCase):
    """ Tests suite for the list elements tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(ListElementTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(ListElementTreeNode.newline_closes)
        self.assertTrue(ListElementTreeNode.same_tag_closes)
        self.assertTrue(ListElementTreeNode.weak_parent_close)
        self.assertFalse(ListElementTreeNode.standalone)
        self.assertTrue(ListElementTreeNode.parse_embedded)
        self.assertFalse(ListElementTreeNode.inline)
        self.assertTrue(ListElementTreeNode.close_inlines)
        self.assertEqual('li', ListElementTreeNode.canonical_tag_name)
        self.assertEqual(('*', ), ListElementTreeNode.alias_tag_names)
        self.assertTrue(ListElementTreeNode.make_paragraphs_here)
        self.assertEqual(UNORDERED_LIST_TYPE, ListElementTreeNode.default_list_type)
        self.assertEqual(ListTreeNode, ListElementTreeNode.base_list_class)
        self.assertEqual('<li>{inner_html}</li>\n', ListElementTreeNode.html_render_template)

    def test_get_parent_list_type_with_list_as_parent(self):
        """ Test the ``get_parent_list_type```method with a list as parent node. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': 'numeric'})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(NUMERIC_LIST_TYPE, tree_node.get_parent_list_type())

    def test_get_parent_list_type_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_type```method without a list as parent node. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(UNORDERED_LIST_TYPE, tree_node.get_parent_list_type())

    def test_get_parent_list_first_number_with_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method with a list as parent node. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'start': '5'})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(5, tree_node.get_parent_list_first_number())

    def test_get_parent_list_first_number_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method without a list as parent node. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(1, tree_node.get_parent_list_first_number())

    def test_get_element_number_from_parent_with_list_as_parent(self):
        """ Test the ``get_element_number_from_parent```method with a list as parent node. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode)
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(1, tree_node.get_element_number_from_parent())

    def test_get_element_number_from_parent_with_list_as_parent_and_multiple_elements(self):
        """ Test the ``get_element_number_from_parent```method with a list as parent node. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode)
        parent_tree_node.new_child('li', ListElementTreeNode)
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(2, tree_node.get_element_number_from_parent())
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(3, tree_node.get_element_number_from_parent())

    def test_get_element_number_from_parent_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method without a list as parent node. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual(1, tree_node.get_element_number_from_parent())

    def test_get_list_bullet(self):
        """ Test the ``get_list_bullet`` method. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': UNORDERED_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('-', tree_node.get_list_bullet())
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('1.', tree_node.get_list_bullet())
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': UPPERCASE_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('A.', tree_node.get_list_bullet())
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': LOWERCASE_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('a.', tree_node.get_list_bullet())
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': UPPER_ROMAN_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('I.', tree_node.get_list_bullet())
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': LOWER_ROMAN_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        self.assertEqual('i.', tree_node.get_list_bullet())

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode)
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = '<li>test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        output_result = tree_node.render_text('Foo\nBar')
        expected_result = '1. Foo\n   Bar\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_no_content(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        output_result = tree_node.render_text('')
        expected_result = '1.\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        parent_tree_node = root_tree_node.new_child('list', ListTreeNode, attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', ListElementTreeNode)
        output_result = tree_node.render_text('  Foo\nBar  ')
        expected_result = '1. Foo\n   Bar\n'
        self.assertEqual(expected_result, output_result)
