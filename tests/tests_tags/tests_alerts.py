"""
SkCode alert box tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         AlertBoxTagOptions,
                         FixedAlertBoxTagOptions,
                         ALERT_TYPE_ERROR,
                         ALERT_TYPE_DANGER,
                         ALERT_TYPE_WARNING,
                         ALERT_TYPE_INFO,
                         ALERT_TYPE_SUCCESS,
                         ALERT_TYPE_NOTE,
                         ALERT_TYPE_QUESTION,
                         DEFAULT_RECOGNIZED_TAGS)


class AlertBoxTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the alerts tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the default dictionary of recognized tags. """
        self.assertIn('alert', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['alert'], AlertBoxTagOptions)

    def test_module_constant_values(self):
        """ Test module level constants """
        self.assertEqual('error', ALERT_TYPE_ERROR)
        self.assertEqual('danger', ALERT_TYPE_DANGER)
        self.assertEqual('warning', ALERT_TYPE_WARNING)
        self.assertEqual('info', ALERT_TYPE_INFO)
        self.assertEqual('success', ALERT_TYPE_SUCCESS)
        self.assertEqual('note', ALERT_TYPE_NOTE)
        self.assertEqual('question', ALERT_TYPE_QUESTION)

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
        self.assertEqual('alert', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertEqual((ALERT_TYPE_ERROR,
                          ALERT_TYPE_DANGER,
                          ALERT_TYPE_WARNING,
                          ALERT_TYPE_INFO,
                          ALERT_TYPE_SUCCESS,
                          ALERT_TYPE_NOTE,
                          ALERT_TYPE_QUESTION), opts.accepted_types)
        self.assertEqual(ALERT_TYPE_INFO, opts.default_type)
        # String values of ``html_template``, ``html_template_without_title``, ``text_title_line_template``
        # and ``default_titles`` are NOT tested.
        self.assertIn(ALERT_TYPE_ERROR, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_ERROR])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_DANGER])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_WARNING])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_INFO])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_SUCCESS])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_NOTE])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, opts.html_template)
        self.assertIn('{title}', opts.html_template[ALERT_TYPE_QUESTION])
        self.assertIn('{inner_html}', opts.html_template[ALERT_TYPE_QUESTION])

        self.assertIn(ALERT_TYPE_ERROR, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_ERROR])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_DANGER])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_WARNING])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_INFO])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_SUCCESS])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_NOTE])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, opts.html_template_without_title)
        self.assertNotIn('{title}', opts.html_template_without_title[ALERT_TYPE_QUESTION])
        self.assertIn('{inner_html}', opts.html_template_without_title[ALERT_TYPE_QUESTION])

        self.assertIn(ALERT_TYPE_ERROR, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, opts.text_title_line_template)
        self.assertIn('{title}', opts.text_title_line_template[ALERT_TYPE_QUESTION])
        self.assertEqual('type', opts.alert_type_attr_name)
        self.assertEqual('title', opts.alert_title_attr_name)

    def test_get_alert_type(self):
        """ Test the ``get_alert_type`` method with a valid alert type. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for known_alert_type in opts.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': known_alert_type})
            alert_type = opts.get_alert_type(tree_node)
            self.assertEqual(known_alert_type, alert_type)

    def test_get_alert_type_uppercase(self):
        """ Test the ``get_alert_type`` method with a valid alert type but in uppercase. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'type': 'ERRor'})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual('error', alert_type)

    def test_get_alert_type_without_type(self):
        """ Test the ``get_alert_type`` method without an alert type. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual(opts.default_type, alert_type)

    def test_get_alert_type_with_invalid_type(self):
        """ Test the ``get_alert_type`` method with an invalid alert type. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'type': 'notatype'})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual(opts.default_type, alert_type)

    def test_get_alert_title_with_tagname_set(self):
        """ Test the ``get_alert_title`` with the tag name attribute set. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'alert': 'test'})
        title = opts.get_alert_title(tree_node)
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_set(self):
        """ Test the ``get_alert_title`` with the "title" attribute set. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'test'})
        title = opts.get_alert_title(tree_node)
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_and_tagname_set(self):
        """ Test the ``get_alert_title`` with the "title" and tag name attribute set. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'alert': 'test', 'title': 'test2'})
        title = opts.get_alert_title(tree_node)
        self.assertEqual('test', title)

    def test_get_alert_title_with_default_value(self):
        """ Test the ``get_alert_title`` with no title set. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={})
        title = opts.get_alert_title(tree_node)
        self.assertEqual('', title)

    def test_get_alert_title_with_html_entities(self):
        """ Test the ``get_alert_title`` when the title contain HTML entities. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={'title': '&lt;test&gt;'})
        title = opts.get_alert_title(tree_node)
        self.assertEqual('<test>', title)

    def test_get_alert_html_template_with_title(self):
        """ Test the ``get_alert_html_template`` method with a title set. """
        opts = AlertBoxTagOptions()
        for alert_type in opts.accepted_types:
            html_template = opts.get_alert_html_template(alert_type, 'test')
            self.assertEqual(opts.html_template[alert_type], html_template)

    def test_get_alert_html_template_without_title(self):
        """ Test the ``get_alert_html_template`` method without a title set. """
        opts = AlertBoxTagOptions()
        for alert_type in opts.accepted_types:
            html_template = opts.get_alert_html_template(alert_type, '')
            self.assertEqual(opts.html_template_without_title[alert_type], html_template)

    def test_get_alert_text_title_line_template_method(self):
        """ Test the ``get_alert_text_title_line_template`` method. """
        opts = AlertBoxTagOptions()
        for alert_type in opts.accepted_types:
            html_template = opts.get_alert_text_title_line_template(alert_type)
            self.assertEqual(opts.text_title_line_template[alert_type], html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template[alert_type].format(type=alert_type,
                                                                                  title='Test',
                                                                                  inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_trailing_newline(self):
        """ Test HTML rendering with trailing newline. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, '\n\nHello world!\n')
            expected_output = AlertBoxTagOptions.html_template[alert_type].format(type=alert_type,
                                                                                  title='Test',
                                                                                  inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities_in_title(self):
        """ Test HTML rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': '<Test>', 'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template[alert_type].format(type=alert_type,
                                                                                  title='&lt;Test&gt;',
                                                                                  inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title(self):
        """ Test HTML rendering without title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_html(tree_node, 'Hello world!')
            expected_output = AlertBoxTagOptions.html_template_without_title[alert_type].format(type=alert_type,
                                                                                                title='',
                                                                                                inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title_but_with_trailing_newline(self):
        """ Test HTML rendering without title but with trailing newline. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_html(tree_node, '\nHello world!\n\n')
            expected_output = AlertBoxTagOptions.html_template_without_title[alert_type].format(type=alert_type,
                                                                                                title='',
                                                                                                inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_trailing_newline(self):
        """ Test text rendering with trailing newline. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, '\n\nHello world!\nBonjour le monde !\n')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities_in_title(self):
        """ Test text rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': '<Test>', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title='<Test>'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title(self):
        """ Test text rendering without title but with trailing newline. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title=''))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title_but_trailing_newline(self):
        """ Test text rendering without title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': alert_type})
            rendered_output = opts.render_text(tree_node, '\nHello world!\nBonjour le monde !\n\n')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title=''))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_newlines(self):
        """ Test text rendering with various newline ending in content. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            rendered_output = opts.render_text(tree_node, 'Hello world!\nBonjour le monde !\r\nYolo.')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
