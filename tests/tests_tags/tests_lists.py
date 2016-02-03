"""
SkCode lists tag test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         ListTagOptions,
                         ListElementTagOptions,
                         OrderedListTagOptions,
                         UnorderedListTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)
from skcode.tags.lists import (UNORDERED_LIST_TYPE,
                               NUMERIC_LIST_TYPE,
                               UPPERCASE_LIST_TYPE,
                               LOWERCASE_LIST_TYPE,
                               UPPER_ROMAN_LIST_TYPE,
                               LOWER_ROMAN_LIST_TYPE,
                               ROMAN_NUMERALS,
                               ALPHABET_NUMERALS,
                               int_to_alphabet_numerals,
                               int_to_roman_numerals)


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
        self.assertIn('list', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['list'], ListTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ListTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)

        self.assertEqual((
            UNORDERED_LIST_TYPE,
            NUMERIC_LIST_TYPE,
            UPPERCASE_LIST_TYPE,
            LOWERCASE_LIST_TYPE,
            UPPER_ROMAN_LIST_TYPE,
            LOWER_ROMAN_LIST_TYPE,
        ), opts.allowed_list_types)
        self.assertEqual(UNORDERED_LIST_TYPE, opts.default_list_type)
        self.assertEqual('type', opts.list_type_attr_name)
        self.assertEqual('start', opts.list_start_number_attr_name)
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
        }, opts.list_type_alias)
        self.assertEqual({
            NUMERIC_LIST_TYPE: '1',
            UPPERCASE_LIST_TYPE: 'A',
            LOWERCASE_LIST_TYPE: 'a',
            UPPER_ROMAN_LIST_TYPE: 'I',
            LOWER_ROMAN_LIST_TYPE: 'i',
        }, opts.html_list_type_lut)
        self.assertEqual({
            UNORDERED_LIST_TYPE: '',
            NUMERIC_LIST_TYPE: '1',
            UPPERCASE_LIST_TYPE: 'A',
            LOWERCASE_LIST_TYPE: 'a',
            UPPER_ROMAN_LIST_TYPE: 'I',
            LOWER_ROMAN_LIST_TYPE: 'i',
        }, opts.alias_list_type_lut)

    def test_get_list_type_with_tagname_set(self):
        """ Test the ``get_list_type`` method with the tag name set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'list': 'numeric'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_type_attr_set(self):
        """ Test the ``get_list_type`` method with the type attribute set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': 'numeric'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_tagname_and_type_attr_set(self):
        """ Test the ``get_list_type`` method with the tag name and type attribute set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'list': '1', 'type': 'A'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_no_type_set(self):
        """ Test the ``get_list_type`` method with no type set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)

    def test_get_list_type_alias_type(self):
        """ Test the ``get_list_type`` method with an type name alias set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': '1'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_with_type_uppercase(self):
        """ Test the ``get_list_type`` method with an type name set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': 'numeRIC'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(NUMERIC_LIST_TYPE, output_result)

    def test_get_list_type_invalid_type(self):
        """ Test the ``get_list_type`` method with an invalid type name set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': 'test'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)

    def test_get_list_first_number_with_number(self):
        """ Test the ``get_list_first_number`` method with a positive number. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'start': '3'})
        output_result = opts.get_list_first_number(tree_node)
        self.assertEqual(3, output_result)

    def test_get_list_first_number_with_non_number(self):
        """ Test the ``get_list_first_number`` method with a non number value. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'start': 'abcd'})
        output_result = opts.get_list_first_number(tree_node)
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_negative_number(self):
        """ Test the ``get_list_first_number`` method with a negative number. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'start': '-3'})
        output_result = opts.get_list_first_number(tree_node)
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_zero(self):
        """ Test the ``get_list_first_number`` method with zero. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'start': '0'})
        output_result = opts.get_list_first_number(tree_node)
        self.assertEqual(1, output_result)

    def test_get_list_first_number_with_no_value(self):
        """ Test the ``get_list_first_number`` method with no value set. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'start': ''})
        output_result = opts.get_list_first_number(tree_node)
        self.assertEqual(1, output_result)

    def test_render_html_unordered(self):
        """ Test the ``render_html`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<ul>test</ul>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_ordered(self):
        """ Test the ``render_html`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': '1'})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<ol type="1">test</ol>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_html_ordered_with_start_number(self):
        """ Test the ``render_html`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': '1', 'start': '3'})
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<ol type="1" start="3">test</ol>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts)
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for list_type in opts.allowed_list_types:
            tree_node = root_tree_node.new_child('list', opts, attrs={'type': list_type})
            output_result = opts.get_skcode_attributes(tree_node, 'test')
            expected_result = ({'type': opts.alias_list_type_lut[list_type]}, 'type')
            self.assertEqual(expected_result, output_result)

    def test_get_skcode_non_ignored_empty_attributes(self):
        """ Test the ``get_skcode_non_ignored_empty_attributes`` method. """
        opts = ListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts)
        output_result = opts.get_skcode_non_ignored_empty_attributes(tree_node, 'test')
        expected_result = ('type', )
        self.assertEqual(expected_result, output_result)


class UnorderedListsTagTestCase(unittest.TestCase):
    """ Tests suite for the unordered lists tag module. """

    def test_subclassing(self):
        """ Test the modules constants """
        self.assertTrue(issubclass(UnorderedListTagOptions, ListTagOptions))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('ul', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ul'], UnorderedListTagOptions)

    def test_get_list_type(self):
        """ Test the ``get_list_type`` method. """
        opts = UnorderedListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'list': 'numeric'})
        output_result = opts.get_list_type(tree_node)
        self.assertEqual(UNORDERED_LIST_TYPE, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = UnorderedListTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('list', opts, attrs={'type': 'numeric'})
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({}, None)
        self.assertEqual(expected_result, output_result)


class OrderedListsTagTestCase(unittest.TestCase):
    """ Tests suite for the ordered lists tag module. """

    def test_subclassing(self):
        """ Test the modules constants """
        self.assertTrue(issubclass(OrderedListTagOptions, ListTagOptions))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('ol', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['ol'], OrderedListTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = OrderedListTagOptions()
        self.assertEqual((
            NUMERIC_LIST_TYPE,
            UPPERCASE_LIST_TYPE,
            LOWERCASE_LIST_TYPE,
            UPPER_ROMAN_LIST_TYPE,
            LOWER_ROMAN_LIST_TYPE,
        ), opts.allowed_list_types)
        self.assertEqual(NUMERIC_LIST_TYPE, opts.default_list_type)


class ListElementTagTestCase(unittest.TestCase):
    """ Tests suite for the list elements tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('li', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['li'], ListElementTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ListElementTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual(UNORDERED_LIST_TYPE, opts.default_list_type)
        self.assertEqual(ListTagOptions, opts.base_list_class)

    def test_get_parent_list_type_assertion(self):
        """ Test the ``get_parent_list_type```method assertions. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        with self.assertRaises(AssertionError) as e:
            opts.get_parent_list_type(root_tree_node)
        self.assertEqual('A list element cannot be a root tree node.', str(e.exception))

    def test_get_parent_list_type_with_list_as_parent(self):
        """ Test the ``get_parent_list_type```method with a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': 'numeric'})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual(NUMERIC_LIST_TYPE, opts.get_parent_list_type(tree_node))

    def test_get_parent_list_type_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_type```method without a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('li', opts)
        self.assertEqual(UNORDERED_LIST_TYPE, opts.get_parent_list_type(tree_node))

    def test_get_parent_list_first_number_assertion(self):
        """ Test the ``get_parent_list_first_number```method assertions. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        with self.assertRaises(AssertionError) as e:
            opts.get_parent_list_first_number(root_tree_node)
        self.assertEqual('A list element cannot be a root tree node.', str(e.exception))

    def test_get_parent_list_first_number_with_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method with a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'start': '5'})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual(5, opts.get_parent_list_first_number(tree_node))

    def test_get_parent_list_first_number_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method without a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('li', opts)
        self.assertEqual(1, opts.get_parent_list_first_number(tree_node))

    def test_get_element_number_from_parent_assertion(self):
        """ Test the ``get_element_number_from_parent```method assertions. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        with self.assertRaises(AssertionError) as e:
            opts.get_element_number_from_parent(root_tree_node)
        self.assertEqual('A list element cannot be a root tree node.', str(e.exception))

    def test_get_element_number_from_parent_with_list_as_parent(self):
        """ Test the ``get_element_number_from_parent```method with a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions())
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual(1, opts.get_element_number_from_parent(tree_node))

    def test_get_element_number_from_parent_with_list_as_parent_and_multiple_elements(self):
        """ Test the ``get_element_number_from_parent```method with a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions())
        parent_tree_node.new_child('li', opts)
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual(2, opts.get_element_number_from_parent(tree_node))
        tree_node = parent_tree_node.new_child('li', opts)
        parent_tree_node.new_child('li', opts)
        self.assertEqual(3, opts.get_element_number_from_parent(tree_node))

    def test_get_element_number_from_parent_with_non_list_as_parent(self):
        """ Test the ``get_parent_list_first_number```method without a list as parent node. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('li', opts)
        self.assertEqual(1, opts.get_element_number_from_parent(tree_node))

    def test_get_list_bullet(self):
        """ Test the ``get_list_bullet`` method. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': UNORDERED_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('-', opts.get_list_bullet(tree_node))

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('1.', opts.get_list_bullet(tree_node))

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': UPPERCASE_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('A.', opts.get_list_bullet(tree_node))

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': LOWERCASE_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('a.', opts.get_list_bullet(tree_node))

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': UPPER_ROMAN_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('I.', opts.get_list_bullet(tree_node))

        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': LOWER_ROMAN_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        self.assertEqual('i.', opts.get_list_bullet(tree_node))

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions())
        tree_node = parent_tree_node.new_child('li', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<li>test</li>\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        output_result = opts.render_text(tree_node, 'Foo\nBar')
        expected_result = '1. Foo\n   Bar\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_no_content(self):
        """ Test the ``render_text`` method. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        output_result = opts.render_text(tree_node, '')
        expected_result = '1.\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_trailing_whitespaces(self):
        """ Test the ``render_text`` method. """
        opts = ListElementTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        parent_tree_node = root_tree_node.new_child('list', ListTagOptions(), attrs={'type': NUMERIC_LIST_TYPE})
        tree_node = parent_tree_node.new_child('li', opts)
        output_result = opts.render_text(tree_node, '  Foo\nBar  ')
        expected_result = '1. Foo\n   Bar\n'
        self.assertEqual(expected_result, output_result)
