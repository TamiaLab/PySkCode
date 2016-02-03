"""
SkCode medias tag definitions code.
"""

import posixpath

from urllib.parse import (urlsplit,
                          parse_qs,
                          quote_plus)

from html import escape as escape_html
from html import unescape as unescape_html_entities

from .base import TagOptions
from ..tools import sanitize_url


class ImageTagOptions(TagOptions):
    """ Image tag options container class. """

    inline = True
    close_inlines = False

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
        # TODO Add relative-absolute URL conversion
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
            return width if width > 0 else 0
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
            return height if height > 0 else 0
        except ValueError:
            return 0

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the image source link
        src_link = self.get_image_src_link(tree_node)

        # Get the alternative text
        alt_text = self.get_alt_text(tree_node)
        extra_attrs = ' alt="%s"' % escape_html(alt_text) if alt_text else ''

        # Get the image width
        img_width = self.get_img_width(tree_node)
        if img_width:
            extra_attrs += ' width="%d"' % img_width

        # Get the image height
        img_height = self.get_img_height(tree_node)
        if img_height:
            extra_attrs += ' height="%d"' % img_height

        # Render the image
        return '<img src="%s"%s />' % (src_link, extra_attrs)

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the image source link
        src_link = self.get_image_src_link(tree_node)

        # Shortcut if no source link
        if not src_link:
            return inner_text

        # Get the alternative text
        alt_text = self.get_alt_text(tree_node)
        return '%s (%s)' % (src_link, alt_text) if alt_text else src_link

    def get_skcode_attributes(self, tree_node, inner_skcode, **kwargs):
        """
        Getter function for retrieving all attributes of this node required for rendering SkCode.
        :param tree_node: The tree node to be rendered.
        :param inner_skcode: The inner SkCode of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return A dictionary of all attributes required for rendering SkCode and the tag value
        attribute name for the shortcut syntax (if required).
        """

        # Get all attributes
        alt_text = self.get_alt_text(tree_node)
        img_width = self.get_img_width(tree_node)
        img_height = self.get_img_height(tree_node)
        return {
                   self.alt_attr_name: alt_text,
                   self.width_attr_name: str(img_width) if img_width > 0 else '',
                   self.height_attr_name: str(img_height) if img_height > 0 else ''
               }, None


class YoutubeTagOptions(TagOptions):
    """ Youtube video integration tag options container class. """

    # Default iframe width
    default_iframe_width = 560

    # Default iframe height
    default_iframe_height = 315

    # Allowed Youtube domains
    allowed_domains = (
        'www.youtube.com',
        'youtube.com',
        'youtu.be',
    )

    # Youtube video ID query arg name
    video_id_query_arg_name = 'v'

    # Special cases, when ID is in path
    video_id_in_path_domains = {
        'youtu.be',
    }

    # HTML template
    integration_html_template = """<div class="embed-container center-block">
        <div class="embed-video">
            <iframe width="%(width)d" height="%(height)d" src="https://www.youtube.com/embed/%(video_id)s" frameborder="0" allowfullscreen="true"></iframe>
        </div>
    </div>
    """

    # Text link
    text_link_format = 'https://youtu.be/%s'

    def get_youtube_video_id(self, tree_node):
        """
        Get the Youtube video ID.
        :param tree_node: Current tree node to be rendered.
        :return The video ID, or an empty string.
        """

        # Get the URL
        url = tree_node.get_raw_content().strip()

        # Shortcut if no url
        if not url:
            return ''

        # Split the URL
        try:
            scheme, netloc, path, query, fragment = urlsplit(url)
        except ValueError:

            # Handle malformed URL
            return ''

        # Check for bad netloc
        if netloc not in self.allowed_domains:
            return ''

        # Video ID in query
        if netloc not in self.video_id_in_path_domains:

            # Check for bad url query
            if not query:
                return ''

            # Get the video ID
            query_args = parse_qs(query)
            video_id = query_args.get(self.video_id_query_arg_name, None)

            # Query args return a list of values
            return video_id[0].strip() if video_id else ''

        # Video ID in path
        else:

            # Check for bad url path
            if not path or not path.startswith('/'):
                return ''

            # Get the video ID
            video_id = posixpath.basename(path.rstrip('/'))

            # Query args return a list of values
            return video_id.strip() if video_id else ''

    def render_html(self, tree_node, inner_html, **kwargs):
        """
        Callback function for rendering HTML.
        :param tree_node: The tree node to be rendered.
        :param inner_html: The inner HTML of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered HTML of this node.
        """

        # Get the video ID
        video_id = self.get_youtube_video_id(tree_node)

        # Render the iframe
        return self.integration_html_template % {
            'width': self.default_iframe_width,
            'height': self.default_iframe_height,
            'video_id': quote_plus(video_id)
        } if video_id else inner_html

    def render_text(self, tree_node, inner_text, **kwargs):
        """
        Callback function for rendering text.
        :param tree_node: The tree node to be rendered.
        :param inner_text: The inner text of this tree node.
        :param kwargs: Extra keyword arguments for rendering.
        :return The rendered text of this node.
        """

        # Get the video ID
        video_id = self.get_youtube_video_id(tree_node)
        return self.text_link_format % quote_plus(video_id) if video_id else inner_text
