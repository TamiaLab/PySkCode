"""
SkCode titles utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import TextTreeNode
from skcode.tags.titles import TitleBaseTreeNode, generate_title_cls
from skcode.utility.titles import (
    extract_titles,
    make_titles_hierarchy,
    make_auto_title_ids,
    render_titles_hierarchy_html,
    render_titles_hierarchy_text
)


class TitlesUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the titles utility module. """

    def test_extract_titles(self):
        """ Test the ``extract_titles`` utility. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('title', generate_title_cls(1))
        document_tree.new_child(None, TextTreeNode)
        a2 = document_tree.new_child('title', generate_title_cls(1))
        document_tree.new_child(None, TextTreeNode)
        a3 = document_tree.new_child('title', generate_title_cls(1))
        document_tree.new_child(None, TextTreeNode)
        a4 = document_tree.new_child('title', generate_title_cls(1))
        titles = extract_titles(document_tree)
        self.assertEqual([a1, a2, a3, a4], titles)

    def test_extract_titles_no_titles(self):
        """ Test the ``extract_titles`` utility with no title. """
        document_tree = RootTreeNode()
        titles = extract_titles(document_tree)
        self.assertEqual([], titles)

    def test_make_auto_title_ids(self):
        """ Test the ``make_auto_title_ids`` utility. """
        document_tree = RootTreeNode()
        document_tree.new_child(None, TextTreeNode)
        a1 = document_tree.new_child('title', generate_title_cls(1))
        a1.new_child(None, TextTreeNode, content='Title 1')
        a2 = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'title-2-custom'})
        a2.new_child(None, TextTreeNode, content='Title 2')
        a3 = document_tree.new_child('title', generate_title_cls(1))
        a3.new_child(None, TextTreeNode, content='Title 3')
        a4 = document_tree.new_child('title', generate_title_cls(1))
        make_auto_title_ids(document_tree)
        self.assertEqual('title-1', a1.get_permalink_slug())
        self.assertEqual('title-2-custom', a2.get_permalink_slug())
        self.assertEqual('title-3', a3.get_permalink_slug())
        self.assertEqual('', a4.get_permalink_slug())

    def test_make_titles_hierarchy_no_titles(self):
        """ Test the ``make_titles_hierarchy`` utility. """
        titles = []
        titles_hierarchy = make_titles_hierarchy(titles)
        self.assertEqual([], list(titles_hierarchy))

    def test_make_titles_hierarchy(self):
        """ Test the ``make_titles_hierarchy`` utility. """
        document_tree = RootTreeNode()
        a = document_tree.new_child('title', generate_title_cls(3))
        b = document_tree.new_child('title', generate_title_cls(4))
        c = document_tree.new_child('title', generate_title_cls(1))
        d = document_tree.new_child('title', generate_title_cls(2))
        e = document_tree.new_child('title', generate_title_cls(3))
        f = document_tree.new_child('title', generate_title_cls(2))
        g = document_tree.new_child('title', generate_title_cls(3))
        h = document_tree.new_child('title', generate_title_cls(1))
        i = document_tree.new_child('title', generate_title_cls(2))
        j = document_tree.new_child('title', generate_title_cls(1))
        k = document_tree.new_child('title', generate_title_cls(1))
        l = document_tree.new_child('title', generate_title_cls(3))
        m = document_tree.new_child('title', generate_title_cls(4))
        n = document_tree.new_child('title', generate_title_cls(2))
        titles = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
        titles_hierarchy = make_titles_hierarchy(titles)
        self.assertEqual([
            (a, [
                (b, [])
            ]),
            (c, [
                (d, [
                    (e, [])
                ]),
                (f, [
                    (g, [])
                ])
            ]),
            (h, [
                (i, [])
            ]),
            (j, []),
            (k, [
                (l, [
                    (m, [])
                ]), (n, [])
            ])
        ], titles_hierarchy)

    def test_render_titles_hierarchy_html_no_titles(self):
        """ Test the ``render_titles_hierarchy_html`` utility. """
        titles_hierarchy = []
        output = render_titles_hierarchy_html(titles_hierarchy)
        self.assertEqual('', output)

    def test_render_titles_hierarchy_html(self):
        """ Test the ``render_titles_hierarchy_text`` utility. """
        document_tree = RootTreeNode()
        a = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title a'})
        a.new_child(None, TextTreeNode, content='Title a')
        b = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title b'})
        b.new_child(None, TextTreeNode, content='Title b')
        c = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title c'})
        c.new_child(None, TextTreeNode, content='Title c')
        d = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title d'})
        d.new_child(None, TextTreeNode, content='Title d')
        e = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title e'})
        e.new_child(None, TextTreeNode, content='Title e')
        f = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title f'})
        f.new_child(None, TextTreeNode, content='Title f')
        g = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title g'})
        g.new_child(None, TextTreeNode, content='Title g')
        h = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title h'})
        h.new_child(None, TextTreeNode, content='Title h')
        i = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title i'})
        i.new_child(None, TextTreeNode, content='Title i')
        j = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title j'})
        j.new_child(None, TextTreeNode, content='Title j')
        k = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title k'})
        k.new_child(None, TextTreeNode, content='Title k')
        l = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title l'})
        l.new_child(None, TextTreeNode, content='Title l')
        m = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title m'})
        m.new_child(None, TextTreeNode, content='Title m')
        n = document_tree.new_child('title', generate_title_cls(2))
        n.new_child(None, TextTreeNode, content='Title n')
        titles = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
        titles_hierarchy = make_titles_hierarchy(titles)
        output = render_titles_hierarchy_html(titles_hierarchy)
        expected_output = """<ul class="titles-summary">
