"""
SkCode relative URLs utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.utility.relative_urls import (
    setup_relative_urls_conversion,
    get_relative_url_base,
    RELATIVE_URL_BASE_ATTR_NAME
)


class RelativeUrlsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the relative URLs utility module. """

    def test_setup_relative_urls_conversion(self):
        """ Test the ``setup_relative_urls_conversion`` helper. """
        document_tree = RootTreeNode()
        self.assertNotIn(RELATIVE_URL_BASE_ATTR_NAME, document_tree.attrs)
        setup_relative_urls_conversion(document_tree, 'http://example.com/')
        self.assertIn(RELATIVE_URL_BASE_ATTR_NAME, document_tree.attrs)
        self.assertEqual('http://example.com/', document_tree.attrs[RELATIVE_URL_BASE_ATTR_NAME])

    def test_get_relative_url_base(self):
        """ Test the ``get_relative_url_base`` helper. """
        document_tree = RootTreeNode()
        setup_relative_urls_conversion(document_tree, 'http://example.com/')
        base_url = get_relative_url_base(document_tree)
        self.assertEqual('http://example.com/', base_url)
