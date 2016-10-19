"""
SkCode alert box tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from ..etree import TreeNode


# Alert types
ALERT_TYPE_ERROR = 'error'
ALERT_TYPE_DANGER = 'danger'
ALERT_TYPE_WARNING = 'warning'
ALERT_TYPE_INFO = 'info'
ALERT_TYPE_SUCCESS = 'success'
ALERT_TYPE_NOTE = 'note'
ALERT_TYPE_QUESTION = 'question'


class AlertBoxTreeNode(TreeNode):
    """ Alert box tree node class. """

    make_paragraphs_here = True

    canonical_tag_name = 'alert'
    alias_tag_names = ()

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
        <h3 class="panel-title"><i class="fa fa-exclamation-circle" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_DANGER: """<div class="panel panel-danger">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-heartbeat" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_WARNING: """<div class="panel panel-warning">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_INFO: """<div class="panel panel-info">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-info-circle" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_SUCCESS: """<div class="panel panel-success">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-check-square-o" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_NOTE: """<div class="panel panel-primary">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
""",

        ALERT_TYPE_QUESTION: """<div class="panel panel-primary">
    <div class="panel-heading">
        <h3 class="panel-title"><i class="fa fa-question-circle" aria-hidden="true"></i> {title}</h3>
    </div>
    <div class="panel-body">
        {inner_html}
    </div>
</div>
"""
    }

    # HTML templates (without title) for all alert types
    html_template_without_title = {

        ALERT_TYPE_ERROR: """<div class="panel panel-danger">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-exclamation-circle text-danger" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_DANGER: """<div class="panel panel-danger">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-heartbeat text-danger" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_WARNING: """<div class="panel panel-warning">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-exclamation-triangle text-warning" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_INFO: """<div class="panel panel-info">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-info-circle text-info" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_SUCCESS: """<div class="panel panel-success">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-check-square-o text-success" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_NOTE: """<div class="panel panel-primary">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-pencil-square-o text-primary" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
""",

        ALERT_TYPE_QUESTION: """<div class="panel panel-primary">
    <div class="panel-body">
        <div class="media">
            <div class="media-left media-middle">
                <i class="fa fa-question-circle text-primary" aria-hidden="true"></i>
            </div>
            <div class="media-body">
                {inner_html}
            </div>
        </div>
    </div>
</div>
"""
    }

    # Text templates for the title of all alert types
    text_title_line_template = {
        ALERT_TYPE_ERROR: "(!) {title}",
        ALERT_TYPE_DANGER: "/!!\\ {title}",
        ALERT_TYPE_WARNING: "/!\\ {title}",
        ALERT_TYPE_INFO: "(i) {title}",
        ALERT_TYPE_SUCCESS: "[x] {title}",
        ALERT_TYPE_NOTE: "(\u2026) {title}",
        ALERT_TYPE_QUESTION: "(?) {title}"
    }

    # Alert type attribute name
    alert_type_attr_name = 'type'

    # Alert title attribute name
    alert_title_attr_name = 'title'

    def get_alert_type(self):
        """
        Return the type of this alert.
        The type can be set by setting the ``alert_type_attr_name`` attribute of the tag.
        :return The alert type if set, or the default type.
        """
        user_alert_type = self.attrs.get(self.alert_type_attr_name, self.default_type)
        user_alert_type = user_alert_type.lower()
        return user_alert_type if user_alert_type in self.accepted_types else self.default_type

    def get_alert_title(self):
        """
        Return the title of this alert.
        The title can be set by setting the ``alert_title_attr_name`` attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), ``alert_title_attr_name``.
        :return The alert title if set or an empty string.
        """
        alert_title = self.attrs.get(self.name, '')
        if not alert_title:
            alert_title = self.attrs.get(self.alert_title_attr_name, '')
        return unescape_html_entities(alert_title)

    def get_alert_html_template(self, alert_type, alert_title):
        """
        Return the HTML template for this alert..
        :param alert_type: The alert type.
        :param alert_title: The alert title.
        :return The HTML template to be used for this alert.
        """
        if alert_title:
            return self.html_template[alert_type]
        else:
            return self.html_template_without_title[alert_type]

    def get_alert_text_title_line_template(self, alert_type):
        """
        Return the text title line template for this alert.
        :param alert_type: The alert type.
        :return The text template to be used for this alert title line.
        """
        return self.text_title_line_template[alert_type]

    def render_html(self, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the alert variables
        alert_type = self.get_alert_type()
        alert_title = self.get_alert_title()
        alert_html_template = self.get_alert_html_template(alert_type, alert_title)

        # Render the alert
        return alert_html_template.format(type=alert_type,
                                          title=escape_html(alert_title),
                                          inner_html=inner_html.strip())

    def render_text(self, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the alert variables
        alert_type = self.get_alert_type()
        alert_title = self.get_alert_title()
        alert_text_title_line_template = self.get_alert_text_title_line_template(alert_type)

        # Render the alert title line
        lines = ['*** ' + alert_text_title_line_template.format(title=alert_title)]

        # Render all inner lines
        for line in inner_text.strip().splitlines():
            lines.append('* ' + line)
        lines.append('***')
        lines.append('')
        return '\n'.join(lines)


def generate_fixed_alert_type_cls(alert_type,
                                  canonical_tag_name=None,
                                  alias_tag_names=None):
    """
    Generate a fixed alert type class at runtime.
    :param alert_type: The desired fixed alert type.
    :param canonical_tag_name: The canonical name of the tag.
    :param alias_tag_names: The name alias of the tag
    :return: The generated class type.
    """
    assert alert_type, "Alert type is mandatory."
    _canonical_tag_name = canonical_tag_name or alert_type
    _alias_tag_names = alias_tag_names or ()
    _alert_type = alert_type

    class FixedTypeAlertBoxTreeNode(AlertBoxTreeNode):
        """ Fixed type alert box tree node class. """

        canonical_tag_name = _canonical_tag_name
        alias_tag_names = _alias_tag_names
        alert_type = _alert_type

        def get_alert_type(self):
            """
            Return the type of this alert.
            :return The alert type, as set at ``self.alert_type``.
            """
            return self.alert_type

    return FixedTypeAlertBoxTreeNode
