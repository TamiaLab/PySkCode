"""
SkCode footnotes utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    FootnoteDeclarationTreeNode,
    TextTreeNode
)
from skcode.utility.footnotes import (
    extract_footnotes,
    render_footnotes_html,
    render_footnotes_text
)


class CustomFootnoteDeclarationTagOption(FootnoteDeclarationTreeNode):
    """
    Custom ``FootnoteDeclarationTreeNode`` subclass for tests.
    """
    pass


class FootnotesUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the footnotes utility module. """

    def test_extract_footnotes(self):
        """ Test the ``extract_footnotes`` utility. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a2 = document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a4 = document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        footnotes = extract_footnotes(document_tree)
        self.assertEqual([a1, a2, a3, a4], footnotes)

    def test_extract_footnotes_no_footnotes(self):
        """ Test the ``extract_footnotes`` utility with no footnote. """
        document_tree = RootTreeNode()
        footnotes = extract_footnotes(document_tree)
        self.assertEqual([], footnotes)

    def test_extract_footnotes_custom_class(self):
        """ Test the ``extract_footnotes`` utility with a custom footnote options class. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        document_tree.new_child(None, TextTreeNode)
        document_tree.new_child('footnote', FootnoteDeclarationTreeNode)
        footnotes = extract_footnotes(document_tree, footnote_declaration_node_cls=CustomFootnoteDeclarationTagOption)
        self.assertEqual([a1, a3], footnotes)

    def test_render_footnotes_html_no_footnote(self):
        """ Test the ``render_footnotes_html`` helper with an empty footnotes list. """
        self.assertEqual('', render_footnotes_html([]))

    def test_render_footnotes_html(self):
        """ Test the ``render_footnotes_html`` helper. """
        self.maxDiff = None
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a1.new_child(None, TextTreeNode, content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a2.new_child(None, TextTreeNode, content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a3.new_child(None, TextTreeNode, content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a4.new_child(None, TextTreeNode, content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual("""<div class="footnotes">
<p class="footnotes-details">
<a id="footnote-footnote-1" href="#footnote-backref-footnote-1"><sup>[footnote-1]</sup></a>
Line 1
</p>
<p class="footnotes-details">
<a id="footnote-footnote-2" href="#footnote-backref-footnote-2"><sup>[footnote-2]</sup></a>
Line 2
</p>
<p class="footnotes-details">
<a id="footnote-footnote-3" href="#footnote-backref-footnote-3"><sup>[footnote-3]</sup></a>
Line 3
</p>
<p class="footnotes-details">
<a id="footnote-footnote-4" href="#footnote-backref-footnote-4"><sup>[footnote-4]</sup></a>
Line 4
</p>
</div>""", render_footnotes_html(footnotes))

    def test_render_footnotes_html_custom_css(self):
        """ Test the ``render_footnotes_html`` helper with custom CSS. """
        self.maxDiff = None
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a1.new_child(None, TextTreeNode, content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a2.new_child(None, TextTreeNode, content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a3.new_child(None, TextTreeNode, content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a4.new_child(None, TextTreeNode, content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual("""<div class="custom_div">
<p class="custom_p">
<a id="footnote-footnote-1" href="#footnote-backref-footnote-1"><sup>[footnote-1]</sup></a>
Line 1
</p>
<p class="custom_p">
<a id="footnote-footnote-2" href="#footnote-backref-footnote-2"><sup>[footnote-2]</sup></a>
Line 2
</p>
<p class="custom_p">
<a id="footnote-footnote-3" href="#footnote-backref-footnote-3"><sup>[footnote-3]</sup></a>
Line 3
</p>
<p class="custom_p">
<a id="footnote-footnote-4" href="#footnote-backref-footnote-4"><sup>[footnote-4]</sup></a>
Line 4
</p>
</div>""", render_footnotes_html(footnotes,
                                 wrapping_div_class_name='custom_div',
                                 wrapping_p_class_name='custom_p'))

    def test_render_footnotes_text_no_footnote(self):
        """ Test the ``render_footnotes_text`` helper with an empty footnotes list. """
        self.assertEqual('', render_footnotes_text([]))

    def test_render_footnotes_text(self):
        """ Test the ``render_footnotes_text`` helper. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a1.new_child(None, TextTreeNode, content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a2.new_child(None, TextTreeNode, content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a3.new_child(None, TextTreeNode, content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption)
        a4.new_child(None, TextTreeNode, content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual('[^footnote-1]: Line 1\n[^footnote-2]: Line 2\n[^footnote-3]: Line 3\n[^footnote-4]: Line 4\n\n', render_footnotes_text(footnotes))
