"""
SkCode alert box tag definitions code.
"""

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions
from ..tools import escape_attrvalue


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

    # Text templates for the title of all alert types
    text_title_line_template = {
        ALERT_TYPE_ERROR: "(!) %s",
        ALERT_TYPE_DANGER: "/!!\ %s",
        ALERT_TYPE_WARNING: "/!\ %s",
        ALERT_TYPE_INFO: "(i) %s",
        ALERT_TYPE_SUCCESS: "[x] %s",
        ALERT_TYPE_NOTE: "(\u2026) %s",
        ALERT_TYPE_QUESTION: "(?) %s"
    }

    # Default titles if not specified ()
    default_titles = {
        ALERT_TYPE_ERROR: "Erreur à éviter",
        ALERT_TYPE_DANGER: "Attention Danger !",
        ALERT_TYPE_WARNING: "Attention !",
        ALERT_TYPE_INFO: "Information",
        ALERT_TYPE_SUCCESS: "Et voila",
        ALERT_TYPE_NOTE: "Nota Bene",
        ALERT_TYPE_QUESTION: "Question"
    }

    # Alert type attribute name
    alert_type_attr_name = 'type'

    # Alert title attribute name
    alert_title_attr_name = 'title'

    def get_alert_type(self, tree_node):
        """
        Return the type of this alert.
        The type can be set by setting the alert_type_attr_name attribute of the tag.
        :param tree_node: The current tree node instance.
        :return The alert type if set, or the default type.
        """
        user_alert_type = tree_node.attrs.get(self.alert_type_attr_name, self.default_type)
        if user_alert_type in self.accepted_types:
            return user_alert_type
        else:
            return self.default_type
 
    def get_alert_title(self, tree_node, alert_type, use_defaults=True):
        """
        Return the title of this alert.
        The title can be set by setting the alert_title_attr_name attribute of the tag or simply
        by setting the tag name attribute.
        The lookup order is: tag name (first), alert_title_attr_name.
        :param tree_node: The current tree node instance.
        :param alert_type: The alert type.
        :param use_defaults: Set to True to get a default title string if no user-supplied title is available,
        set to False to get an empty string (default to True).
        :return The alert title if set, or a default title string, or an empty string if use_defaults is False.
        """
        alert_title = tree_node.attrs.get(tree_node.name, '')
        if not alert_title:
            alert_title = tree_node.attrs.get(self.alert_title_attr_name, '')
        if not alert_title and use_defaults:
            return self.default_titles[alert_type]
        else:
            return unescape_html_entities(alert_title)

    def get_alert_html_template(self, tree_node, alert_type, alert_title):
        """
        Return the HTML template for this alert.
        :param tree_node: The current tree node instance.
        :param alert_type: The alert type.
        :param alert_title: The alert title.
        :return The HTML template to be used for this alert.
        """
        return self.html_template[alert_type]

    def get_alert_text_title_line_template(self, tree_node, alert_type, alert_title):
        """
        Return the (text) title line template for this alert.
        :param tree_node: The current tree node instance.
        :param alert_type: The alert type.
        :param alert_title: The alert title.
        :return The text template to be used for this alert title line.
        """
        return self.text_title_line_template[alert_type]

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: Ignored.
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the alert variables
        alert_type = self.get_alert_type(tree_node)
        alert_title = self.get_alert_title(tree_node, alert_type)
        alert_html_template = self.get_alert_html_template(tree_node, alert_type, alert_title)

        # Render the alert
        context = {
            'type': alert_type,
            'title': escape_html(alert_title),
            'inner_html': inner_html.strip(),
        }
        return alert_html_template % context

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """
        
        # Get the alert variables
        alert_type = self.get_alert_type(tree_node)
        alert_title = self.get_alert_title(tree_node, alert_type)
        alert_text_title_line_template = self.get_alert_text_title_line_template(
            tree_node, alert_type, alert_title)

        # Render the alert title line
        lines = ['*** ' + (alert_text_title_line_template % alert_title)]

        # Render all inner lines
        for line in inner_text.strip().splitlines():
            lines.append('* ' + line)
        lines.append('***')
        lines.append('')
        return '\n'.join(lines)

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the alert type
        alert_type = self.get_alert_type(tree_node)
        extra_attrs = ' %s=%s' % (self.alert_type_attr_name,
                                  escape_attrvalue(alert_type))

        # Get the alert title
        alert_title = self.get_alert_title(tree_node, alert_type, use_defaults=False)
        if alert_title:
            extra_attrs += ' %s=%s' % (self.alert_title_attr_name,
                                       escape_attrvalue(alert_title))

        # Return the code
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, inner_skcode, node_name)


class FixedAlertBoxTagOptions(AlertBoxTagOptions):
    """ Fixed type alert box tag options container class. """

    def __init__(self, alert_type, **kwargs):
        """
        Alert box tag with fixed type.
        :param alert_type: Alert type.
        :param kwargs: Keyword arguments for super constructor.
        """
        super(FixedAlertBoxTagOptions, self).__init__(**kwargs)
        self.alert_type = alert_type

    def get_alert_type(self, tree_node):
        """
        Return the type of this alert.
        :param tree_node: The current tree node instance.
        :return The alert type, as set at __init__.
        """
        return self.alert_type

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the alert title
        alert_title = self.get_alert_title(tree_node, self.alert_type, use_defaults=False)
        if alert_title:
            extra_attrs = ' %s=%s' % (self.alert_title_attr_name,
                                      escape_attrvalue(alert_title))
        else:
            extra_attrs = ''

        # Return the code
        tagname = tree_node.name
        return '[%s%s]%s[/%s]' % (tagname, extra_attrs, inner_skcode, tagname)