* Yolo.
***
""".format(title_line=AlertBoxTagOptions.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': 'Test', 'type': alert_type})
            expected_result = ({'type': alert_type, 'title': 'Test'}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))

    def test_get_skcode_attributes_without_title(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering without title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'type': alert_type})
            expected_result = ({'type': alert_type, 'title': ''}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))

    def test_get_skcode_attributes_with_html_entities_in_title(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering with HTML entities in title. """
        opts = AlertBoxTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            tree_node = root_tree_node.new_child('alert', opts, attrs={'title': '<Test>', 'type': alert_type})
            expected_result = ({'type': alert_type, 'title': '<Test>'}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))


class FixedAlertBoxTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the alerts tag module (fixed type tag variants). """

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

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = FixedAlertBoxTagOptions('customtype')
        self.assertEqual('customtype', opts.alert_type)
        self.assertEqual('customtype', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = FixedAlertBoxTagOptions('customtype', canonical_tag_name='foobar')
        self.assertEqual('customtype', opts.alert_type)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_get_alert_type_method(self):
        """ Test the ``get_alert_type`` method. """
        opts = FixedAlertBoxTagOptions('customtype')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('alert', opts, attrs={})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual('customtype', alert_type)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering. """
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = root_tree_node.new_child(alert_type, opts, attrs={'title': 'Test'})
            expected_result = ({'title': 'Test'}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))

    def test_get_skcode_attributes_without_title(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering without title. """
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = root_tree_node.new_child(alert_type, opts, attrs={})
            expected_result = ({'title': ''}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))

    def test_get_skcode_attributes_with_html_entities_in_title(self):
        """ Test the ``get_skcode_attributes`` used for SkCode rendering with HTML entities in title. """
        root_tree_node = RootTreeNode(RootTagOptions())
        for alert_type in AlertBoxTagOptions.accepted_types:
            opts = FixedAlertBoxTagOptions(alert_type)
            tree_node = root_tree_node.new_child(alert_type, opts, attrs={'title': '<Test>'})
            expected_result = ({'title': '<Test>'}, 'title')
            self.assertEqual(expected_result, opts.get_skcode_attributes(tree_node, 'Hello world!'))
