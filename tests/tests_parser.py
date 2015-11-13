"""
SkCode tag parser test code.
"""

import unittest

from skcode.parser import (WHITESPACE_CHARSET,
                           IDENTIFIER_CHARSET,
                           skip_nb_char_then_whitespaces,
                           get_identifier,
                           get_attribute_value,
                           parse_tag)


class TagParserTestCase(unittest.TestCase):
    """ Tests suite for the ``parse_tag`` function. """

    def test_whitespace_charset_valid(self):
        """ Test if the whitespace charset is valid. """
        self.assertEqual(frozenset(' \t'), WHITESPACE_CHARSET)

    def test_identifier_charset_valid(self):
        """ Test if the identifier charset is valid. """
        self.assertEqual(frozenset('abcdefghijklmnopqrstuvwxyz'
                                   'ABCDEFGHIJKLMNOPQRSTUVWXY'
                                   '0123456789'), IDENTIFIER_CHARSET)

    def test_skip_nb_char_then_whitespaces_with_whitespaces(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method really skip whitespaces at beginning of the string.
        """
        offset, ch = skip_nb_char_then_whitespaces("     abcdef", 0, 0)
        self.assertEqual(offset, 5)
        self.assertEqual('a', ch)

    def test_skip_nb_char_then_whitespaces_without_whitespaces(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method work with a string starting without whitespaces.
        """
        offset, ch = skip_nb_char_then_whitespaces("abcdef", 0, 0)
        self.assertEqual(offset, 0)
        self.assertEqual('a', ch)

    def test_skip_nb_char_then_whitespaces_with_offset(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method skip whitespaces at beginning of the string starting
        at the given offset.
        """
        offset, ch = skip_nb_char_then_whitespaces("xy   abcdef", 2, 0)
        self.assertEqual(offset, 5)
        self.assertEqual('a', ch)

    def test_skip_nb_char_then_whitespaces_with_too_big_offset(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method raise an ``IndexError`` if the offset is greater than the
        size of the input text.
        """
        with self.assertRaises(IndexError):
            skip_nb_char_then_whitespaces("0123456789", 10, 0)

    def test_skip_nb_char_then_whitespaces_with_default_nb_char_to_skip(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method skip any char at beginning of the string if not specified.
        """
        offset, ch = skip_nb_char_then_whitespaces("xy   abcdef", 0)
        self.assertEqual(offset, 0)
        self.assertEqual('x', ch)

    def test_skip_nb_char_then_whitespaces_with_nb_char_to_skip(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method skip the given count of char at beginning of the string.
        """
        offset, ch = skip_nb_char_then_whitespaces("xy   abcdef", 0, 2)
        self.assertEqual(offset, 5)
        self.assertEqual('a', ch)

    def test_skip_nb_char_then_whitespaces_with_nb_char_to_skip_too_big(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method raise an ``IndexError`` if the number of char to be skip
        make the offset greater than the actual size of the input text.
        """
        with self.assertRaises(IndexError):
            skip_nb_char_then_whitespaces("0123456789", 5, 5)

    def test_nb_char_to_skip_with_whitespaces_only(self):
        """
        Test if the ``skip_nb_char_then_whitespaces`` method raise a ``IndexError`` if the string end with whitespaces.
        """
        with self.assertRaises(IndexError):
            skip_nb_char_then_whitespaces("  ", 0, 0)

    # --- Functional tests
    PASS_TESTS = (
        # Test simple opening tag with extra whitespaces
        ('[test]', ('test', False, False, {}, 6)),
        ('[ test]', ('test', False, False, {}, 7)),
        ('[test ]', ('test', False, False, {}, 7)),
        ('[ test ]', ('test', False, False, {}, 8)),

        # Test tag name normalization
        ('[TesT]', ('test', False, False, {}, 6)),

        # Test attribute name normalization
        ('[test kEy=value]', ('test', False, False, {'key': 'value'}, 16)),

        # Test standalone attribute
        ('[test key]', ('test', False, False, {'key': ''}, 10)),

        # Test tag value escape sequence
        ('[test="val\\"ue"]', ('test', False, False, {'test': 'val"ue'}, 16)),
        ('[test=\'val\\\'ue\']', ('test', False, False, {'test': 'val\'ue'}, 16)),

        # Test tag value erroneous escape sequence
        ('[test="val\\\'ue"]', ('test', False, False, {'test': 'val\\\'ue'}, 16)),
        ('[test=\'val\\"ue\']', ('test', False, False, {'test': 'val\\"ue'}, 16)),
        ('[test="val\\nue"]', ('test', False, False, {'test': 'val\\nue'}, 16)),
        ('[test=\'val\\nue\']', ('test', False, False, {'test': 'val\\nue'}, 16)),

        # Test attribute escape sequence
        ('[test key="val\\"ue"]', ('test', False, False, {'key': 'val"ue'}, 20)),
        ('[test key=\'val\\\'ue\']', ('test', False, False, {'key': 'val\'ue'}, 20)),

        # Test attribute erroneous escape sequence
        ('[test key="val\\\'ue"]', ('test', False, False, {'key': 'val\\\'ue'}, 20)),
        ('[test key=\'val\\"ue\']', ('test', False, False, {'key': 'val\\"ue'}, 20)),
        ('[test key="val\\nue"]', ('test', False, False, {'key': 'val\\nue'}, 20)),
        ('[test key=\'val\\nue\']', ('test', False, False, {'key': 'val\\nue'}, 20)),

        # Test simple closing tag with extra whitespaces
        ('[/test]', ('test', True, False, {}, 7)),
        ('[ /test]', ('test', True, False, {}, 8)),
        ('[ / test]', ('test', True, False, {}, 9)),
        ('[/test ]', ('test', True, False, {}, 8)),
        ('[/ test ]', ('test', True, False, {}, 9)),
        ('[ / test ]', ('test', True, False, {}, 10)),

        # Test simple self closing tag with extra whitespaces
        ('[test/]', ('test', False, True, {}, 7)),
        ('[test /]', ('test', False, True, {}, 8)),
        ('[test / ]', ('test', False, True, {}, 9)),
        ('[ test/]', ('test', False, True, {}, 8)),
        ('[ test /]', ('test', False, True, {}, 9)),
        ('[ test / ]', ('test', False, True, {}, 10)),

        # Test simple opening tag with tag value (unquoted)
        ('[test=value]', ('test', False, False, {'test': 'value'}, 12)),
        ('[test =value]', ('test', False, False, {'test': 'value'}, 13)),
        ('[test= value]', ('test', False, False, {'test': 'value'}, 13)),
        ('[test = value]', ('test', False, False, {'test': 'value'}, 14)),

        # Test simple opening tag with tag value (double quoted)
        ('[test="value"]', ('test', False, False, {'test': 'value'}, 14)),
        ('[test ="value"]', ('test', False, False, {'test': 'value'}, 15)),
        ('[test= "value"]', ('test', False, False, {'test': 'value'}, 15)),
        ('[test = "value"]', ('test', False, False, {'test': 'value'}, 16)),

        # Test simple opening tag with tag value (single quoted)
        ('[test=\'value\']', ('test', False, False, {'test': 'value'}, 14)),
        ('[test =\'value\']', ('test', False, False, {'test': 'value'}, 15)),
        ('[test= \'value\']', ('test', False, False, {'test': 'value'}, 15)),
        ('[test = \'value\']', ('test', False, False, {'test': 'value'}, 16)),

        # Test simple self closing tag with tag value (unquoted)
        ('[test=value /]', ('test', False, True, {'test': 'value'}, 14)),
        ('[test =value /]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test= value /]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test = value /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test=value / ]', ('test', False, True, {'test': 'value'}, 15)),
        ('[test =value / ]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test= value / ]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test = value / ]', ('test', False, True, {'test': 'value'}, 17)),

        # Test simple self closing tag with tag value (double quoted)
        ('[test="value" /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test ="value" /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test= "value" /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test = "value" /]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test="value" / ]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test ="value" / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test= "value" / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test = "value" / ]', ('test', False, True, {'test': 'value'}, 19)),

        # Test simple self closing tag with tag value (single quoted)
        ('[test=\'value\' /]', ('test', False, True, {'test': 'value'}, 16)),
        ('[test =\'value\' /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test= \'value\' /]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test = \'value\' /]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test=\'value\' / ]', ('test', False, True, {'test': 'value'}, 17)),
        ('[test =\'value\' / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test= \'value\' / ]', ('test', False, True, {'test': 'value'}, 18)),
        ('[test = \'value\' / ]', ('test', False, True, {'test': 'value'}, 19)),

        # Test simple opening tag with a single attribute (unquoted)
        ('[test key=value]', ('test', False, False, {'key': 'value'}, 16)),
        ('[test key =value]', ('test', False, False, {'key': 'value'}, 17)),
        ('[test key= value]', ('test', False, False, {'key': 'value'}, 17)),
        ('[test key = value]', ('test', False, False, {'key': 'value'}, 18)),

        # Test simple opening tag with a single attribute (double quoted)
        ('[test key="value"]', ('test', False, False, {'key': 'value'}, 18)),
        ('[test key ="value"]', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key= "value"]', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key = "value"]', ('test', False, False, {'key': 'value'}, 20)),

        # Test simple opening tag with a single attribute (single quoted)
        ('[test key=\'value\']', ('test', False, False, {'key': 'value'}, 18)),
        ('[test key =\'value\']', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key= \'value\']', ('test', False, False, {'key': 'value'}, 19)),
        ('[test key = \'value\']', ('test', False, False, {'key': 'value'}, 20)),

        # Test empty attribute quoted value
        ('[test key=""]', ('test', False, False, {'key': ''}, 13)),
        ('[test key=\'\']', ('test', False, False, {'key': ''}, 13)),

        # Test empty tag value quoted value
        ('[test=""]', ('test', False, False, {'test': ''}, 9)),
        ('[test=\'\']', ('test', False, False, {'test': ''}, 9)),

        # Test last unquoted value empty (with error case)
        ('[test=]', ('test', False, False, {'test': ''}, 7)),
        ('[test key=]', ('test', False, False, {'key': ''}, 11)),
        ('[test= key=]', ('test', False, False, {'test': 'key='}, 12)),

        # Test whitespaces strip in attribute quoted values
        ('[test key=" value "]', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key=\' value \']', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key="\tvalue\t"]', ('test', False, False, {'key': 'value'}, 20)),
        ('[test key=\'\tvalue\t\']', ('test', False, False, {'key': 'value'}, 20)),

        # Test simple opening tag with tag value (unquoted) and a single attribute
        ('[test=value key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 22)),
        ('[test=value key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test=value key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),

        # Test simple opening tag with tag value (double quoted) and a single attribute
        ('[test="value" key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test="value" key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),
        ('[test="value" key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),

        # Test simple opening tag with tag value (single quoted) and a single attribute
        ('[test=\'value\' key=value]', ('test', False, False, {'test': 'value', 'key': 'value'}, 24)),
        ('[test=\'value\' key="value"]', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),
        ('[test=\'value\' key=\'value\']', ('test', False, False, {'test': 'value', 'key': 'value'}, 26)),

        # Test simple opening tag with tag value (unquoted) and multiple attributes
        ('[test=value key=value key2=value2]', ('test', False, False,
                                                {'test': 'value', 'key': 'value', 'key2': 'value2'}, 34)),
        ('[test=value key="value" key2="value2"]', ('test', False, False,
                                                    {'test': 'value', 'key': 'value', 'key2': 'value2'}, 38)),
        ('[test=value key=\'value\' key2=\'value2\']', ('test', False, False,
                                                        {'test': 'value', 'key': 'value', 'key2': 'value2'}, 38)),

        # Test simple opening tag with tag value (double quoted) and multiple attributes
        ('[test="value" key=value key2=value2]', ('test', False, False,
                                                  {'test': 'value', 'key': 'value', 'key2': 'value2'}, 36)),
        ('[test="value" key="value" key2="value2"]', ('test', False, False,
                                                      {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),
        ('[test="value" key=\'value\' key2=\'value2\']', ('test', False, False,
                                                          {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),

        # Test simple opening tag with tag value (single quoted) and multiple attributes
        ('[test=\'value\' key=value key2=value2]', ('test', False, False,
                                                    {'test': 'value', 'key': 'value', 'key2': 'value2'}, 36)),
        ('[test=\'value\' key="value" key2="value2"]', ('test', False, False,
                                                        {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),
        ('[test=\'value\' key=\'value\' key2=\'value2\']', ('test', False, False,
                                                            {'test': 'value', 'key': 'value', 'key2': 'value2'}, 40)),

        # Test simple opening tag with unquoted value ending with slash at end of the tag attrs
        ('[test=http://example.com/]', ('test', False, False, {'test': 'http://example.com/'}, 26)),
        ('[test url=http://example.com/]', ('test', False, False, {'url': 'http://example.com/'}, 30)),
    )

    # --- Error handling tests
    FAIL_TESTS = (
        # Opening tag without end
        ('[', IndexError),
        ('[ ', IndexError),
        ('[/', IndexError),
        ('[/ ', IndexError),
        ('[ /', IndexError),
        ('[ / ', IndexError),

        # Opening tag without name
        ('[[', ValueError),
        ('[]', ValueError),
        ('[/]', ValueError),
        ('[#', ValueError),
        ('["', ValueError),

        # Opening tag without end after tag name
        ('[test', IndexError),
        ('[test ', IndexError),

        # Closing tag with arguments
        ('[/test=value]', ValueError),
        ('[/test =value]', ValueError),
        ('[/test= value]', ValueError),
        ('[/test = value]', ValueError),
        ('[/test key=value]', ValueError),

        # Opening tag without end after attribute value
        ('[test=', IndexError),
        ('[test= ', IndexError),
        ('[test="', IndexError),
        ('[test="aaa', IndexError),
        ('[test="a\\', IndexError),
        ('[test=""', IndexError),

        # Opening tag without space between attribute names
        ('[test=""a', ValueError),
        ('[test=\'\'a', ValueError),

        # Opening tag without end after tag value
        ('[test=a', IndexError),
        ('[test=a ', IndexError),

        # Opening tag without end after attribute name or value
        ('[test key', IndexError),
        ('[test key ', IndexError),
        ('[test key=', IndexError),
        ('[test key= ', IndexError),
        ('[test key=a', IndexError),
        ('[test key=a ', IndexError),

        # Opening tag with erroneous attribute name
        ('[test key=value =value', ValueError),
        ('[test key=value #=value ', ValueError),

        # Opening tag without end after attribute value
        ('[test key=', IndexError),
        ('[test key= ', IndexError),
        ('[test key="', IndexError),
        ('[test key="aaa', IndexError),
        ('[test key="a\\', IndexError),
        ('[test key=""', IndexError),

        # Opening tag without space between attribute names
        ('[test key=""a', ValueError),
        ('[test key=\'\'a', ValueError),

        # Opening tag without end after final slash
        ('[test /', IndexError),
        ('[test / ', IndexError),
        ('[test />', ValueError),

        # Malformed self closing tag
        ('[/test /]', ValueError),
    )

    def test_functional(self):
        """ Functional tests. """
        for text, excepted_result in self.PASS_TESTS:
            result = parse_tag(text, 0, opening_tag_ch='[', closing_tag_ch=']')
            self.assertEqual(result, excepted_result, msg=text)

    def test_error(self):
        """ Error handling tests. """
        for text, excepted_exception in self.FAIL_TESTS:
            try:
                with self.assertRaises(excepted_exception, msg=text):
                    parse_tag(text, 0, opening_tag_ch='[', closing_tag_ch=']')
            except:
                print('Exception during test:', text)
                raise


# Run test suite
if __name__ == '__main__':
    unittest.main()
