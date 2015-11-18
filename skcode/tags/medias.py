"""
SkCode medias tag definitions code.
"""

from urllib.parse import (urlsplit,
                          parse_qs,
                          quote_plus)

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions
from ..tools import (escape_attrvalue,
                     sanitize_url)


class ImageTagOptions(TagOptions):
    """ Image tag options container class. """

    # Alternate text attribute name
    alt_attr_name = 'alt'

    # Image width attribute name
    width_attr_name = 'width'

    # Image height attribute name
    height_attr_name = 'height'

    # Allowed schemes for URL
    allowed_schemes = ('http', 'https')

    def get_image_src_link(self, tree_node):
        """
        Get the image source link URL.
        :param tree_node: The current tree node instance.
        :return The image source link URL (not sanitized).
        """
        src_link = tree_node.get_raw_content().strip()
        return sanitize_url(src_link, allowed_schemes=self.allowed_schemes)

    def get_alt_text(self, tree_node):
        """
        Get the image alt text.
        :param tree_node: The current tree node instance.
        :return The image alternative text as string, or an empty string.
        """
        alt_text = tree_node.attrs.get(self.alt_attr_name, '')
        return unescape_html_entities(alt_text)

    def get_img_width(self, tree_node):
        """
        Get the image width, or zero.
        :param tree_node: The current tree node instance.
        :return The image width, or zero.
        """
        try:
            width = int(tree_node.attrs.get(self.width_attr_name, 0))
            if width <= 0:
                return 0
            return width
        except ValueError:
            return 0

    def get_img_height(self, tree_node):
        """
        Get the image height, or zero.
        :param tree_node: The current tree node instance.
        :return The image height, or zero.
        """
        try:
            height = int(tree_node.attrs.get(self.height_attr_name, 0))
            if height <= 0:
                return 0
            return height
        except ValueError:
            return 0

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the image source link
        src_link = self.get_image_src_link(tree_node)

        # Shortcut if no source link
        if not src_link:
            return ''

        # Get the alternative text
        alt_text = self.get_alt_text(tree_node)
        if alt_text:
            extra_attrs = ' alt="%s"' % escape_html(alt_text)
        else:
            extra_attrs = ''

        # Get the image width
        img_width = self.get_img_width(tree_node)
        if img_width:
            extra_attrs += ' width="%d"' % img_width

        # Get the image height
        img_height = self.get_img_height(tree_node)
        if img_width:
            extra_attrs += ' height="%d"' % img_height

        # Render the image
        return '<img src="%s"%s />' % (src_link, extra_attrs)

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the image source link
        src_link = self.get_image_src_link(tree_node)

        # Shortcut if no source link
        if not src_link:
            return inner_text

        # Get the alternative text
        alt_text = self.get_alt_text(tree_node)
        if alt_text:
            return '%s (%s)' % (src_link, alt_text)
        else:
            return src_link

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the image source link
        src_link = self.get_image_src_link(tree_node)

        # Shortcut if no source link
        if not src_link:
            return inner_skcode

        # Get the alternative text
        alt_text = self.get_alt_text(tree_node)
        if alt_text:
            extra_attrs = ' %s=%s' % (self.alt_attr_name,
                                      escape_attrvalue(alt_text))
        else:
            extra_attrs = ''

        # Get the image width
        img_width = self.get_img_width(tree_node)
        if img_width:
            extra_attrs += ' %s="%d"' % (self.width_attr_name, img_width)

        # Get the image height
        img_height = self.get_img_height(tree_node)
        if img_width:
            extra_attrs += ' %s="%d"' % (self.height_attr_name, img_height)

        # Render the image
        node_name = tree_node.name
        return '[%s%s]%s[/%s]' % (node_name, extra_attrs, src_link, node_name)


class YoutubeTagOptions(TagOptions):
    """ Youtube video integration tag options container class. """

    # Default iframe width
    default_iframe_width = 560

    # Default iframe height
    default_iframe_height = 315

    # Allowed Youtube domains
    allowed_domains = ('www.youtube.com', 'youtube.com')

    # Youtube video ID query arg name
    video_id_query_arg_name = 'v'

    def get_youtube_video_id(self, tree_node):
        """
        Get the Youtube video ID.
        :param tree_node: Current tree node to be rendered.
        :return The video ID, or an empty string.
        """

        # Get the URL
        url = tree_node.get_raw_content().strip()

        # Split the URL
        try:
            scheme, netloc, path, query, fragment = urlsplit(url)
        except ValueError:

            # Handle malformed URL
            return ''

        # Check for bad netloc
        if netloc not in self.allowed_domains:
            return ''

        # Check for bad url query
        if not query:
            return ''

        # Get the video ID
        query_args = parse_qs(query)
        video_id = query_args.get(self.video_id_query_arg_name, None)

        # Query args return a list of values
        if not video_id:
            return ''
        else:
            return video_id[0].strip()

    def render_html(self, tree_node, inner_html, force_rel_nofollow=True):
        """
        Callback function for rendering HTML.
        :param force_rel_nofollow: If set, all links in the rendered HTML will have "rel=nofollow" (default to True).
        :param tree_node: Current tree node to be rendered.
        :param inner_html: Inner HTML of this tree node.
        :return Rendered HTML of this node.
        """

        # Get the video ID
        video_id = self.get_youtube_video_id(tree_node)

        # Render the iframe
        if video_id:
            return '<iframe width="%d" height="%d" ' \
                   'src="https://www.youtube.com/embed/%s" ' \
                   'frameborder="0" allowfullscreen></iframe>' % (self.default_iframe_width,
                                                                  self.default_iframe_height,
                                                                  quote_plus(video_id))
        else:
            return inner_html

    def render_text(self, tree_node, inner_text):
        """
        Callback function for rendering text.
        :param tree_node: Current tree node to be rendered.
        :param inner_text: Inner text of this tree node.
        :return Rendered text of this node.
        """

        # Get the video ID
        video_id = self.get_youtube_video_id(tree_node)

        # Render the video link
        if video_id:
            return 'https://www.youtube.com/watch?v=%s' % quote_plus(video_id)
        else:
            return inner_text

    def render_skcode(self, tree_node, inner_skcode):
        """
        Callback function for rendering SkCode.
        :param tree_node: Current tree node to be rendered.
        :param inner_skcode: Inner SkCode of this tree node.
        :return Rendered SkCode of this node.
        """

        # Get the video ID
        video_id = self.get_youtube_video_id(tree_node)

        # Render the video tag
        if video_id:
            node_name = tree_node.name
            return '[%s]https://www.youtube.com/watch?v=%s[/%s]' % (node_name, quote_plus(video_id), node_name)
        else:
            return inner_skcode
