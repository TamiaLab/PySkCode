"""
SkCode tables tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    TableTreeNode,
    TableRowTreeNode,
    TableCellTreeNode,
    TableHeaderCellTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)


class CustomTableTreeNode(TableTreeNode):
    """ Custom table class """

    css_class_name = 'custom_css'


class TablesTagTestCase(unittest.TestCase):
    """ Tests suite for the tables tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TableTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TableTreeNode.newline_closes)
        self.assertFalse(TableTreeNode.same_tag_closes)
        self.assertFalse(TableTreeNode.weak_parent_close)
        self.assertFalse(TableTreeNode.standalone)
        self.assertTrue(TableTreeNode.parse_embedded)
        self.assertFalse(TableTreeNode.inline)
        self.assertTrue(TableTreeNode.close_inlines)
        self.assertEqual('table', TableTreeNode.canonical_tag_name)
        self.assertEqual((), TableTreeNode.alias_tag_names)
        self.assertFalse(TableTreeNode.make_paragraphs_here)
        self.assertEqual('table table-condensed table-striped', TableTreeNode.css_class_name)
        self.assertEqual('<table class="{class_name}">{inner_html}</table>\n', TableTreeNode.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('table', TableTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<table class="table table-condensed table-striped">test</table>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_custom_css(self):
        """ Test HTML rendering with a custom CSS class name. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('table', CustomTableTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<table class="custom_css">test</table>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('table', TableTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class TableRowsTagTestCase(unittest.TestCase):
    """ Tests suite for the table rows tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TableRowTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TableRowTreeNode.newline_closes)
        self.assertFalse(TableRowTreeNode.same_tag_closes)
        self.assertFalse(TableRowTreeNode.weak_parent_close)
        self.assertFalse(TableRowTreeNode.standalone)
        self.assertTrue(TableRowTreeNode.parse_embedded)
        self.assertFalse(TableRowTreeNode.inline)
        self.assertTrue(TableRowTreeNode.close_inlines)
        self.assertEqual('tr', TableRowTreeNode.canonical_tag_name)
        self.assertEqual((), TableRowTreeNode.alias_tag_names)
        self.assertFalse(TableRowTreeNode.make_paragraphs_here)
        self.assertEqual('<tr>{inner_html}</tr>\n', TableRowTreeNode.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('tr', TableRowTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<tr>test</tr>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('tr', TableRowTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class TableCellsTagTestCase(unittest.TestCase):
    """ Tests suite for the table cells tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TableCellTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TableCellTreeNode.newline_closes)
        self.assertFalse(TableCellTreeNode.same_tag_closes)
        self.assertFalse(TableCellTreeNode.weak_parent_close)
        self.assertFalse(TableCellTreeNode.standalone)
        self.assertTrue(TableCellTreeNode.parse_embedded)
        self.assertFalse(TableCellTreeNode.inline)
        self.assertTrue(TableCellTreeNode.close_inlines)
        self.assertEqual('td', TableCellTreeNode.canonical_tag_name)
        self.assertEqual((), TableCellTreeNode.alias_tag_names)
        self.assertTrue(TableCellTreeNode.make_paragraphs_here)
        self.assertEqual('colspan', TableCellTreeNode.colspan_attr_name)
        self.assertEqual('rowspan', TableCellTreeNode.rowspan_attr_name)
        self.assertEqual('<td{extra_args}>{inner_html}</td>\n', TableCellTreeNode.html_render_template)

    def test_get_cell_colspan(self):
        """ Test the ``get_cell_colspan`` with a valid value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '3'})
        colspan = tree_node.get_cell_colspan()
        self.assertEqual(colspan, 3)

    def test_get_cell_colspan_with_no_value_set(self):
        """ Test the ``get_cell_colspan`` with no value set.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={})
        colspan = tree_node.get_cell_colspan()
        self.assertEqual(colspan, 1)

    def test_get_cell_colspan_with_non_number(self):
        """ Test the ``get_cell_colspan`` with an invalid non-number value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': 'abc'})
        colspan = tree_node.get_cell_colspan()
        self.assertEqual(colspan, 1)

    def test_get_cell_colspan_with_negative_value(self):
        """ Test the ``get_cell_colspan`` with an invalid negative value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '-3'})
        colspan = tree_node.get_cell_colspan()
        self.assertEqual(colspan, 1)

    def test_get_cell_rowspan(self):
        """ Test the ``get_cell_rowspan`` with a valid value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': '3'})
        rowspan = tree_node.get_cell_rowspan()
        self.assertEqual(rowspan, 3)

    def test_get_cell_rowspan_with_no_value_set(self):
        """ Test the ``get_cell_rowspan`` with no value set.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={})
        rowspan = tree_node.get_cell_rowspan()
        self.assertEqual(rowspan, 1)

    def test_get_cell_rowspan_with_non_number(self):
        """ Test the ``get_cell_rowspan`` with an invalid non-number value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': 'abc'})
        rowspan = tree_node.get_cell_rowspan()
        self.assertEqual(rowspan, 1)

    def test_get_cell_rowspan_with_negative_value(self):
        """ Test the ``get_cell_rowspan`` with a valid value.  """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': '-3'})
        rowspan = tree_node.get_cell_rowspan()
        self.assertEqual(rowspan, 1)

    def test_get_html_extra_attrs_blank(self):
        """ Test the ``get_html_extra_attrs`` method without any colspan or rowspan value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={})
        extra_attrs = tree_node.get_html_extra_attrs()
        self.assertEqual('', extra_attrs)

    def test_get_html_extra_attrs_with_colspan(self):
        """ Test the ``get_html_extra_attrs`` method with colspan set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '3'})
        extra_attrs = tree_node.get_html_extra_attrs()
        self.assertEqual(' colspan="3"', extra_attrs)

    def test_get_html_extra_attrs_with_row_span(self):
        """ Test the ``get_html_extra_attrs`` method with rowspan set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': '3'})
        extra_attrs = tree_node.get_html_extra_attrs()
        self.assertEqual(' rowspan="3"', extra_attrs)

    def test_get_html_extra_attrs_with_colspan_and_rowspan(self):
        """ Test the ``get_html_extra_attrs`` method with colspan and rowspan set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '2', 'rowspan': '3'})
        extra_attrs = tree_node.get_html_extra_attrs()
        self.assertEqual(' colspan="2" rowspan="3"', extra_attrs)

    def test_sanitize_node(self):
        """ Test the ``sanitize_node`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': '3'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '3'})
        tree_node.sanitize_node([])
        self.assertEqual('', tree_node.error_message)

        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': '-3'})
        tree_node.sanitize_node([])
        self.assertEqual('Row span must be greater than 1', tree_node.error_message)
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '-3'})
        tree_node.sanitize_node([])
        self.assertEqual('Column span must be greater than 1', tree_node.error_message)

        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'rowspan': 'abc'})
        tree_node.sanitize_node([])
        self.assertEqual('abc is not a number', tree_node.error_message)
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': 'abc'})
        tree_node.sanitize_node([])
        self.assertEqual('abc is not a number', tree_node.error_message)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<td>test</td>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_extra_attrs(self):
        """ Test HTML rendering with extra attributes. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = tree_node.render_html('test')
        expected_output = '<td colspan="2" rowspan="3">test</td>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_attrs(self):
        """ Test text rendering with extra attributes. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('td', TableCellTreeNode, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)


class TableHeaderCellsTagTestCase(unittest.TestCase):
    """ Tests suite for the table cells tag module. """

    def test_subclassing(self):
        """ Test super class """
        self.assertTrue(issubclass(TableHeaderCellTreeNode, TableCellTreeNode))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(TableHeaderCellTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(TableHeaderCellTreeNode.newline_closes)
        self.assertFalse(TableHeaderCellTreeNode.same_tag_closes)
        self.assertFalse(TableHeaderCellTreeNode.weak_parent_close)
        self.assertFalse(TableHeaderCellTreeNode.standalone)
        self.assertTrue(TableHeaderCellTreeNode.parse_embedded)
        self.assertFalse(TableHeaderCellTreeNode.inline)
        self.assertTrue(TableHeaderCellTreeNode.close_inlines)
        self.assertEqual('th', TableHeaderCellTreeNode.canonical_tag_name)
        self.assertEqual((), TableHeaderCellTreeNode.alias_tag_names)
        self.assertTrue(TableHeaderCellTreeNode.make_paragraphs_here)
        self.assertEqual('colspan', TableHeaderCellTreeNode.colspan_attr_name)
        self.assertEqual('rowspan', TableHeaderCellTreeNode.rowspan_attr_name)
        self.assertEqual('<th{extra_args}>{inner_html}</th>\n', TableHeaderCellTreeNode.html_render_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('th', TableHeaderCellTreeNode)
        rendered_output = tree_node.render_html('test')
        expected_output = '<th>test</th>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_extra_attrs(self):
        """ Test HTML rendering with extra attributes. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('th', TableHeaderCellTreeNode, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = tree_node.render_html('test')
        expected_output = '<th colspan="2" rowspan="3">test</th>\n'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('th', TableHeaderCellTreeNode)
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_extra_attrs(self):
        """ Test text rendering with extra attributes. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('th', TableHeaderCellTreeNode, attrs={'colspan': '2', 'rowspan': '3'})
        rendered_output = tree_node.render_text('test')
        expected_output = 'test'
        self.assertEqual(expected_output, rendered_output)
