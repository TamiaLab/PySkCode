"""
SkCode tables tag definitions code.
"""

from .base import TagOptions


class TableTagOptions(TagOptions):
    """ Table tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<table>%s</table>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        # TODO But how?
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class TableRowTagOptions(TagOptions):
    """ Table row tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        return '<tr>%s</tr>\n' % inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        # TODO But how?
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        node_name = tree_node.name
        return '[%s]%s[/%s]' % (node_name, inner_skcode, node_name)


class TableCellOptions(TagOptions):
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
            if user_colspan < 1:
                user_colspan = 1
        except ValueError:
            user_colspan = 1

        # Return the result
        return user_colspan

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
            if user_rowspan < 1:
                user_rowspan = 1
        except ValueError:
            user_rowspan = 1

        # Return the result
        return user_rowspan

    def get_html_extra_attrs(self, tree_node):
        """
        Return any extra attributes for the HTML rendering.
        :param tree_node: The current tree node instance.
        :return Any extra attributes for the HTML rendering.
        """

        # Get the column span
        colspan = self.get_cell_colspan(tree_node)
        if colspan:
            extra_attrs = ' colspan="%d"' % colspan
        else:
            extra_attrs = ''

        # Get the row span
        rowspan = self.get_cell_rowspan(tree_node)
        if rowspan:
            extra_attrs += ' rowspan="%d"' % rowspan

        # Return the string
        return extra_attrs

    def get_skcode_extra_attrs(self, tree_node):
        """
        Return any extra attributes for the SkCode rendering.
        :param tree_node: The current tree node instance.
        :return Any extra attributes for the SkCode rendering.
        """

        # Get the column span
        colspan = self.get_cell_colspan(tree_node)
        if colspan:
            extra_attrs = ' %s="%d"' % (self.colspan_attr_name, colspan)
        else:
            extra_attrs = ''

        # Get the row span
        rowspan = self.get_cell_rowspan(tree_node)
        if rowspan:
            extra_attrs += ' %s="%d"' % (self.rowspan_attr_name, rowspan)

        # Return the string
        return extra_attrs

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        extra_attrs = self.get_html_extra_attrs(tree_node)
        return '<td%s>%s</td>\n' % (extra_attrs, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        # TODO But how?
        return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """
        extra_attrs = self.get_html_extra_attrs(tree_node)
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)


class TableHeaderCellTagOptions(TableCellOptions):
    """ Table tag options container class. """

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """
        extra_attrs = self.get_html_extra_attrs(tree_node)
        return '<th%s>%s</th>\n' % (extra_attrs, inner_html)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        # TODO But how?
        return inner_text
