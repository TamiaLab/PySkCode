"""
SkCode tables tag definitions code.
"""

from .base import TagOptions


class TableTagOptions(TagOptions):
    """ Table tag options container class. """

    # CSS class name for the table
    css_class_name = 'table table-condensed table-striped'

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<table class="%s">%s</table>\n' % (self.css_class_name, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text


class TableRowTagOptions(TagOptions):
    """ Table row tag options container class. """

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return '<tr>%s</tr>\n' % inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text


class TableCellTagOptions(TagOptions):
    """ Table tag options container class. """

    make_paragraphs_here = True

    # Column span attribute name
    colspan_attr_name = 'colspan'

    # Row span attribute name
    rowspan_attr_name = 'rowspan'

    def get_cell_colspan(self, tree_node):
        """
        Return the column span value of this cell.
        :param tree_node: The current tree node instance.
        :return The column span value of this cell, or 1.
        """

        # Get the raw string value
        user_colspan = tree_node.attrs.get(self.colspan_attr_name, '')

        # Shortcut if no value
        if not user_colspan:
            return 1

        # If set, turn the string into an int
        try:
            user_colspan = int(user_colspan)
            return user_colspan if user_colspan > 1 else 1
        except ValueError:
            return 1

    def get_cell_rowspan(self, tree_node):
        """
        Return the row span value of this cell.
        :param tree_node: The current tree node instance.
        :return The row span value of this cell, or 1.
        """

        # Get the raw string value
        user_rowspan = tree_node.attrs.get(self.rowspan_attr_name, '')

        # Shortcut if no value
        if not user_rowspan:
            return 1

        # If set, turn the string into an int
        try:
            user_rowspan = int(user_rowspan)
            return user_rowspan if user_rowspan > 1 else 1
        except ValueError:
            return 1

    def get_html_extra_attrs(self, tree_node):
        """
        Return any extra attributes for the HTML rendering.
        :param tree_node: The current tree node instance.
        :return Any extra attributes for the HTML rendering.
        """

        # Get the column span
        colspan = self.get_cell_colspan(tree_node)
        extra_attrs = ' colspan="%d"' % colspan if colspan != 1 else ''

        # Get the row span
        rowspan = self.get_cell_rowspan(tree_node)
        if rowspan != 1:
            extra_attrs += ' rowspan="%d"' % rowspan

        # Return the string
        return extra_attrs

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        extra_attrs = self.get_html_extra_attrs(tree_node)
        return '<td%s>%s</td>\n' % (extra_attrs, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """
        # Get the column and row span
        colspan = self.get_cell_colspan(tree_node)
        rowspan = self.get_cell_rowspan(tree_node)
        return {
                   self.colspan_attr_name: str(colspan) if colspan != 1 else '',
                   self.rowspan_attr_name: str(rowspan) if rowspan != 1 else ''
               }, None


class TableHeaderCellTagOptions(TableCellTagOptions):
    """ Table tag options container class. """

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        extra_attrs = self.get_html_extra_attrs(tree_node)
        return '<th%s>%s</th>\n' % (extra_attrs, inner_html)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text
