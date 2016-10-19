"""
SkCode emoticons replacement utility test code.
"""

import unittest
from html import escape as escape_html

from skcode.etree import RootTreeNode
from skcode.tags import TextTreeNode
from skcode.utility.smileys import (
    setup_smileys_replacement,
    do_smileys_replacement,
    DEFAULT_EMOTICONS_MAP,
    EMOTICONS_MAP_ATTR_NAME,
    EMOTICONS_REGEX_ATTR_NAME,
    EMOTICONS_BASE_URL_ATTR_NAME,
    EMOTICONS_HTML_CLASS_ATTR_NAME
)


class EmoticonsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the emoticons utility module. """

    def test_setup_smileys_replacement(self):
        """ Test the ``setup_smileys_replacement`` helper. """
        document_tree = RootTreeNode()
        self.assertNotIn(EMOTICONS_MAP_ATTR_NAME, document_tree.attrs)
        self.assertNotIn(EMOTICONS_REGEX_ATTR_NAME, document_tree.attrs)
        self.assertNotIn(EMOTICONS_BASE_URL_ATTR_NAME, document_tree.attrs)
        self.assertNotIn(EMOTICONS_HTML_CLASS_ATTR_NAME, document_tree.attrs)
        setup_smileys_replacement(document_tree, 'http://example.com/', (
            (':)', 'smile.png'),
            (':<test?:', 'test.png'),
        ), 'custom_css')
        self.assertIn(EMOTICONS_MAP_ATTR_NAME, document_tree.attrs)
        self.assertEqual({
            ':)': 'smile.png',
            ':&lt;test?:': 'test.png'
        }, document_tree.attrs[EMOTICONS_MAP_ATTR_NAME])
        self.assertIn(EMOTICONS_REGEX_ATTR_NAME, document_tree.attrs)
        self.assertEqual(r"re.compile('(^|\\s+)(?P<emoticon>\\:\\)|\\:\\&lt\\;test\\?\\:)(\\s+|$)')",
                         str(document_tree.attrs[EMOTICONS_REGEX_ATTR_NAME]))
        self.assertIn(EMOTICONS_BASE_URL_ATTR_NAME, document_tree.attrs)
        self.assertEqual('http://example.com/test.png', document_tree.attrs[EMOTICONS_BASE_URL_ATTR_NAME]('test.png'))
        self.assertIn(EMOTICONS_HTML_CLASS_ATTR_NAME, document_tree.attrs)
        self.assertEqual('custom_css', document_tree.attrs[EMOTICONS_HTML_CLASS_ATTR_NAME])

    def test_setup_smileys_replacement_trailing_slash_base_url(self):
        """ Test the ``setup_smileys_replacement`` helper. """
        document_tree = RootTreeNode()
        setup_smileys_replacement(document_tree, 'http://example.com')
        self.assertEqual('http://example.com/test.png', document_tree.attrs[EMOTICONS_BASE_URL_ATTR_NAME]('test.png'))

    def test_setup_smileys_replacement_callable_base_url(self):
        """ Test the ``setup_smileys_replacement`` helper. """
        document_tree = RootTreeNode()
        setup_smileys_replacement(document_tree, lambda x: 'http://example.com/lambda/' + x)
        self.assertEqual('http://example.com/lambda/test.png',
                         document_tree.attrs[EMOTICONS_BASE_URL_ATTR_NAME]('test.png'))

    def test_do_smileys_replacement_no_input(self):
        """ Test the ``do_smileys_replacement`` function. """
        root_tree_node = RootTreeNode()
        output = do_smileys_replacement(root_tree_node, '')
        self.assertEqual('', output)

    def test_do_smileys_replacement_no_setup(self):
        """ Test the ``do_smileys_replacement`` function. """
        root_tree_node = RootTreeNode()
        output = do_smileys_replacement(root_tree_node, 'Test :)')
        self.assertEqual('Test :)', output)

    def test_do_smileys_replacement(self):
        """ Test the ``do_smileys_replacement`` function. """
        root_tree_node = RootTreeNode()
        setup_smileys_replacement(root_tree_node, '/smiley/', html_class='custom_css')
        for smiley, filename in DEFAULT_EMOTICONS_MAP:
            smiley = escape_html(smiley)
            output = do_smileys_replacement(root_tree_node, 'Foo %s bar' % smiley)
            self.assertEqual('Foo <img src="/smiley/%s" alt="%s" class="custom_css"> bar' % (filename, smiley), output)

    def test_do_smileys_replacement_no_css_class(self):
        """ Test the ``do_smileys_replacement`` function. """
        root_tree_node = RootTreeNode()
        setup_smileys_replacement(root_tree_node, '/smiley/', html_class='')
        for smiley, filename in DEFAULT_EMOTICONS_MAP:
            smiley = escape_html(smiley)
            output = do_smileys_replacement(root_tree_node, 'Foo %s bar' % smiley)
            self.assertEqual('Foo <img src="/smiley/%s" alt="%s"> bar' % (filename, smiley), output)

    def test_do_smileys_replacement_text(self):
        """ Test the ``do_smileys_replacement`` function. """
        root_tree_node = RootTreeNode()
        setup_smileys_replacement(root_tree_node, '/smiley/', html_class='')
        tree_node = root_tree_node.new_child(None, TextTreeNode, content='Test :)')
        output = tree_node.render_html('')
        self.assertEqual('Test <img src="/smiley/smile.png" alt=":)">', output)
        output = tree_node.render_text('')
        self.assertEqual('Test :)', output)

    def test_do_smileys_replacement_internal_error(self):
        """ Test the ``do_smileys_replacement`` function when the internal emoticons map is corrupted. """
        root_tree_node = RootTreeNode()
        setup_smileys_replacement(root_tree_node, '/smiley/', html_class='')
        root_tree_node.attrs[EMOTICONS_MAP_ATTR_NAME].pop('&lt;3')
        tree_node = root_tree_node.new_child(None, TextTreeNode, content='Test <3')
        output = tree_node.render_html('')
        self.assertEqual('Test &lt;3', output)
