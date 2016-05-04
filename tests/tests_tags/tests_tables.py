"""
SkCode tables tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         TableTagOptions,
                         TableRowTagOptions,
                         TableCellTagOptions,
                         TableHeaderCellTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)


class TablesTagTestCase(unittest.TestCase):
    """ Tests suite for the tables tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('table', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['table'], TableTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TableTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('table', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('table table-condensed table-striped', opts.css_class_name)
        self.assertEqual('<table class="{class_name}">{inner_html}</table>\n', opts.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = TableTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('table', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<table class="table table-condensed table-striped">test</table>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering with a custom CSS class name. """
        opts = TableTagOptions(css_class_name='custom_css')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('table', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<table class="custom_css">test</table>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = TableTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('table', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class TableRowsTagTestCase(unittest.TestCase):
    """ Tests suite for the table rows tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('tr', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['tr'], TableRowTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TableRowTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('tr', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('<tr>{inner_html}</tr>\n', opts.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = TableRowTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('tr', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<tr>test</tr>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = TableRowTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('tr', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class TableCellsTagTestCase(unittest.TestCase):
    """ Tests suite for the table cells tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('td', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['td'], TableCellTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TableCellTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('td', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('colspan', opts.colspan_attr_name)
        self.assertEqual('rowspan', opts.rowspan_attr_name)
        self.assertEqual('<td{extra_args}>{inner_html}</td>\n', opts.html_render_template)

    def test_get_cell_colspan(self):
        """ Test the ``get_cell_colspan`` with a valid value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '3'})
        colspan = opts.get_cell_colspan(tree_node)
        self.assertEqual(colspan, 3)

    def test_get_cell_colspan_with_no_value_set(self):
        """ Test the ``get_cell_colspan`` with no value set.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={})
        colspan = opts.get_cell_colspan(tree_node)
        self.assertEqual(colspan, 1)

    def test_get_cell_colspan_with_non_number(self):
        """ Test the ``get_cell_colspan`` with an invalid non-number value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': 'abc'})
        colspan = opts.get_cell_colspan(tree_node)
        self.assertEqual(colspan, 1)

    def test_get_cell_colspan_with_negative_value(self):
        """ Test the ``get_cell_colspan`` with an invalid negative value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '-3'})
        colspan = opts.get_cell_colspan(tree_node)
        self.assertEqual(colspan, 1)

    def test_get_cell_rowspan(self):
        """ Test the ``get_cell_rowspan`` with a valid value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'rowspan': '3'})
        rowspan = opts.get_cell_rowspan(tree_node)
        self.assertEqual(rowspan, 3)

    def test_get_cell_rowspan_with_no_value_set(self):
        """ Test the ``get_cell_rowspan`` with no value set.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={})
        rowspan = opts.get_cell_rowspan(tree_node)
        self.assertEqual(rowspan, 1)

    def test_get_cell_rowspan_with_non_number(self):
        """ Test the ``get_cell_rowspan`` with an invalid non-number value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'rowspan': 'abc'})
        rowspan = opts.get_cell_rowspan(tree_node)
        self.assertEqual(rowspan, 1)

    def test_get_cell_rowspan_with_negative_value(self):
        """ Test the ``get_cell_rowspan`` with a valid value.  """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'rowspan': '-3'})
        rowspan = opts.get_cell_rowspan(tree_node)
        self.assertEqual(rowspan, 1)

    def test_get_html_extra_attrs_blank(self):
        """ Test the ``get_html_extra_attrs`` method without any colspan or rowspan value set. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={})
        extra_attrs = opts.get_html_extra_attrs(tree_node)
        self.assertEqual('', extra_attrs)

    def test_get_html_extra_attrs_with_colspan(self):
        """ Test the ``get_html_extra_attrs`` method with colspan set. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '3'})
        extra_attrs = opts.get_html_extra_attrs(tree_node)
        self.assertEqual(' colspan="3"', extra_attrs)

    def test_get_html_extra_attrs_with_row_span(self):
        """ Test the ``get_html_extra_attrs`` method with rowspan set. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'rowspan': '3'})
        extra_attrs = opts.get_html_extra_attrs(tree_node)
        self.assertEqual(' rowspan="3"', extra_attrs)

    def test_get_html_extra_attrs_with_colspan_and_rowspan(self):
        """ Test the ``get_html_extra_attrs`` method with colspan and rowspan set. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '2', 'rowspan': '3'})
        extra_attrs = opts.get_html_extra_attrs(tree_node)
        self.assertEqual(' colspan="2" rowspan="3"', extra_attrs)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<td>test</td>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_extra_attrs(self):
        """ Test HTML rendering with extra attributes. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<td colspan="2" rowspan="3">test</td>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_attrs(self):
        """ Test text rendering with extra attributes. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts)
        rendered_output = opts.get_skcode_attributes(tree_node, 'test')
        expected_output = ({'colspan': '', 'rowspan': ''}, None)
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes_with_extra_attrs(self):
        """ Test the ``get_skcode_attributes`` method with extra attributes. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '1', 'rowspan': '1'})
        rendered_output = opts.get_skcode_attributes(tree_node, 'test')
        expected_output = ({'colspan': '', 'rowspan': ''}, None)
        self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes_with_extra_attrs_2(self):
        """ Test the ``get_skcode_attributes`` method with extra attributes. """
        opts = TableCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('td', opts, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = opts.get_skcode_attributes(tree_node, 'test')
        expected_output = ({'colspan': '2', 'rowspan': '3'}, None)
        self.assertEqual(expected_output, rendered_output)


class TableHeaderCellsTagTestCase(unittest.TestCase):
    """ Tests suite for the table cells tag module. """

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(TableHeaderCellTagOptions, TableCellTagOptions))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('th', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['th'], TableHeaderCellTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = TableHeaderCellTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('th', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual('colspan', opts.colspan_attr_name)
        self.assertEqual('rowspan', opts.rowspan_attr_name)
        self.assertEqual('<th{extra_args}>{inner_html}</th>\n', opts.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = TableHeaderCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('th', opts)
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<th>test</th>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_extra_attrs(self):
        """ Test HTML rendering with extra attributes. """
        opts = TableHeaderCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('th', opts, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = opts.render_html(tree_node, 'test')
        expected_output = '<th colspan="2" rowspan="3">test</th>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = TableHeaderCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('th', opts)
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_attrs(self):
        """ Test text rendering with extra attributes. """
        opts = TableHeaderCellTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('th', opts, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = opts.render_text(tree_node, 'test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)
