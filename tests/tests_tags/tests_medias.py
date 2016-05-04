"""
SkCode medias tag test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         ImageTagOptions,
                         YoutubeTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class ImagesTagTestCase(unittest.TestCase):
    """ Tests suite for the image tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('img', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['img'], ImageTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = ImageTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertTrue(opts.inline)
        self.assertFalse(opts.close_inlines)
        self.assertEqual('img', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('alt', opts.alt_attr_name)
        self.assertEqual('width', opts.width_attr_name)
        self.assertEqual('height', opts.height_attr_name)
        self.assertEqual(('http', 'https'), opts.allowed_schemes)
        self.assertEqual('<img src="{src_link}"{extra_args} />', opts.html_render_template)

    def test_get_image_src_link(self):
        """ Test the ``get_image_src_link`` method with a valid source link. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        src_link = opts.get_image_src_link(tree_node)
        self.assertEqual('http://example.com/image.jpg', src_link)

    def test_get_image_src_link_trailing_whitespaces(self):
        """ Test the ``get_image_src_link`` method with a valid source link. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='  http://example.com/image.jpg  ')
        src_link = opts.get_image_src_link(tree_node)
        self.assertEqual('http://example.com/image.jpg', src_link)

    def test_get_image_src_link_called_sanitize(self):
        """ Test the ``get_image_src_link`` method call the ``sanitize_url`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        with unittest.mock.patch('skcode.tags.medias.sanitize_url') as mock_sanitize_url:
            opts.get_image_src_link(tree_node)
        mock_sanitize_url.assert_called_once_with('http://example.com/image.jpg',
                                                  allowed_schemes=opts.allowed_schemes,
                                                  absolute_base_url='')

    def test_get_image_src_link_called_sanitize_with_relative_url_conversion(self):
        """ Test the ``get_image_src_link`` method call the ``sanitize_url`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        with unittest.mock.patch('skcode.tags.medias.sanitize_url') as mock_sanitize_url:
            opts.get_image_src_link(tree_node)
        mock_sanitize_url.assert_called_once_with('http://example.com/image.jpg',
                                                  allowed_schemes=opts.allowed_schemes,
                                                  absolute_base_url='http://example.com/')

    def test_get_alt_text(self):
        """ Test the ``get_alt_text`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Hello World!'})
        alt_text = opts.get_alt_text(tree_node)
        self.assertEqual('Hello World!', alt_text)

    def test_get_alt_text_without_value(self):
        """ Test the ``get_alt_text`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={})
        alt_text = opts.get_alt_text(tree_node)
        self.assertEqual('', alt_text)

    def test_get_alt_text_with_html_entities(self):
        """ Test the ``get_alt_text`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': '<Hello World!>'})
        alt_text = opts.get_alt_text(tree_node)
        self.assertEqual('<Hello World!>', alt_text)

    def test_get_alt_text_with_encoded_html_entities(self):
        """ Test the ``get_alt_text`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': '&lt;Hello World!&gt;'})
        alt_text = opts.get_alt_text(tree_node)
        self.assertEqual('<Hello World!>', alt_text)

    def test_get_img_width(self):
        """ Test the ``get_img_width`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'width': '120'})
        img_width = opts.get_img_width(tree_node)
        self.assertEqual(img_width, 120)

    def test_get_img_width_without_value(self):
        """ Test the ``get_img_width`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={})
        img_width = opts.get_img_width(tree_node)
        self.assertEqual(img_width, 0)

    def test_get_img_width_with_negative_value(self):
        """ Test the ``get_img_width`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'width': '-120'})
        img_width = opts.get_img_width(tree_node)
        self.assertEqual(img_width, 0)

    def test_get_img_width_with_non_number(self):
        """ Test the ``get_img_width`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'width': 'abc'})
        img_width = opts.get_img_width(tree_node)
        self.assertEqual(img_width, 0)

    def test_get_img_height(self):
        """ Test the ``get_img_height`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'height': '120'})
        img_height = opts.get_img_height(tree_node)
        self.assertEqual(img_height, 120)

    def test_get_img_height_without_value(self):
        """ Test the ``get_img_height`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={})
        img_height = opts.get_img_height(tree_node)
        self.assertEqual(img_height, 0)

    def test_get_img_height_with_negative_value(self):
        """ Test the ``get_img_height`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'height': '-120'})
        img_height = opts.get_img_height(tree_node)
        self.assertEqual(img_height, 0)

    def test_get_img_height_with_non_number(self):
        """ Test the ``get_img_height`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'height': 'abc'})
        img_height = opts.get_img_height(tree_node)
        self.assertEqual(img_height, 0)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="http://example.com/image.jpg" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_no_src_link(self):
        """ Test the ``render_html`` method without a source link. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_alt_text(self):
        """ Test the ``render_html`` method with an alternative text. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Example image.'},
                                             content='http://example.com/image.jpg')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_alt_text_containing_html_entities(self):
        """ Test the ``render_html`` method with an alternative text containing HTML entities. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': '<Example image.>'},
                                             content='http://example.com/image.jpg')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="http://example.com/image.jpg" alt="&lt;Example image.&gt;" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_img_width(self):
        """ Test the ``render_html`` method with an image width. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Example image.', 'width': '120'},
                                             content='http://example.com/image.jpg')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." width="120" />'
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_img_height(self):
        """ Test the ``render_html`` method with an image height. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts,
                                             attrs={'alt': 'Example image.', 'width': '120', 'height': '240'},
                                             content='http://example.com/image.jpg')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = '<img src="http://example.com/image.jpg" alt="Example image." width="120" height="240" />'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'http://example.com/image.jpg'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_no_src_link(self):
        """ Test the ``render_text`` method without a source link. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={})
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_alt_text(self):
        """ Test the ``render_text`` method with an alternative text. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Example image.'},
                                             content='http://example.com/image.jpg')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'http://example.com/image.jpg (Example image.)'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={}, content='http://example.com/image.jpg')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'alt': '', 'width': '', 'height': ''}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_no_src_link(self):
        """ Test the ``get_skcode_attributes`` method with no source link. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={})
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'alt': '', 'width': '', 'height': ''}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_alt_text(self):
        """ Test the ``get_skcode_attributes`` method with a alternative text. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Example image.'},
                                             content='http://example.com/image.jpg')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'alt': 'Example image.', 'width': '', 'height': ''}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_img_width(self):
        """ Test the ``get_skcode_attributes`` method with an image width. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts, attrs={'alt': 'Example image.', 'width': '120'},
                                             content='http://example.com/image.jpg')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'alt': 'Example image.', 'width': '120', 'height': ''}, None)
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_img_height(self):
        """ Test the ``get_skcode_attributes`` method with an image height. """
        opts = ImageTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('img', opts,
                                             attrs={'alt': 'Example image.', 'width': '120', 'height': '240'},
                                             content='http://example.com/image.jpg')
        output_result = opts.get_skcode_attributes(tree_node, 'test')
        expected_result = ({'alt': 'Example image.', 'width': '120', 'height': '240'}, None)
        self.assertEqual(expected_result, output_result)


class YoutubeVideosTagTestCase(unittest.TestCase):
    """ Tests suite for the Youtube video tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('youtube', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['youtube'], YoutubeTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = YoutubeTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertTrue(opts.parse_embedded)
        self.assertFalse(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertEqual('youtube', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual(opts.default_iframe_width, 560)
        self.assertEqual(opts.default_iframe_height, 315)
        self.assertEqual(opts.allowed_domains, ('www.youtube.com', 'youtube.com', 'youtu.be'))
        self.assertEqual(opts.video_id_query_arg_name, 'v')
        self.assertEqual(opts.video_id_in_path_domains, {'youtu.be'})
        self.assertEqual("""<div class="embed-container center-block">
        <div class="embed-video">
            <iframe width="{width}" height="{height}" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen="true"></iframe>
        </div>
    </div>
    """, opts.integration_html_template)
        self.assertEqual('https://youtu.be/{video_id}', opts.text_link_format)

    def test_get_youtube_video_id(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='   https://www.youtube.com/watch?v=dQw4w9WgXcQ ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_with_no_value_set(self):
        """ Test the ``get_youtube_video_id`` method with no link set. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts)
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_malformed_url(self):
        """ Test the ``get_youtube_video_id`` method with a malformed link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='http://[www.youtube.com/watch?v=dQw4w9WgXcQ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_disallowed_domain(self):
        """ Test the ``get_youtube_video_id`` method with a disallowed domain name. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.notyoutube.com/watch?v=dQw4w9WgXcQ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_no_query(self):
        """ Test the ``get_youtube_video_id`` method with not query. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_no_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?foo=bar')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_empty_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_empty_video_id_2(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_with_multiple_video_id(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=foo&v=bar')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('foo', video_id)

    def test_get_youtube_video_id_with_video_id_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with no video ID (empty query arg). """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=+++foobar+++')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('foobar', video_id)

    def test_get_youtube_video_id_path(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://youtu.be/dQw4w9WgXcQ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_2(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://youtu.be/something/dQw4w9WgXcQ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_trailing_slash(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://youtu.be/dQw4w9WgXcQ/')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_path_trailing_whitespaces(self):
        """ Test the ``get_youtube_video_id`` method with a valid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://youtu.be/  dQw4w9WgXcQ ')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('dQw4w9WgXcQ', video_id)

    def test_get_youtube_video_id_no_path(self):
        """ Test the ``get_youtube_video_id`` method with a invalid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://youtu.be')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_get_youtube_video_id_path_no_netloc(self):
        """ Test the ``get_youtube_video_id`` method with a invalid youtube link. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='youtu.be/')
        video_id = opts.get_youtube_video_id(tree_node)
        self.assertEqual('', video_id)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        output_result = opts.render_html(tree_node, 'test')
        expected_result = opts.integration_html_template.format(width=opts.default_iframe_width,
                                                                height=opts.default_iframe_height,
                                                                video_id='dQw4w9WgXcQ')
        self.assertEqual(expected_result, output_result)

    def test_render_html_without_video(self):
        """ Test the ``render_html`` method without a valid video ID. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts)
        output_result = opts.render_html(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts, content='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'https://youtu.be/dQw4w9WgXcQ'
        self.assertEqual(expected_result, output_result)

    def test_render_text_without_video(self):
        """ Test the ``render_text`` method without a valid video ID. """
        opts = YoutubeTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('youtube', opts)
        output_result = opts.render_text(tree_node, 'test')
        expected_result = 'test'
        self.assertEqual(expected_result, output_result)
