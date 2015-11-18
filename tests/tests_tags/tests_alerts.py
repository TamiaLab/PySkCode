"""
SkCode alerts tag test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import (AlertBoxTagOptions,
                         FixedAlertBoxTagOptions,
                         ALERT_TYPE_ERROR,
                         ALERT_TYPE_DANGER,
                         ALERT_TYPE_WARNING,
                         ALERT_TYPE_INFO,
                         ALERT_TYPE_SUCCESS,
                         ALERT_TYPE_NOTE,
                         ALERT_TYPE_QUESTION,
                         DEFAULT_RECOGNIZED_TAGS)


class AlertsTagtestCase(unittest.TestCase):
    """ Tests suite for the alerts tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('alert', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['alert'], AlertBoxTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = AlertBoxTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertTrue(opts.make_paragraphs_here)
        self.assertEqual(opts.accepted_types, (ALERT_TYPE_ERROR,
                                               ALERT_TYPE_DANGER,
                                               ALERT_TYPE_WARNING,
                                               ALERT_TYPE_INFO,
                                               ALERT_TYPE_SUCCESS,
                                               ALERT_TYPE_NOTE,
                                               ALERT_TYPE_QUESTION))
        self.assertEqual(opts.default_type, ALERT_TYPE_INFO)
        # html_template, text_title_line_template, default_titles not tested
        self.assertEqual(opts.alert_type_attr_name, 'type')
        self.assertEqual(opts.alert_title_attr_name, 'title')

    def test_get_alert_type(self):
        """ Test the ``get_alert_type`` method with a valid alert type. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'type': ALERT_TYPE_ERROR})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual('error', alert_type)

    def test_get_alert_type_without_type(self):
        """ Test the ``get_alert_type`` method without an alert type. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual(opts.default_type, alert_type)

    def test_get_alert_type_with_invalid_type(self):
        """ Test the ``get_alert_type`` method with an invalid alert type. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'type': 'johndoe'})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual(opts.default_type, alert_type)

    def test_get_alert_title_with_tagname_set(self):
        """ Test the ``get_alert_title`` with the tag name attribute set. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'alert': 'test'})
        title = opts.get_alert_title(tree_node, ALERT_TYPE_ERROR)
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_set(self):
        """ Test the ``get_alert_title`` with the "title" attribute set. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'test'})
        title = opts.get_alert_title(tree_node, ALERT_TYPE_ERROR)
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_and_tagname_set(self):
        """ Test the ``get_alert_title`` with the "title" and tag name attribute set. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'test', 'alert': 'test2'})
        title = opts.get_alert_title(tree_node, ALERT_TYPE_ERROR)
        self.assertEqual('test2', title)

    def test_get_alert_title_with_default_value(self):
        """ Test the ``get_alert_title`` with no title set. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        for alert_type in opts.accepted_types:
            title = opts.get_alert_title(tree_node, alert_type)
            self.assertEqual(opts.default_titles[alert_type], title)

    def test_get_alert_title_with_default_value_disabled(self):
        """ Test the ``get_alert_title`` with no title set and default title disabled. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        for alert_type in opts.accepted_types:
            title = opts.get_alert_title(tree_node, alert_type, use_defaults=False)
            self.assertEqual('', title)

    def test_get_alert_title_with_html_entities(self):
        """ Test the ``get_alert_title`` when the title contain HTML entities. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={'title': '&lt;test&gt;'})
        title = opts.get_alert_title(tree_node, ALERT_TYPE_ERROR)
        self.assertEqual('<test>', title)

    def test_get_alert_html_template_method(self):
        """ Test the ``get_alert_html_template`` method. """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        for alert_type in opts.accepted_types:
            html_template = opts.get_alert_html_template(tree_node, alert_type, 'test')
            self.assertEqual(opts.html_template[alert_type], html_template)

    def test_get_alert_text_title_line_template_method(self):
        """ Test the ``get_alert_text_title_line_template`` """
        opts = AlertBoxTagOptions()
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        for alert_type in opts.accepted_types:
            html_template = opts.get_alert_text_title_line_template(tree_node, alert_type, 'test')
            self.assertEqual(opts.text_title_line_template[alert_type], html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'Test alert', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template[alert_type] % {
                'type': alert_type,
                'title': 'Test alert',
                'inner_html': 'Hello world!',
            }
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_trailing_newline(self):
        """ Test HTML rendering with trailing newline. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'Test alert', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, '\n\nHello world!\n')
            expected_output = AlertBoxTagOptions.html_template[alert_type] % {
                'type': alert_type,
                'title': 'Test alert',
                'inner_html': 'Hello world!',
            }
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title(self):
        """ Test HTML rendering without title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template[alert_type] % {
                'type': alert_type,
                'title': AlertBoxTagOptions.default_titles[alert_type],
                'inner_html': 'Hello world!',
            }
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities_in_title(self):
        """ Test HTML rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': '<Test alert>', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template[alert_type] % {
                'type': alert_type,
                'title': '&lt;Test alert&gt;',
                'inner_html': 'Hello world!',
            }
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'Test alert', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!')
            expected_output = """*** %s
* Hello world!
***
""" % (AlertBoxTagOptions.text_title_line_template[alert_type] % 'Test alert')
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_trailing_newline(self):
        """ Test text rendering with trailing newline. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'Test alert', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, '\n\nHello world!\n')
            expected_output = """*** %s
