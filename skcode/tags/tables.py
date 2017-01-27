"""
SkCode tables tag definitions code.
"""

from gettext import gettext as _

from ..etree import TreeNode


class TableTreeNode(TreeNode):
    """ Table tree node class. """

    canonical_tag_name = 'table'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<table class="{class_name}">{inner_html}</table>\n'

    # CSS class name for the table
    css_class_name = 'table table-condensed table-striped'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(class_name=self.css_class_name, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text


class TableRowTreeNode(TreeNode):
    """ Table row tree node class. """

    canonical_tag_name = 'tr'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<tr>{inner_html}</tr>\n'

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        return self.html_render_template.format(inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text


class TableCellTreeNode(TreeNode):
    """ Table tree node class. """

    canonical_tag_name = 'td'
    alias_tag_names = ()

    make_paragraphs_here = True

    # HTML template for rendering
    html_render_template = '<td{extra_args}>{inner_html}</td>\n'

    # Column span attribute name
    colspan_attr_name = 'colspan'

    # Row span attribute name
    rowspan_attr_name = 'rowspan'

    def get_cell_colspan(self):
        """
        Return the column span value of this cell.
        :return The column span value of this cell, or 1.
        """

        # Get the raw string value
        user_colspan = self.attrs.get(self.colspan_attr_name, '')

        # Shortcut if no value
        if not user_colspan:
            return 1

        # If set, turn the string into an int
        try:
            user_colspan = int(user_colspan)
            if user_colspan > 1:
                return user_colspan
            else:
                self.error_message = _('Column span must be greater than 1')
        except ValueError:
            self.error_message = _('{} is not a number').format(user_colspan)
            return 1
        return 1

    def get_cell_rowspan(self):
        """
        Return the row span value of this cell.
        :return The row span value of this cell, or 1.
        """

        # Get the raw string value
        user_rowspan = self.attrs.get(self.rowspan_attr_name, '')

        # Shortcut if no value
        if not user_rowspan:
            return 1

        # If set, turn the string into an int
        try:
            user_rowspan = int(user_rowspan)
            if user_rowspan > 1:
                return user_rowspan
            else:
                self.error_message = _('Row span must be greater than 1')
        except ValueError:
            self.error_message = _('{} is not a number').format(user_rowspan)
            return 1
        return 1

    def get_html_extra_attrs(self):
        """
        Return any extra attributes for the HTML rendering.
        """

        # Get the column span
        colspan = self.get_cell_colspan()
        extra_attrs = ' colspan="{:d}"'.format(colspan) if colspan != 1 else ''

        # Get the row span
        rowspan = self.get_cell_rowspan()
        if rowspan != 1:
            extra_attrs += ' rowspan="{:d}"'.format(rowspan)

        # Return the string
        return extra_attrs

    def sanitize_node(self, breadcrumb):
        """
        Callback function for sanitizing and cleaning-up the given node.
        :param breadcrumb: The breadcrumb of node instances from the root node to the current node (excluded).
        """
        super(TableCellTreeNode, self).sanitize_node(breadcrumb)
        self.get_cell_colspan()
        self.get_cell_rowspan()

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """
        extra_attrs = self.get_html_extra_attrs()
        return self.html_render_template.format(extra_args=extra_attrs, inner_html=inner_html)

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """
        # TODO But how?
        return inner_text


class TableHeaderCellTreeNode(TableCellTreeNode):
    """ Table tree node class. """

    canonical_tag_name = 'th'
    alias_tag_names = ()

    # HTML template for rendering
    html_render_template = '<th{extra_args}>{inner_html}</th>\n'
