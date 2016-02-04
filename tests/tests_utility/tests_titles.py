"""
SkCode titles utility test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TitleTagOptions,
                         TextTagOptions)
from skcode.utility import (extract_titles,
                            make_titles_hierarchy, make_auto_title_ids,
                            render_titles_hierarchy_html, render_titles_hierarchy_text)


class CustomTitleTagOption(TitleTagOptions):
    """
    Custom ``TitleTagOptions`` subclass for tests.
    """
    pass


class TitlesUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the titles utility module. """

    def test_extract_titles(self):
        """ Test the ``extract_titles`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('title', TitleTagOptions(1))
        document_tree.new_child('_text', TextTagOptions())
        a2 = document_tree.new_child('title', TitleTagOptions(1))
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('title', TitleTagOptions(1))
        document_tree.new_child('_text', TextTagOptions())
        a4 = document_tree.new_child('title', TitleTagOptions(1))
        titles = extract_titles(document_tree)
        self.assertEqual([a1, a2, a3, a4], titles)

    def test_extract_titles_no_titles(self):
        """ Test the ``extract_titles`` utility with no title. """
        document_tree = RootTreeNode(RootTagOptions())
        titles = extract_titles(document_tree)
        self.assertEqual([], titles)

    def test_extract_titles_custom_class(self):
        """ Test the ``extract_titles`` utility with a custom title options class. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('title', CustomTitleTagOption(1))
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('title', TitleTagOptions(1))
        document_tree.new_child('_text', TextTagOptions())
        a3 = document_tree.new_child('title', CustomTitleTagOption(1))
        document_tree.new_child('_text', TextTagOptions())
        document_tree.new_child('title', TitleTagOptions(1))
        titles = extract_titles(document_tree, title_ops_cls=CustomTitleTagOption)
        self.assertEqual([a1, a3], titles)

    def test_make_auto_title_ids(self):
        """ Test the ``make_auto_title_ids`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        document_tree.new_child('_text', TextTagOptions())
        a1 = document_tree.new_child('title', TitleTagOptions(1))
        a1.new_child('_text', TextTagOptions(), content='Title 1')
        a2 = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'title-2-custom'})
        a2.new_child('_text', TextTagOptions(), content='Title 2')
        a3 = document_tree.new_child('title', TitleTagOptions(1))
        a3.new_child('_text', TextTagOptions(), content='Title 3')
        a4 = document_tree.new_child('title', TitleTagOptions(1))
        make_auto_title_ids(document_tree)
        self.assertEqual('title-1', a1.opts.get_permalink_slug(a1))
        self.assertEqual('title-2-custom', a2.opts.get_permalink_slug(a2))
        self.assertEqual('title-3', a3.opts.get_permalink_slug(a3))
        self.assertEqual('', a4.opts.get_permalink_slug(a4))

    def test_make_titles_hierarchy_no_titles(self):
        """ Test the ``make_titles_hierarchy`` utility. """
        titles = []
        titles_hierarchy = make_titles_hierarchy(titles)
        self.assertEqual([], list(titles_hierarchy))

    def test_make_titles_hierarchy(self):
        """ Test the ``make_titles_hierarchy`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        a = document_tree.new_child('title', TitleTagOptions(3))
        b = document_tree.new_child('title', TitleTagOptions(4))
        c = document_tree.new_child('title', TitleTagOptions(1))
        d = document_tree.new_child('title', TitleTagOptions(2))
        e = document_tree.new_child('title', TitleTagOptions(3))
        f = document_tree.new_child('title', TitleTagOptions(2))
        g = document_tree.new_child('title', TitleTagOptions(3))
        h = document_tree.new_child('title', TitleTagOptions(1))
        i = document_tree.new_child('title', TitleTagOptions(2))
        j = document_tree.new_child('title', TitleTagOptions(1))
        k = document_tree.new_child('title', TitleTagOptions(1))
        l = document_tree.new_child('title', TitleTagOptions(3))
        m = document_tree.new_child('title', TitleTagOptions(4))
        n = document_tree.new_child('title', TitleTagOptions(2))
        titles = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
        titles_hierarchy = make_titles_hierarchy(titles)

        def _recur_list(titles_grp):
            result = []
            for title, subtitles in titles_grp:
                result.append((title, _recur_list(subtitles)))
            return result

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
        ], _recur_list(titles_hierarchy))

    def test_render_titles_hierarchy_html_no_titles(self):
        """ Test the ``render_titles_hierarchy_html`` utility. """
        titles_hierarchy = []
        output = render_titles_hierarchy_html(titles_hierarchy)
        self.assertEqual('', output)

    def test_render_titles_hierarchy_html(self):
        """ Test the ``render_titles_hierarchy_text`` utility. """
        document_tree = RootTreeNode(RootTagOptions())
        a = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title a'})
        a.new_child('_text', TextTagOptions(), content='Title a')
        b = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title b'})
        b.new_child('_text', TextTagOptions(), content='Title b')
        c = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title c'})
        c.new_child('_text', TextTagOptions(), content='Title c')
        d = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title d'})
        d.new_child('_text', TextTagOptions(), content='Title d')
        e = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title e'})
        e.new_child('_text', TextTagOptions(), content='Title e')
        f = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title f'})
        f.new_child('_text', TextTagOptions(), content='Title f')
        g = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title g'})
        g.new_child('_text', TextTagOptions(), content='Title g')
        h = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title h'})
        h.new_child('_text', TextTagOptions(), content='Title h')
        i = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title i'})
        i.new_child('_text', TextTagOptions(), content='Title i')
        j = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title j'})
        j.new_child('_text', TextTagOptions(), content='Title j')
        k = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title k'})
        k.new_child('_text', TextTagOptions(), content='Title k')
        l = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title l'})
        l.new_child('_text', TextTagOptions(), content='Title l')
        m = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title m'})
        m.new_child('_text', TextTagOptions(), content='Title m')
        n = document_tree.new_child('title', TitleTagOptions(2))
        n.new_child('_text', TextTagOptions(), content='Title n')
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
        document_tree = RootTreeNode(RootTagOptions())
        a = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title a'})
        a.new_child('_text', TextTagOptions(), content='Title a')
        b = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title b'})
        b.new_child('_text', TextTagOptions(), content='Title b')
        c = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title c'})
        c.new_child('_text', TextTagOptions(), content='Title c')
        d = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title d'})
        d.new_child('_text', TextTagOptions(), content='Title d')
        e = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title e'})
        e.new_child('_text', TextTagOptions(), content='Title e')
        f = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title f'})
        f.new_child('_text', TextTagOptions(), content='Title f')
        g = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title g'})
        g.new_child('_text', TextTagOptions(), content='Title g')
        h = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title h'})
        h.new_child('_text', TextTagOptions(), content='Title h')
        i = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title i'})
        i.new_child('_text', TextTagOptions(), content='Title i')
        j = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title j'})
        j.new_child('_text', TextTagOptions(), content='Title j')
        k = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title k'})
        k.new_child('_text', TextTagOptions(), content='Title k')
        l = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title l'})
        l.new_child('_text', TextTagOptions(), content='Title l')
        m = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title m'})
        m.new_child('_text', TextTagOptions(), content='Title m')
        n = document_tree.new_child('title', TitleTagOptions(2))
        n.new_child('_text', TextTagOptions(), content='Title n')
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
        document_tree = RootTreeNode(RootTagOptions())
        a = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title a'})
        a.new_child('_text', TextTagOptions(), content='Title a')
        b = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title b'})
        b.new_child('_text', TextTagOptions(), content='Title b')
        c = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title c'})
        c.new_child('_text', TextTagOptions(), content='Title c')
        d = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title d'})
        d.new_child('_text', TextTagOptions(), content='Title d')
        e = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title e'})
        e.new_child('_text', TextTagOptions(), content='Title e')
        f = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title f'})
        f.new_child('_text', TextTagOptions(), content='Title f')
        g = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title g'})
        g.new_child('_text', TextTagOptions(), content='Title g')
        h = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title h'})
        h.new_child('_text', TextTagOptions(), content='Title h')
        i = document_tree.new_child('title', TitleTagOptions(2), attrs={'id': 'Title i'})
        i.new_child('_text', TextTagOptions(), content='Title i')
        j = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title j'})
        j.new_child('_text', TextTagOptions(), content='Title j')
        k = document_tree.new_child('title', TitleTagOptions(1), attrs={'id': 'Title k'})
        k.new_child('_text', TextTagOptions(), content='Title k')
        l = document_tree.new_child('title', TitleTagOptions(3), attrs={'id': 'Title l'})
        l.new_child('_text', TextTagOptions(), content='Title l')
        m = document_tree.new_child('title', TitleTagOptions(4), attrs={'id': 'Title m'})
        m.new_child('_text', TextTagOptions(), content='Title m')
        n = document_tree.new_child('title', TitleTagOptions(2))
        n.new_child('_text', TextTagOptions(), content='Title n')
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
