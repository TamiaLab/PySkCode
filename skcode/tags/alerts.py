"""
SkCode alert box tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions


# Alert types
ALERT_TYPE_ERROR = 'error'
ALERT_TYPE_DANGER = 'danger'
ALERT_TYPE_WARNING = 'warning'
ALERT_TYPE_INFO = 'info'
ALERT_TYPE_SUCCESS = 'success'
ALERT_TYPE_NOTE = 'note'
ALERT_TYPE_QUESTION = 'question'


class AlertBoxTagOptions(TagOptions):
    """ Alert box tag options container class. """

    make_paragraphs_here = True

    # Accepted alert types list
    accepted_types = (ALERT_TYPE_ERROR,
                      ALERT_TYPE_DANGER,
                      ALERT_TYPE_WARNING,
                      ALERT_TYPE_INFO,
                      ALERT_TYPE_SUCCESS,
                      ALERT_TYPE_NOTE,
                      ALERT_TYPE_QUESTION)

    # Default alert type if not specified
    default_type = ALERT_TYPE_INFO

    # HTML templates for all alert types
    html_template = {

        ALERT_TYPE_ERROR: """<div class="panel panel-danger">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-exclamation-circle"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_DANGER: """<div class="panel panel-danger">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-heartbeat"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_WARNING: """<div class="panel panel-warning">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-exclamation-triangle"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_INFO: """<div class="panel panel-info">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-info-circle"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_SUCCESS: """<div class="panel panel-success">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-check-square-o"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_NOTE: """<div class="panel panel-primary">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-pencil-square-o"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_QUESTION: """<div class="panel panel-primary">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-question-circle"></i> %(title)s</h3>
    </div>
    <div class="panel-body">
        %(inner_html)s
    </div>
</div>
"""
    }

    # HTML templates (without title) for all alert types
    html_template_without_title = {

        ALERT_TYPE_ERROR: """<div class="panel panel-danger">
    <div class="panel-body">
        <i class="fa fa-exclamation-circle text-danger"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_DANGER: """<div class="panel panel-danger">
    <div class="panel-body">
        <i class="fa fa-heartbeat text-danger"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_WARNING: """<div class="panel panel-warning">
    <div class="panel-body">
        <i class="fa fa-exclamation-triangle text-warning"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_INFO: """<div class="panel panel-info">
    <div class="panel-body">
        <i class="fa fa-info-circle text-info"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_SUCCESS: """<div class="panel panel-success">
    <div class="panel-body">
        <i class="fa fa-check-square-o text-success"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_NOTE: """<div class="panel panel-primary">
    <div class="panel-body">
        <i class="fa fa-pencil-square-o text-primary"></i> %(inner_html)s
    </div>
</div>
""",

        ALERT_TYPE_QUESTION: """<div class="panel panel-primary">
    <div class="panel-body">
        <i class="fa fa-question-circle text-primary"></i> %(inner_html)s
    </div>
</div>
"""
    }

    # Text templates for the title of all alert types
    text_title_line_template = {
        ALERT_TYPE_ERROR: "(!) %(title)s",
        ALERT_TYPE_DANGER: "/!!\\ %(title)s",
        ALERT_TYPE_WARNING: "/!\\ %(title)s",
        ALERT_TYPE_INFO: "(i) %(title)s",
        ALERT_TYPE_SUCCESS: "[x] %(title)s",
        ALERT_TYPE_NOTE: "(\u2026) %(title)s",
        ALERT_TYPE_QUESTION: "(?) %(title)s"
    }

    # Alert type attribute name
    alert_type_attr_name = 'type'

    # Alert title attribute name
    alert_title_attr_name = 'title'

    def get_alert_type(self, tree_node):
        """
        Return the type of this alert.
        The type can be set by setting the ``alert_type_attr_name`` attribute of the tag.
        :param tree_node: The current tree node instance.
        :return The alert type if set, or the default type.
        """
        user_alert_type = tree_node.attrs.get(self.alert_type_attr_name, self.default_type)
        user_alert_type = user_alert_type.lower()
        return user_alert_type if user_alert_type in self.accepted_types else self.default_type

    def get_alert_title(self, tree_node):
        """
        Return the title of this alert.
        The title can be set by setting the ``alert_title_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``alert_title_attr_name``.
        :param tree_node: The current tree node instance.
        :return The alert title if set or an empty string.
        """
        alert_title = tree_node.attrs.get(tree_node.name, '')
        if not alert_title:
            alert_title = tree_node.attrs.get(self.alert_title_attr_name, '')
        return unescape_html_entities(alert_title)

    def get_alert_html_template(self, alert_type, alert_title):
        """
        Return the HTML template for this alert..
        :param alert_type: The alert type.
        :param alert_title: The alert title.
        :return The HTML template to be used for this alert.
        """
        return self.html_template[alert_type] if alert_title else self.html_template_without_title[alert_type]

    def get_alert_text_title_line_template(self, alert_type):
        """
        Return the (text) title line template for this alert.
        :param alert_type: The alert type.
        :return The text template to be used for this alert title line.
        """
        return self.text_title_line_template[alert_type]

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the alert variables
        alert_type = self.get_alert_type(tree_node)
        alert_title = self.get_alert_title(tree_node)
        alert_html_template = self.get_alert_html_template(alert_type, alert_title)

        # Render the alert
        context = {
            'type': alert_type,
            'title': escape_html(alert_title),
            'inner_html': inner_html.strip(),
        }
        return alert_html_template % context

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the alert variables
        alert_type = self.get_alert_type(tree_node)
        alert_title = self.get_alert_title(tree_node)
        alert_text_title_line_template = self.get_alert_text_title_line_template(alert_type)

        # Render the alert title line
        lines = ['*** ' + alert_text_title_line_template % {'title': alert_title}]

        # Render all inner lines
        for line in inner_text.strip().splitlines():
            lines.append('* ' + line)
        lines.append('***')
        lines.append('')
        return '\n'.join(lines)

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """

        # Get the alert type and title
        alert_type = self.get_alert_type(tree_node)
        alert_title = self.get_alert_title(tree_node)
        return {
                   self.alert_type_attr_name: alert_type,
                   self.alert_title_attr_name: alert_title
               }, self.alert_title_attr_name


class FixedAlertBoxTagOptions(AlertBoxTagOptions):
    """ Fixed type alert box tag options container class. """

    def __init__(self, alert_type, **kwargs):
        """
        Alert box tag with fixed type.
        :param alert_type: The fixed alert type.
        :param kwargs: Keyword arguments for super constructor.
        """
        assert alert_type, "Alert type is mandatory."
        super(FixedAlertBoxTagOptions, self).__init__(**kwargs)
        self.alert_type = alert_type

    def get_alert_type(self, tree_node):
        """
        Return the type of this alert.
        :param tree_node: The current tree node instance.
        :return The alert type, as set at ``__init__``.
        """
        return self.alert_type

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Callback function for retrieving all attributes required for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tagvalue
        attribute name for the shortcut syntax (if required). Example: {'title': 'foobar'}, 'title'
        """

        # Get the alert title
        alert_title = self.get_alert_title(tree_node)
        return {
                   self.alert_title_attr_name: alert_title
               }, self.alert_title_attr_name
