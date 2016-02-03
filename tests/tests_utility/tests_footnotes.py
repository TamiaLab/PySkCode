"""
SkCode footnotes utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         FootnoteDeclarationTagOptions,
                         TextTagOptions)
from skcode.utility import (extract_footnotes,
                            render_footnotes_html,
                            render_footnotes_text)


class CustomFootnoteDeclarationTagOption(FootnoteDeclarationTagOptions):
    """
    Custom ``FootnoteDeclarationTagOptions`` subclass for tests.
    """
    pass


class FootnotesUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the footnotes utility module. """

    def test_extract_footnotes(self):
        """ Test the ``extract_footnotes`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a2 = document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a4 = document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        footnotes = extract_footnotes(document_tree)
        self.assertEqual([a1, a2, a3, a4], footnotes)

    def test_extract_footnotes_no_footnotes(self):
        """ Test the ``extract_footnotes`` utility with no footnote. """
        document_tree = RootTreeNode(RootTagOptions())
        footnotes = extract_footnotes(document_tree)
        self.assertEqual([], footnotes)

    def test_extract_footnotes_custom_class(self):
        """ Test the ``extract_footnotes`` utility with a custom footnote options class. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('footnote', FootnoteDeclarationTagOptions())
        footnotes = extract_footnotes(document_tree, footnote_declaration_ops_cls=CustomFootnoteDeclarationTagOption)
        self.assertEqual([a1, a3], footnotes)

    def test_render_footnotes_html_no_footnote(self):
        """ Test the ``render_footnotes_html`` helper with an empty footnotes list. """
        self.assertEqual('', render_footnotes_html([]))

    def test_render_footnotes_html(self):
        """ Test the ``render_footnotes_html`` helper. """
        self.maxDiff = None
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a1.new_child('_text', TextTagOptions(), content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a2.new_child('_text', TextTagOptions(), content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a3.new_child('_text', TextTagOptions(), content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a4.new_child('_text', TextTagOptions(), content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual("""<div class="footnotes">
<p class="footnotes-details">
<a id="footnote-1" href="#footnote-backref-1"><sup>[1]</sup></a>
Line 1
</p>
<p class="footnotes-details">
<a id="footnote-2" href="#footnote-backref-2"><sup>[2]</sup></a>
Line 2
</p>
<p class="footnotes-details">
<a id="footnote-3" href="#footnote-backref-3"><sup>[3]</sup></a>
Line 3
</p>
<p class="footnotes-details">
<a id="footnote-4" href="#footnote-backref-4"><sup>[4]</sup></a>
Line 4
</p>
</div>""", render_footnotes_html(footnotes))

    def test_render_footnotes_html_custom_css(self):
        """ Test the ``render_footnotes_html`` helper with custom CSS. """
        self.maxDiff = None
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a1.new_child('_text', TextTagOptions(), content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a2.new_child('_text', TextTagOptions(), content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a3.new_child('_text', TextTagOptions(), content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a4.new_child('_text', TextTagOptions(), content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual("""<div class="custom_div">
<p class="custom_p">
<a id="footnote-1" href="#footnote-backref-1"><sup>[1]</sup></a>
Line 1
</p>
<p class="custom_p">
<a id="footnote-2" href="#footnote-backref-2"><sup>[2]</sup></a>
Line 2
</p>
<p class="custom_p">
<a id="footnote-3" href="#footnote-backref-3"><sup>[3]</sup></a>
Line 3
</p>
<p class="custom_p">
<a id="footnote-4" href="#footnote-backref-4"><sup>[4]</sup></a>
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
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a1.new_child('_text', TextTagOptions(), content='Line 1')
        a2 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a2.new_child('_text', TextTagOptions(), content='Line 2')
        a3 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a3.new_child('_text', TextTagOptions(), content='Line 3')
        a4 = document_tree.new_child('footnote', CustomFootnoteDeclarationTagOption())
        a4.new_child('_text', TextTagOptions(), content='Line 4')
        footnotes = [a1, a2, a3, a4]
        self.assertEqual('[^1]: Line 1\n[^2]: Line 2\n[^3]: Line 3\n[^4]: Line 4\n\n', render_footnotes_text(footnotes))
