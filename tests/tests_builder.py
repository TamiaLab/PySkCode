"""
SkCode tag building test code.
"""

import unittest
from unittest import mock

from skcode.builder import build_tag_str


class BuilderTagStringTestCase(unittest.TestCase):
    """ Tests suite for the tag builder function. """

    def test_build_tag_str_assertions(self):
        """ Test the assertions of the ``build_tag_str`` function. """
        with self.assertRaises(AssertionError) as e:
            build_tag_str('')
        self.assertEqual('The tag name is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            build_tag_str('test', opening_tag_ch='')
        self.assertEqual('The opening tag character is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            build_tag_str('test', opening_tag_ch='{{')
        self.assertEqual('Opening tag character must be one char long exactly.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            build_tag_str('test', closing_tag_ch='')
        self.assertEqual('The closing tag character is mandatory.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            build_tag_str('test', closing_tag_ch='}}')
        self.assertEqual('Closing tag character must be one char long exactly.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            build_tag_str('test', standalone=True, content='Foobar')
        self.assertEqual('Standalone tags cannot have content.', str(e.exception))

    def test_simple_tag(self):
        """ Test the ``build_tag_str`` function with a simple tag."""
        output = build_tag_str('test')
        self.assertEqual('[test][/test]', output)

    def test_standalone_tag(self):
        """ Test the ``build_tag_str`` function with a standalone tag."""
        output = build_tag_str('test', standalone=True)
        self.assertEqual('[test]', output)

    def test_custom_open_close_char(self):
        """ Test the ``build_tag_str`` function with a simple tag but with custom open/close characters."""
        output = build_tag_str('test', opening_tag_ch='<', closing_tag_ch='>')
        self.assertEqual('<test></test>', output)

    def test_simple_tag_with_attributes(self):
        """ Test the ``build_tag_str`` function with a tag with attributes."""
        output = build_tag_str('test', attrs={'foo': 'bar'})
        self.assertEqual('[test foo="bar"][/test]', output)

    def test_escape_attr_value(self):
        """ Test the ``build_tag_str`` function escape attributes values. """
        with mock.patch('skcode.builder.escape_attrvalue') as mock_escape_attrvalue:
            mock_escape_attrvalue.return_value = 'bar'
            build_tag_str('test', attrs={'foo': 'bar'})
        mock_escape_attrvalue.assert_called_once_with('bar')

    def test_ignore_empty_attributes(self):
        """ Test the ``build_tag_str`` function with a empty attributes."""
        output = build_tag_str('test', attrs={'foo': '', 'bar': ''})
        self.assertEqual('[test][/test]', output)

    def test_non_ignored_empty_attributes(self):
        """ Test the ``build_tag_str`` function with a non-ignored empty attributes."""
        output = build_tag_str('test', attrs={'test': '', 'foo': '', 'bar': ''}, non_ignored_empty_attrs=('bar', ))
        self.assertEqual('[test bar=""][/test]', output)

    def test_non_ignored_empty_attributes_tagvalue(self):
        """ Test the ``build_tag_str`` function with a non-ignored empty tag value."""
        output = build_tag_str('test', attrs={'test': '', 'foo': '', 'bar': ''}, non_ignored_empty_attrs=('test', ))
        self.assertEqual('[test=""][/test]', output)

    def test_standalone_attributes(self):
        """ Test the ``build_tag_str`` function with a standalone tag."""
        output = build_tag_str('test', attrs={'foo': None}, non_ignored_empty_attrs=('test', ))
        self.assertEqual('[test foo][/test]', output)

    def test_tagvalue(self):
        """ Test the ``build_tag_str`` function with a simple tag with a tag value."""
        output = build_tag_str('test', attrs={'test': 'foobar'})
        self.assertEqual('[test="foobar"][/test]', output)
        output = build_tag_str('test', attrs={'test': 'foobar'}, allow_tagvalue_attr=False)
        self.assertEqual('[test test="foobar"][/test]', output)

    def test_tagvalue_custom_attr_name(self):
        """ Test the ``build_tag_str`` function with a tag with a tag value not named like the tag name."""
        output = build_tag_str('test', attrs={'foo': 'bar'}, tagvalue_attr_name='foo')
        self.assertEqual('[test="bar"][/test]', output)