<li class="titles-summary-entry">
<a href="#title-a" class="titles-summary-link">Title a</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-b" class="titles-summary-link">Title b</a>
</li>
</ul>
</li>
<li class="titles-summary-entry">
<a href="#title-c" class="titles-summary-link">Title c</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-d" class="titles-summary-link">Title d</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-e" class="titles-summary-link">Title e</a>
</li>
</ul>
</li>
<li class="titles-summary-entry">
<a href="#title-f" class="titles-summary-link">Title f</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-g" class="titles-summary-link">Title g</a>
</li>
</ul>
</li>
</ul>
</li>
<li class="titles-summary-entry">
<a href="#title-h" class="titles-summary-link">Title h</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-i" class="titles-summary-link">Title i</a>
</li>
</ul>
</li>
<li class="titles-summary-entry">
<a href="#title-j" class="titles-summary-link">Title j</a>
</li>
<li class="titles-summary-entry">
<a href="#title-k" class="titles-summary-link">Title k</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-l" class="titles-summary-link">Title l</a>
<ul class="titles-summary-subentry">
<li class="titles-summary-entry">
<a href="#title-m" class="titles-summary-link">Title m</a>
</li>
</ul>
</li>
<li class="titles-summary-entry">
<a href="#" class="titles-summary-link">Title n</a>
</li>
</ul>
</li>
</ul>"""
        self.assertEqual(expected_output, output)

    def test_render_titles_hierarchy_html_custom_class(self):
        """ Test the ``render_titles_hierarchy_html`` utility. """
        document_tree = RootTreeNode()
        a = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title a'})
        a.new_child(None, TextTreeNode, content='Title a')
        b = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title b'})
        b.new_child(None, TextTreeNode, content='Title b')
        c = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title c'})
        c.new_child(None, TextTreeNode, content='Title c')
        d = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title d'})
        d.new_child(None, TextTreeNode, content='Title d')
        e = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title e'})
        e.new_child(None, TextTreeNode, content='Title e')
        f = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title f'})
        f.new_child(None, TextTreeNode, content='Title f')
        g = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title g'})
        g.new_child(None, TextTreeNode, content='Title g')
        h = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title h'})
        h.new_child(None, TextTreeNode, content='Title h')
        i = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title i'})
        i.new_child(None, TextTreeNode, content='Title i')
        j = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title j'})
        j.new_child(None, TextTreeNode, content='Title j')
        k = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title k'})
        k.new_child(None, TextTreeNode, content='Title k')
        l = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title l'})
        l.new_child(None, TextTreeNode, content='Title l')
        m = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title m'})
        m.new_child(None, TextTreeNode, content='Title m')
        n = document_tree.new_child('title', generate_title_cls(2))
        n.new_child(None, TextTreeNode, content='Title n')
        titles = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
        titles_hierarchy = make_titles_hierarchy(titles)
        output = render_titles_hierarchy_html(titles_hierarchy,
                                              root_ul_class_name='custom_summary',
                                              li_class_name='custom_summary-entry',
                                              a_class_name='custom_summary-link',
                                              ul_class_name='custom_summary-subentry')
        expected_output = """<ul class="custom_summary">