* Hello world!
***
""" % (AlertBoxTagOptions.text_title_line_template[alert_type] % 'Test alert')
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title(self):
        """ Test text rendering without title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!')
            expected_output = """*** %s
* Hello world!
***
""" % (AlertBoxTagOptions.text_title_line_template[alert_type] % AlertBoxTagOptions.default_titles[alert_type])
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities_in_title(self):
        """ Test text rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': '<Test alert>', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!')
            expected_output = """*** %s
* Hello world!
***
""" % (AlertBoxTagOptions.text_title_line_template[alert_type] % '<Test alert>')
            self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': 'Test alert', 'type': alert_type})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[alert type="%s" title="Test alert"]Hello world![/alert]' % alert_type
            self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering_without_title(self):
        """ Test SkCode rendering without title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[alert type="%s"]Hello world![/alert]' % alert_type
            self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering_with_html_entities_in_title(self):
        """ Test SkCode rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = TreeNode(None, 'alert', opts, attrs={'title': '<Test alert>', 'type': alert_type})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[alert type="%s" title="<Test alert>"]Hello world![/alert]' % alert_type
            self.assertEqual(expected_output, rendered_output)


class FixedTypeAlertsTagtestCase(unittest.TestCase):
    """ Tests suite for the fixed type alerts tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('error', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['error'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['error'].alert_type, ALERT_TYPE_ERROR)
        self.assertIn('danger', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['danger'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['danger'].alert_type, ALERT_TYPE_DANGER)
        self.assertIn('warning', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['warning'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['warning'].alert_type, ALERT_TYPE_WARNING)
        self.assertIn('info', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['info'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['info'].alert_type, ALERT_TYPE_INFO)
        self.assertIn('success', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['success'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['success'].alert_type, ALERT_TYPE_SUCCESS)
        self.assertIn('note', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['note'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['note'].alert_type, ALERT_TYPE_NOTE)
        self.assertIn('question', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['question'], FixedAlertBoxTagOptions)
        self.assertEqual(DEFAULT_RECOGNIZED_TAGS['question'].alert_type, ALERT_TYPE_QUESTION)

    def test_get_alert_type_method(self):
        """ Test the ``get_alert_type`` method. """
        opts = FixedAlertBoxTagOptions('johndoe')
        tree_node = TreeNode(None, 'alert', opts, attrs={})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual('johndoe', alert_type)

    def test_skcode_rendering(self):
        """ Test SkCode rendering. """
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = TreeNode(None, alert_type, opts, attrs={'title': 'Test alert'})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[%s title="Test alert"]Hello world![/%s]' % (alert_type, alert_type)
            self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering_without_title(self):
        """ Test SkCode rendering without title. """
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = TreeNode(None, alert_type, opts, attrs={})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[%s]Hello world![/%s]' % (alert_type, alert_type)
            self.assertEqual(expected_output, rendered_output)

    def test_skcode_rendering_with_html_entities_in_title(self):
        """ Test SkCode rendering with HTML entities in title. """
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = TreeNode(None, alert_type, opts, attrs={'title': '<Test alert>'})
            rendered_output = opts.render_skcode(tree_node, 'Hello world!')
            expected_output = '[%s title="<Test alert>"]Hello world![/%s]' % (alert_type, alert_type)
            self.assertEqual(expected_output, rendered_output)
