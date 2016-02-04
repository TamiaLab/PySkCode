"""
SkCode tag parser test code.
"""

import unittest

from skcode.tokenizer import (tokenize_tag,
                              TOKEN_DATA,
                              TOKEN_NEWLINE,
                              TOKEN_OPEN_TAG,
                              TOKEN_CLOSE_TAG,
                              TOKEN_SELF_CLOSE_TAG)


class TokenizerTestCase(unittest.TestCase):
    """ Tests suite for the ``tokenize_tag`` function. """

    PASS_TESTS = (
        # Raw text without tag
        ('raw text', ((TOKEN_DATA, None, None, 'raw text'),)),

        # One valid opening tag
        ('[test]', ((TOKEN_OPEN_TAG, 'test', {}, '[test]'),)),

        # One valid closing tag
        ('[/test]', ((TOKEN_CLOSE_TAG, 'test', {}, '[/test]'),)),

        # One valid self closing tag
        ('[test/]', ((TOKEN_SELF_CLOSE_TAG, 'test', {}, '[test/]'),)),

        # One tag with raw text before
        ('azerty[test]', ((TOKEN_DATA, None, None, 'azerty'),
                          (TOKEN_OPEN_TAG, 'test', {}, '[test]'),)),

        # One tag with raw text before and after
        ('azerty[test]qwerty', ((TOKEN_DATA, None, None, 'azerty'),
                                (TOKEN_OPEN_TAG, 'test', {}, '[test]'),
                                (TOKEN_DATA, None, None, 'qwerty'),)),

        # Two tags with raw text between
        ('[foobar]azerty[test]', ((TOKEN_OPEN_TAG, 'foobar', {}, '[foobar]'),
                                  (TOKEN_DATA, None, None, 'azerty'),
                                  (TOKEN_OPEN_TAG, 'test', {}, '[test]'),)),

        # Two tags with raw text before, between and after
        ('omgwtfbbq[foobar]azerty[test]qwerty', ((TOKEN_DATA, None, None, 'omgwtfbbq'),
                                                 (TOKEN_OPEN_TAG, 'foobar', {}, '[foobar]'),
                                                 (TOKEN_DATA, None, None, 'azerty'),
                                                 (TOKEN_OPEN_TAG, 'test', {}, '[test]'),
                                                 (TOKEN_DATA, None, None, 'qwerty'),)),

        # Test newline tokenizing
        ('raw\ntext', ((TOKEN_DATA, None, None, 'raw'),
                       (TOKEN_NEWLINE, None, None, '\n'),
                       (TOKEN_DATA, None, None, 'text'),)),
        ('raw\r\ntext', ((TOKEN_DATA, None, None, 'raw'),
                         (TOKEN_NEWLINE, None, None, '\n'),
                         (TOKEN_DATA, None, None, 'text'),)),
        ('raw\rtext', ((TOKEN_DATA, None, None, 'raw'),
                       (TOKEN_NEWLINE, None, None, '\n'),
                       (TOKEN_DATA, None, None, 'text'),)),

        # Test bad tag handling
        ('[foobar[test]', ((TOKEN_DATA, None, None, '[foobar'),
                           (TOKEN_OPEN_TAG, 'test', {}, '[test]'),)),
    )

    def test_functional(self):
        """ Functional tests. """
        for text, excepted_result in self.PASS_TESTS:
            result = tuple(tokenize_tag(text, opening_tag_ch='[', closing_tag_ch=']'))
            self.assertEqual(result, excepted_result, msg=text)