<li class="custom_summary-entry">
<a href="#title-a" class="custom_summary-link">Title a</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-b" class="custom_summary-link">Title b</a>
</li>
</ul>
</li>
<li class="custom_summary-entry">
<a href="#title-c" class="custom_summary-link">Title c</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-d" class="custom_summary-link">Title d</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-e" class="custom_summary-link">Title e</a>
</li>
</ul>
</li>
<li class="custom_summary-entry">
<a href="#title-f" class="custom_summary-link">Title f</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-g" class="custom_summary-link">Title g</a>
</li>
</ul>
</li>
</ul>
</li>
<li class="custom_summary-entry">
<a href="#title-h" class="custom_summary-link">Title h</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-i" class="custom_summary-link">Title i</a>
</li>
</ul>
</li>
<li class="custom_summary-entry">
<a href="#title-j" class="custom_summary-link">Title j</a>
</li>
<li class="custom_summary-entry">
<a href="#title-k" class="custom_summary-link">Title k</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-l" class="custom_summary-link">Title l</a>
<ul class="custom_summary-subentry">
<li class="custom_summary-entry">
<a href="#title-m" class="custom_summary-link">Title m</a>
</li>
</ul>
</li>
<li class="custom_summary-entry">
<a href="#" class="custom_summary-link">Title n</a>
</li>
</ul>
</li>
</ul>"""
        self.assertEqual(expected_output, output)

    def test_render_titles_hierarchy_text_no_titles(self):
        """ Test the ``render_titles_hierarchy_text`` utility. """
        titles_hierarchy = []
        output = render_titles_hierarchy_text(titles_hierarchy)
        self.assertEqual('', output)

    def test_render_titles_hierarchy_text(self):
        """ Test the ``render_titles_hierarchy_text`` utility. """
        document_tree = RootTreeNode()
        a = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title a'})
        a.new_child(None, TextTreeNode, content='Title a')
        b = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title b'})
        b.new_child(None, TextTreeNode, content='Title b')
        c = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title c'})
        c.new_child(None, TextTreeNode, content='Title c')
        d = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title d'})
        d.new_child(None, TextTreeNode, content='Title d')
        e = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title e'})
        e.new_child(None, TextTreeNode, content='Title e')
        f = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title f'})
        f.new_child(None, TextTreeNode, content='Title f')
        g = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title g'})
        g.new_child(None, TextTreeNode, content='Title g')
        h = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title h'})
        h.new_child(None, TextTreeNode, content='Title h')
        i = document_tree.new_child('title', generate_title_cls(2), attrs={'id': 'Title i'})
        i.new_child(None, TextTreeNode, content='Title i')
        j = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title j'})
        j.new_child(None, TextTreeNode, content='Title j')
        k = document_tree.new_child('title', generate_title_cls(1), attrs={'id': 'Title k'})
        k.new_child(None, TextTreeNode, content='Title k')
        l = document_tree.new_child('title', generate_title_cls(3), attrs={'id': 'Title l'})
        l.new_child(None, TextTreeNode, content='Title l')
        m = document_tree.new_child('title', generate_title_cls(4), attrs={'id': 'Title m'})
        m.new_child(None, TextTreeNode, content='Title m')
        n = document_tree.new_child('title', generate_title_cls(2))
        n.new_child(None, TextTreeNode, content='Title n')
        titles = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
        titles_hierarchy = make_titles_hierarchy(titles)
        output = render_titles_hierarchy_text(titles_hierarchy)
        expected_output = """# Title a
## Title b
# Title c
## Title d
### Title e
## Title f
### Title g
# Title h
## Title i
# Title j
# Title k
## Title l
### Title m
## Title n"""
        self.assertEqual(expected_output, output)
