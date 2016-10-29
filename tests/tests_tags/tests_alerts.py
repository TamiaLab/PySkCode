"""
SkCode alert box tag definitions test code.
"""

import unittest

from skcode.etree import RootTreeNode
from skcode.tags import (
    AlertBoxTreeNode,
    ALERT_TYPE_ERROR,
    ALERT_TYPE_DANGER,
    ALERT_TYPE_WARNING,
    ALERT_TYPE_INFO,
    ALERT_TYPE_SUCCESS,
    ALERT_TYPE_NOTE,
    ALERT_TYPE_QUESTION,
    DEFAULT_RECOGNIZED_TAGS_LIST,
    generate_fixed_alert_type_cls
)


class AlertBoxTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the alerts tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the default dictionary of recognized tags. """
        self.assertIn(AlertBoxTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

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
        self.assertFalse(AlertBoxTreeNode.newline_closes)
        self.assertFalse(AlertBoxTreeNode.same_tag_closes)
        self.assertFalse(AlertBoxTreeNode.weak_parent_close)
        self.assertFalse(AlertBoxTreeNode.standalone)
        self.assertTrue(AlertBoxTreeNode.parse_embedded)
        self.assertFalse(AlertBoxTreeNode.inline)
        self.assertTrue(AlertBoxTreeNode.close_inlines)
        self.assertTrue(AlertBoxTreeNode.make_paragraphs_here)
        self.assertEqual('alert', AlertBoxTreeNode.canonical_tag_name)
        self.assertEqual((), AlertBoxTreeNode.alias_tag_names)
        self.assertEqual((
            ALERT_TYPE_ERROR,
            ALERT_TYPE_DANGER,
            ALERT_TYPE_WARNING,
            ALERT_TYPE_INFO,
            ALERT_TYPE_SUCCESS,
            ALERT_TYPE_NOTE,
            ALERT_TYPE_QUESTION
        ), AlertBoxTreeNode.accepted_types)
        self.assertEqual(ALERT_TYPE_INFO, AlertBoxTreeNode.default_type)
        # String values of ``html_template``, ``html_template_without_title``, ``text_title_line_template``
        # and ``default_titles`` are NOT tested.
        self.assertIn(ALERT_TYPE_ERROR, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_ERROR])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_DANGER])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_WARNING])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_INFO])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_SUCCESS])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_NOTE])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, AlertBoxTreeNode.html_template)
        self.assertIn('{title}', AlertBoxTreeNode.html_template[ALERT_TYPE_QUESTION])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template[ALERT_TYPE_QUESTION])
        self.assertIn(ALERT_TYPE_ERROR, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_ERROR])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_DANGER])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_WARNING])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_INFO])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_SUCCESS])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_NOTE])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, AlertBoxTreeNode.html_template_without_title)
        self.assertNotIn('{title}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_QUESTION])
        self.assertIn('{inner_html}', AlertBoxTreeNode.html_template_without_title[ALERT_TYPE_QUESTION])
        self.assertIn(ALERT_TYPE_ERROR, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_ERROR])
        self.assertIn(ALERT_TYPE_DANGER, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_DANGER])
        self.assertIn(ALERT_TYPE_WARNING, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_WARNING])
        self.assertIn(ALERT_TYPE_INFO, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_INFO])
        self.assertIn(ALERT_TYPE_SUCCESS, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_SUCCESS])
        self.assertIn(ALERT_TYPE_NOTE, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_NOTE])
        self.assertIn(ALERT_TYPE_QUESTION, AlertBoxTreeNode.text_title_line_template)
        self.assertIn('{title}', AlertBoxTreeNode.text_title_line_template[ALERT_TYPE_QUESTION])
        self.assertEqual('type', AlertBoxTreeNode.alert_type_attr_name)
        self.assertEqual('title', AlertBoxTreeNode.alert_title_attr_name)

    def test_get_alert_type(self):
        """ Test the ``get_alert_type`` method with a valid alert type. """
        root_tree_node = RootTreeNode()
        for known_alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': known_alert_type})
            alert_type = tree_node.get_alert_type()
            self.assertEqual(known_alert_type, alert_type)

    def test_get_alert_type_uppercase(self):
        """ Test the ``get_alert_type`` method with a valid alert type but in uppercase. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': 'ERRor'})
        alert_type = tree_node.get_alert_type()
        self.assertEqual('error', alert_type)

    def test_get_alert_type_without_type(self):
        """ Test the ``get_alert_type`` method without an alert type. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={})
        alert_type = tree_node.get_alert_type()
        self.assertEqual(tree_node.default_type, alert_type)

    def test_get_alert_type_with_invalid_type(self):
        """ Test the ``get_alert_type`` method with an invalid alert type. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': 'notatype'})
        alert_type = tree_node.get_alert_type()
        self.assertEqual(tree_node.default_type, alert_type)

    def test_get_alert_title_with_tagname_set(self):
        """ Test the ``get_alert_title`` with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'alert': 'test'})
        title = tree_node.get_alert_title()
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_set(self):
        """ Test the ``get_alert_title`` with the "title" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'title': 'test'})
        title = tree_node.get_alert_title()
        self.assertEqual('test', title)

    def test_get_alert_title_with_title_and_tagname_set(self):
        """ Test the ``get_alert_title`` with the "title" and tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'alert': 'test', 'title': 'test2'})
        title = tree_node.get_alert_title()
        self.assertEqual('test', title)

    def test_get_alert_title_with_default_value(self):
        """ Test the ``get_alert_title`` with no title set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={})
        title = tree_node.get_alert_title()
        self.assertEqual('', title)

    def test_get_alert_title_with_html_entities(self):
        """ Test the ``get_alert_title`` when the title contain HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'title': '&lt;test&gt;'})
        title = tree_node.get_alert_title()
        self.assertEqual('<test>', title)

    def test_get_alert_html_template_with_title(self):
        """ Test the ``get_alert_html_template`` method with a title set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={})
        for alert_type in AlertBoxTreeNode.accepted_types:
            html_template = tree_node.get_alert_html_template(alert_type, 'test')
            self.assertEqual(tree_node.html_template[alert_type], html_template)

    def test_get_alert_html_template_without_title(self):
        """ Test the ``get_alert_html_template`` method without a title set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={})
        for alert_type in AlertBoxTreeNode.accepted_types:
            html_template = tree_node.get_alert_html_template(alert_type, '')
            self.assertEqual(tree_node.html_template_without_title[alert_type], html_template)

    def test_get_alert_text_title_line_template_method(self):
        """ Test the ``get_alert_text_title_line_template`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={})
        for alert_type in AlertBoxTreeNode.accepted_types:
            html_template = tree_node.get_alert_text_title_line_template(alert_type)
            self.assertEqual(tree_node.text_title_line_template[alert_type], html_template)

    def test_html_rendering(self):
        """ Test HTML rendering. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': 'Test', 'type': alert_type})
            rendered_output = tree_node.render_html('Hello world!')
            expected_output = AlertBoxTreeNode.html_template[alert_type].format(type=alert_type,
                                                                                title='Test',
                                                                                inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_trailing_newline(self):
        """ Test HTML rendering with trailing newline. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': 'Test', 'type': alert_type})
            rendered_output = tree_node.render_html('\n\nHello world!\n')
            expected_output = AlertBoxTreeNode.html_template[alert_type].format(type=alert_type,
                                                                                title='Test',
                                                                                inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_with_html_entities_in_title(self):
        """ Test HTML rendering with HTML entities in title. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': '<Test>', 'type': alert_type})
            rendered_output = tree_node.render_html('Hello world!')
            expected_output = AlertBoxTreeNode.html_template[alert_type].format(type=alert_type,
                                                                                title='&lt;Test&gt;',
                                                                                inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title(self):
        """ Test HTML rendering without title. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': alert_type})
            rendered_output = tree_node.render_html('Hello world!')
            expected_output = AlertBoxTreeNode.html_template_without_title[alert_type].format(type=alert_type,
                                                                                              title='',
                                                                                              inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_html_rendering_without_title_but_with_trailing_newline(self):
        """ Test HTML rendering without title but with trailing newline. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': alert_type})
            rendered_output = tree_node.render_html('\nHello world!\n\n')
            expected_output = AlertBoxTreeNode.html_template_without_title[alert_type].format(type=alert_type,
                                                                                              title='',
                                                                                              inner_html='Hello world!')
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering(self):
        """ Test text rendering. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': 'Test', 'type': alert_type})
            rendered_output = tree_node.render_text('Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_trailing_newline(self):
        """ Test text rendering with trailing newline. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': 'Test', 'type': alert_type})
            rendered_output = tree_node.render_text('\n\nHello world!\nBonjour le monde !\n')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_with_html_entities_in_title(self):
        """ Test text rendering with HTML entities in title. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': '<Test>', 'type': alert_type})
            rendered_output = tree_node.render_text('Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title='<Test>'))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title(self):
        """ Test text rendering without title but with trailing newline. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': alert_type})
            rendered_output = tree_node.render_text('Hello world!\nBonjour le monde !')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title=''))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_without_title_but_trailing_newline(self):
        """ Test text rendering without title. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode, attrs={'type': alert_type})
            rendered_output = tree_node.render_text('\nHello world!\nBonjour le monde !\n\n')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title=''))
            self.assertEqual(expected_output, rendered_output)

    def test_text_rendering_newlines(self):
        """ Test text rendering with various newline ending in content. """
        root_tree_node = RootTreeNode()
        for alert_type in AlertBoxTreeNode.accepted_types:
            tree_node = root_tree_node.new_child('alert', AlertBoxTreeNode,
                                                 attrs={'title': 'Test', 'type': alert_type})
            rendered_output = tree_node.render_text('Hello world!\nBonjour le monde !\r\nYolo.')
            expected_output = """*** {title_line}
* Hello world!
* Bonjour le monde !
* Yolo.
***
""".format(title_line=AlertBoxTreeNode.text_title_line_template[alert_type].format(title='Test'))
            self.assertEqual(expected_output, rendered_output)


class FixedAlertBoxTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the alerts tag module (fixed type tag variants). """

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = generate_fixed_alert_type_cls('customtype')
        self.assertEqual('customtype', opts.alert_type)
        self.assertEqual('customtype', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = generate_fixed_alert_type_cls('customtype', canonical_tag_name='foobar')
        self.assertEqual('customtype', opts.alert_type)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_get_alert_type_method(self):
        """ Test the ``get_alert_type`` method. """
        opts = generate_fixed_alert_type_cls('customtype')
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('alert', opts, attrs={})
        alert_type = opts.get_alert_type(tree_node)
        self.assertEqual('customtype', alert_type)
