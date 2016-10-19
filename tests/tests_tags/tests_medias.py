"""
SkCode medias tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (
    ImageTreeNode,
    YoutubeTreeNode,
    DEFAULT_RECOGNIZED_TAGS_LIST
)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class ImagesTagTestCase(unittest.TestCase):
    """ Tests suite for the image tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(ImageTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(ImageTreeNode.newline_closes)
        self.assertFalse(ImageTreeNode.same_tag_closes)
        self.assertFalse(ImageTreeNode.standalone)
        self.assertTrue(ImageTreeNode.parse_embedded)
        self.assertTrue(ImageTreeNode.inline)
        self.assertFalse(ImageTreeNode.close_inlines)
        self.assertEqual('img', ImageTreeNode.canonical_tag_name)
        self.assertEqual((), ImageTreeNode.alias_tag_names)
        self.assertFalse(ImageTreeNode.make_paragraphs_here)
        self.assertEqual('alt', ImageTreeNode.alt_attr_name)
        self.assertEqual('width', ImageTreeNode.width_attr_name)
        self.assertEqual('height', ImageTreeNode.height_attr_name)
        self.assertEqual(('http', 'https'), ImageTreeNode.allowed_schemes)
        self.assertEqual('<img src="{src_link}"{extra_args} />', ImageTreeNode.html_render_template)

    def test_get_image_src_link(self):
        """ Test the ``get_image_src_link`` method with a valid source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='http://example.com/image.jpg')
        src_link = tree_node.get_image_src_link()
        self.assertEqual('http://example.com/image.jpg', src_link)

    def test_get_image_src_link_trailing_whitespaces(self):
        """ Test the ``get_image_src_link`` method with a valid source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='  http://example.com/image.jpg  ')
        src_link = tree_node.get_image_src_link()
        self.assertEqual('http://example.com/image.jpg', src_link)

    def test_get_image_src_link_called_sanitize(self):
        """ Test the ``get_image_src_link`` method call the ``sanitize_url`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='http://example.com/image.jpg')
        with unittest.mock.patch('skcode.tags.medias.sanitize_url') as mock_sanitize_url:
            tree_node.get_image_src_link()
        mock_sanitize_url.assert_called_once_with('http://example.com/image.jpg',
                                                  allowed_schemes=ImageTreeNode.allowed_schemes,
                                                  absolute_base_url='')

    def test_get_image_src_link_called_sanitize_with_relative_url_conversion(self):
        """ Test the ``get_image_src_link`` method call the ``sanitize_url`` method. """
        root_tree_node = RootTreeNode()
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='http://example.com/image.jpg')
        with unittest.mock.patch('skcode.tags.medias.sanitize_url') as mock_sanitize_url:
            tree_node.get_image_src_link()
        mock_sanitize_url.assert_called_once_with('http://example.com/image.jpg',
                                                  allowed_schemes=ImageTreeNode.allowed_schemes,
                                                  absolute_base_url='http://example.com/')

    def test_get_alt_text(self):
        """ Test the ``get_alt_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': 'Hello World!'})
        alt_text = tree_node.get_alt_text()
        self.assertEqual('Hello World!', alt_text)

    def test_get_alt_text_without_value(self):
        """ Test the ``get_alt_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={})
        alt_text = tree_node.get_alt_text()
        self.assertEqual('', alt_text)

    def test_get_alt_text_with_html_entities(self):
        """ Test the ``get_alt_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': '<Hello World!>'})
        alt_text = tree_node.get_alt_text()
        self.assertEqual('<Hello World!>', alt_text)

    def test_get_alt_text_with_encoded_html_entities(self):
        """ Test the ``get_alt_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': '&lt;Hello World!&gt;'})
        alt_text = tree_node.get_alt_text()
        self.assertEqual('<Hello World!>', alt_text)

    def test_get_img_width(self):
        """ Test the ``get_img_width`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'width': '120'})
        img_width = tree_node.get_img_width()
        self.assertEqual(img_width, 120)

    def test_get_img_width_without_value(self):
        """ Test the ``get_img_width`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={})
        img_width = tree_node.get_img_width()
        self.assertEqual(img_width, 0)

    def test_get_img_width_with_negative_value(self):
        """ Test the ``get_img_width`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'width': '-120'})
        img_width = tree_node.get_img_width()
        self.assertEqual(img_width, 0)

    def test_get_img_width_with_non_number(self):
        """ Test the ``get_img_width`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'width': 'abc'})
        img_width = tree_node.get_img_width()
        self.assertEqual(img_width, 0)

    def test_get_img_height(self):
        """ Test the ``get_img_height`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'height': '120'})
        img_height = tree_node.get_img_height()
        self.assertEqual(img_height, 120)

    def test_get_img_height_without_value(self):
        """ Test the ``get_img_height`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={})
        img_height = tree_node.get_img_height()
        self.assertEqual(img_height, 0)

    def test_get_img_height_with_negative_value(self):
        """ Test the ``get_img_height`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'height': '-120'})
        img_height = tree_node.get_img_height()
        self.assertEqual(img_height, 0)

    def test_get_img_height_with_non_number(self):
        """ Test the ``get_img_height`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'height': 'abc'})
        img_height = tree_node.get_img_height()
        self.assertEqual(img_height, 0)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='http://example.com/image.jpg')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="http://example.com/image.jpg" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_src_link(self):
        """ Test the ``render_html`` method without a source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_alt_text(self):
        """ Test the ``render_html`` method with an alternative text. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': 'Example image.'},
                                             content='http://example.com/image.jpg')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_alt_text_containing_html_entities(self):
        """ Test the ``render_html`` method with an alternative text containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': '<Example image.>'},
                                             content='http://example.com/image.jpg')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="http://example.com/image.jpg" alt="&lt;Example image.&gt;" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_img_width(self):
        """ Test the ``render_html`` method with an image width. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': 'Example image.', 'width': '120'},
                                             content='http://example.com/image.jpg')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." width="120" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_img_height(self):
        """ Test the ``render_html`` method with an image height. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode,
                                             attrs={'alt': 'Example image.', 'width': '120', 'height': '240'},
                                             content='http://example.com/image.jpg')
        output_result = tree_node.render_html('test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." width="120" height="240" />'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={}, content='http://example.com/image.jpg')
        output_result = tree_node.render_text('test')
        expected_result = 'http://example.com/image.jpg'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_src_link(self):
        """ Test the ``render_text`` method without a source link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={})
        output_result = tree_node.render_text('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_alt_text(self):
        """ Test the ``render_text`` method with an alternative text. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('img', ImageTreeNode, attrs={'alt': 'Example image.'},
                                             content='http://example.com/image.jpg')
        output_result = tree_node.render_text('test')
        expected_result = 'http://example.com/image.jpg (Example image.)'
        self.assertEqual(expected_result, output_result)


class YoutubeVideosTagTestCase(unittest.TestCase):
    """ Tests suite for the Youtube video tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(YoutubeTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(YoutubeTreeNode.newline_closes)
        self.assertFalse(YoutubeTreeNode.same_tag_closes)
        self.assertFalse(YoutubeTreeNode.standalone)
        self.assertTrue(YoutubeTreeNode.parse_embedded)
        self.assertFalse(YoutubeTreeNode.inline)
        self.assertTrue(YoutubeTreeNode.close_inlines)
        self.assertEqual('youtube', YoutubeTreeNode.canonical_tag_name)
        self.assertEqual((), YoutubeTreeNode.alias_tag_names)
        self.assertFalse(YoutubeTreeNode.make_paragraphs_here)
        self.assertEqual(YoutubeTreeNode.default_iframe_width, 560)
        self.assertEqual(YoutubeTreeNode.default_iframe_height, 315)
        self.assertEqual(YoutubeTreeNode.allowed_domains, ('www.youtube.com', 'youtube.com', 'youtu.be'))
        self.assertEqual(YoutubeTreeNode.video_id_query_arg_name, 'v')
        self.assertEqual(YoutubeTreeNode.video_id_in_path_domains, {'youtu.be'})
        self.assertEqual("""<div class="embed-container center-block">
        <div class="embed-video">
            <iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen="true"></iframe>
        </div>
    </div>
    """, YoutubeTreeNode.integration_html_template)
        self.assertEqual('https://youtu.be/{video_id}', YoutubeTreeNode.text_link_format)

    def test_get_youtube_video_id(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='   https://www.youtube.com/watch?v=dQw4w9WgXcQ ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_with_no_value_set(self):
        """ Test the ``get_youtube_video_id`` method with no link set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode)
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_malformed_url(self):
        """ Test the ``get_youtube_video_id`` method with a malformed link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='http://[www.youtube.com/watch?v=dQw4w9WgXcQ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_disallowed_domain(self):
        """ Test the ``get_youtube_video_id`` method with a disallowed domain name. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.notyoutube.com/watch?v=dQw4w9WgXcQ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_no_query(self):
        """ Test the ``get_youtube_video_id`` method with not query. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_no_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?foo=bar')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_empty_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_empty_video_id_2(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_multiple_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=foo&v=bar')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('foo', video_id)

    def test_get_youtube_video_id_with_video_id_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=+++foobar+++')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('foobar', video_id)

    def test_get_youtube_video_id_path(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """

        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://youtu.be/dQw4w9WgXcQ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_2(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """

        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://youtu.be/something/dQw4w9WgXcQ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_trailing_slash(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://youtu.be/dQw4w9WgXcQ/')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://youtu.be/  dQw4w9WgXcQ ')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_no_path(self):
        """ Test the ``get_youtube_video_id`` method with a invalid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://youtu.be')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_path_no_netloc(self):
        """ Test the ``get_youtube_video_id`` method with a invalid youtube link. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='youtu.be/')
        video_id = tree_node.get_youtube_video_id()
        self.assertEqual('', video_id)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        output_result = tree_node.render_html('test')
        expected_result = YoutubeTreeNode.integration_html_template.format(width=YoutubeTreeNode.default_iframe_width,
                                                                           height=YoutubeTreeNode.default_iframe_height,
                                                                           video_id='dQw4w9WgXcQ')
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_video(self):
        """ Test the ``render_html`` method without a valid video ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode)
        output_result = tree_node.render_html('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        output_result = tree_node.render_text('test')
        expected_result = 'https://youtu.be/dQw4w9WgXcQ'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_video(self):
        """ Test the ``render_text`` method without a valid video ID. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('youtube', YoutubeTreeNode)
        output_result = tree_node.render_text('test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)
