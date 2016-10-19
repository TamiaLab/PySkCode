"""
SkCode tools test code.
"""

import unittest

from skcode.tools import (
    escape_attribute_value,
    sanitize_url,
    slugify
)


class ToolsTestCase(unittest.TestCase):
    """ Test suite for the tools module. """

    def test_escape_attr_value_with_single_quote(self):
        """ Test the ``escape_attribute_value`` method with a string containing a single quote. """
        output = escape_attribute_value("test'test")
        self.assertEqual('"test\'test"', output)

    def test_escape_attr_value_with_double_quote(self):
        """ Test the ``escape_attribute_value`` method with a string containing a double quote. """
        output = escape_attribute_value('test"test')
        self.assertEqual("'test\"test'", output)

    def test_escape_attr_value_with_single_and_double_quotes(self):
        """ Test the ``escape_attribute_value`` method with a string containing a single and a double quote. """
        output = escape_attribute_value("""test'test"test""")
        self.assertEqual('"test\'test\\"test"', output)

    def test_escape_attr_value_with_single_and_double_quotes_and_backslash(self):
        """ Test the ``escape_attribute_value`` method with a string containing a single and a double quote. """
        output = escape_attribute_value("""test'test\\"test""")
        self.assertEqual('"test\'test\\\\\\"test"', output)

    def test_escape_attr_value_with_no_quote(self):
        """ Test the ``escape_attribute_value`` method with a string containing no quote. """
        output = escape_attribute_value('test')
        self.assertEqual('"test"', output)

    def test_sanitize_url_assertions(self):
        """ Test the assertions of the ``sanitize_url`` method. """
        with self.assertRaises(AssertionError) as e:
            sanitize_url('https://github.com/TamiaLab/PySkCode', default_scheme='')
        self.assertEqual('A default scheme is mandatory to avoid XSS.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            sanitize_url('https://github.com/TamiaLab/PySkCode', allowed_schemes=())
        self.assertEqual('You need to allow at least one scheme to get a result.', str(e.exception))

        with self.assertRaises(AssertionError) as e:
            sanitize_url('https://github.com/TamiaLab/PySkCode',
                         force_default_scheme=True, force_remove_scheme=True)
        self.assertEqual('You cannot force the default scheme and also force-remove the scheme.', str(e.exception))

    def test_sanitize_url(self):
        """ Test the ``sanitize_url`` method with a valid URL. """
        output = sanitize_url('https://github.com/TamiaLab/PySkCode')
        self.assertEqual('https://github.com/TamiaLab/PySkCode', output)

    def test_sanitize_url_ipv6(self):
        """ Test the ``sanitize_url`` method with a valid URL (using a IPv6 address). """
        output = sanitize_url('https://[2001:db8:85a3:8d3:1319:8a2e:370:7348]:443/')
        self.assertEqual('https://[2001:db8:85a3:8d3:1319:8a2e:370:7348]:443/', output)

    def test_sanitize_url_with_no_url(self):
        """ Test the ``sanitize_url`` method without any URL. """
        output = sanitize_url('')
        self.assertEqual('', output)

    def test_sanitize_url_with_dangerous_char(self):
        """ Test the ``sanitize_url`` method with an URL containing dangerous char inside. """
        output = sanitize_url('{https}://github.com/<TamiaLab>/PySkCode')
        self.assertEqual('https://github.com/TamiaLab/PySkCode', output)

    def test_sanitize_url_with_malformed_url(self):
        """ Test the ``sanitize_url`` method with a malformed URL. """
        output = sanitize_url('https://[github.com/TamiaLab/PySkCode')
        self.assertEqual('', output)

    def test_sanitize_url_with_scheme_not_in_white_list(self):
        """ Test the ``sanitize_url`` method with an URL and a scheme not in white list. """
        output = sanitize_url('https://github.com/TamiaLab/PySkCode', allowed_schemes=('http',))
        self.assertEqual('', output)

    def test_sanitize_url_with_local_url_without_scheme(self):
        """ Test the ``sanitize_url`` method with a local URL without a scheme. """
        output = sanitize_url('/TamiaLab/PySkCode', default_scheme='https')
        self.assertEqual('/TamiaLab/PySkCode', output)

    def test_sanitize_url_with_non_local_url_without_scheme(self):
        """ Test the ``sanitize_url`` method with a non local URL and without a scheme. """
        output = sanitize_url('github.com/TamiaLab/PySkCode', default_scheme='https')
        self.assertEqual('https://github.com/TamiaLab/PySkCode', output)

    def test_sanitize_url_with_non_local_url_without_scheme_disabled(self):
        """ Test the ``sanitize_url`` method with a non local URL and without a scheme. """
        output = sanitize_url('github.com/TamiaLab/PySkCode', default_scheme='https', fix_non_local_urls=False)
        self.assertEqual('github.com/TamiaLab/PySkCode', output)

    def test_sanitize_url_with_only_domain_name(self):
        """ Test the ``sanitize_url`` method with onyl a domain name. """
        output = sanitize_url('github.com', default_scheme='https')
        self.assertEqual('https://github.com', output)

    def test_sanitize_url_with_force_default_scheme(self):
        """ Test the ``sanitize_url`` method with a local URL without a scheme but with force_default_scheme set. """
        output = sanitize_url('/TamiaLab/PySkCode', default_scheme='https', force_default_scheme=True)
        self.assertEqual('https:///TamiaLab/PySkCode', output)

    def test_sanitize_url_with_force_remove_scheme(self):
        """ Test the ``sanitize_url`` method with a valid URL and the force_remove_scheme set. """
        output = sanitize_url('https://github.com/TamiaLab/PySkCode', force_remove_scheme=True)
        self.assertEqual('//github.com/TamiaLab/PySkCode', output)

    def test_sanitize_url_with_html_entities(self):
        """ Test the ``sanitize_url`` method with an URL containing HTML entities char inside. """
        output = sanitize_url("https://github.com/TamiaLab/PySkCode?foo=bar&bar=foo")
        self.assertEqual('https://github.com/TamiaLab/PySkCode?foo=bar&amp;bar=foo', output)

    def test_sanitize_url_with_html_entities_escape_disabled(self):
        """ Test the ``sanitize_url`` method with an URL containing HTML entities char inside. """
        output = sanitize_url("https://github.com/TamiaLab/PySkCode?foo=bar&bar=foo", encode_html_entities=False)
        self.assertEqual('https://github.com/TamiaLab/PySkCode?foo=bar&bar=foo', output)

    def test_sanitize_url_with_javascript_xss(self):
        """ Test the ``sanitize_url`` method with a classic ``javascript:`` XSS injection. """
        self.assertEqual('', sanitize_url("javascript:alert('XSS');"))
        self.assertEqual('', sanitize_url("jav\tascript:alert('XSS');"))

    def test_sanitize_url_with_data_xss(self):
        """ Test the ``sanitize_url`` method with a classic ``data:`` XSS injection. """
        output = sanitize_url("data:image/png;base64,iVBORw0KGgoAA"
                              "AANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0l"
                              "EQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6"
                              "P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC")
        self.assertEqual('', output)

    def test_sanitize_url_with_local_url_absolute_conversion(self):
        """ Test the ``sanitize_url`` method with a local URL without a scheme and absolute conversion set. """
        output = sanitize_url('/TamiaLab/PySkCode',
                              absolute_base_url='https://github.com')
        self.assertEqual('https://github.com/TamiaLab/PySkCode', output)

    def test_slugify_no_value(self):
        """ Test the ``slugify`` method without value. """
        output = slugify('')
        self.assertEqual('', output)

    def test_slugify_no_value_trailing_whitespaces(self):
        """ Test the ``slugify`` method without value. """
        output = slugify('      ')
        self.assertEqual('', output)

    def test_slugify(self):
        """ Test the ``slugify`` method. """

        # Cloned from Django tests suite
        output = slugify(' Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/')
        self.assertEqual('jack-jill-like-numbers-123-and-4-and-silly-characters', output)

        output = slugify("Un \xe9l\xe9phant \xe0 l'or\xe9e du bois")
        self.assertEqual('un-elephant-a-loree-du-bois', output)
