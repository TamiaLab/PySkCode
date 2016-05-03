"""
SkCode smileys replacement utility code.
"""

import re
from html import escape as escape_html


# Default emoticons map
DEFAULT_EMOTICONS_MAP = (

    ('<3', 'heart.png'),
    (':heart:', 'heart.png'),

    (":')", 'joy.png'),
    (':")', 'joy.png'),
    (":'-)", 'joy.png'),
    (':"-)', 'joy.png'),
    (":joy:", 'joy.png'),

    (':D', 'grin.png'),
    (':-D', 'grin.png'),
    ('=D', 'grin.png'),
    (':grin:', 'grin.png'),

    (':)', 'smile.png'),
    (':-)', 'smile.png'),
    ('=]', 'smile.png'),
    ('=)', 'smile.png'),
    (':]', 'smile.png'),
    ('^^', 'smile.png'),
    (':smile:', 'smile.png'),

    ("':)", 'sweat_smile.png'),
    ("':-)", 'sweat_smile.png'),
    ("'=)", 'sweat_smile.png'),
    ("':D", 'sweat_smile.png'),
    ("':-D", 'sweat_smile.png'),
    ("'=D", 'sweat_smile.png'),
    ("^^'", 'sweat_smile.png'),
    ('^^"', 'sweat_smile.png'),
    (':sweat_smile:', 'sweat_smile.png'),

    ('>:)', 'laughing.png'),
    ('>;)', 'laughing.png'),
    ('>:-)', 'laughing.png'),
    ('>;-)', 'laughing.png'),
    ('>=)', 'laughing.png'),
    (':laughing:', 'laughing.png'),

    (';)', 'wink.png'),
    (';-)', 'wink.png'),
    ('*-)', 'wink.png'),
    ('*)', 'wink.png'),
    (';-]', 'wink.png'),
    (';]', 'wink.png'),
    (';D', 'wink.png'),
    (';^)', 'wink.png'),
    (':wink:', 'wink.png'),

    ("':(", 'sweat.png'),
    ("':-(", 'sweat.png'),
    ("'=(", 'sweat.png'),
    (':sweat:', 'sweat.png'),

    (':*', 'kissing.png'),
    (':-*', 'kissing.png'),
    ('=*', 'kissing.png'),
    (':^*', 'kissing.png'),
    (':kissing:', 'kissing.png'),

    ('>:P', 'troll.png'),
    ('X-P', 'troll.png'),
    ('X-p', 'troll.png'),
    ('x-p', 'troll.png'),
    ('x-P', 'troll.png'),

    ('>:[', 'disappointed.png'),
    (':-(', 'disappointed.png'),
    (':(', 'disappointed.png'),
    (':-[', 'disappointed.png'),
    (':[', 'disappointed.png'),
    ('=(', 'disappointed.png'),
    (':disappointed:', 'disappointed.png'),

    ('>:(', 'angry.png'),
    ('>:-(', 'angry.png'),
    (':@', 'angry.png'),
    (':angry:', 'angry.png'),

    (":'(", 'cry.png'),
    (":'-(", 'cry.png'),
    (";(", 'cry.png'),
    (";-(", 'cry.png'),
    (':cry:', 'cry.png'),
    (':sad:', 'cry.png'),

    ('>.<', 'doh.png'),
    ('>_<', 'doh.png'),
    (':doh:', 'doh.png'),

    ('D:', 'fearful.png'),
    (':fearful:', 'fearful.png'),

    (':$', 'zip.png'),
    ('=$', 'zip.png'),
    (':zip:', 'zip.png'),

    ('x)', 'dizzy.png'),
    ('x-)', 'dizzy.png'),
    ('xD', 'dizzy.png'),
    ('X)', 'dizzy.png'),
    ('X-)', 'dizzy.png'),
    ('XD', 'dizzy.png'),
    (':dizzy:', 'dizzy.png'),

    ('*\\0/*', 'victory.png'),
    ('\\0/', 'victory.png'),
    ('*\\O/*', 'victory.png'),
    ('*\\o/*', 'victory.png'),
    ('\\O/', 'victory.png'),
    ('\\o/', 'victory.png'),

    ('O:-)', 'innocent.png'),
    ('0:-3', 'innocent.png'),
    ('0:3', 'innocent.png'),
    ('0:-)', 'innocent.png'),
    ('0:)', 'innocent.png'),
    ('0;^)', 'innocent.png'),
    ('O:-)', 'innocent.png'),
    ('O:)', 'innocent.png'),
    ('O;-)', 'innocent.png'),
    ('O=)', 'innocent.png'),
    ('0;-)', 'innocent.png'),
    ('O:-3', 'innocent.png'),
    ('O:3', 'innocent.png'),
    (':innocent:', 'innocent.png'),

    ('B-)', 'sunglasses.png'),
    ('B)', 'sunglasses.png'),
    ('8)', 'sunglasses.png'),
    ('8-)', 'sunglasses.png'),
    ('B-D', 'sunglasses.png'),
    ('8-D', 'sunglasses.png'),
    (':cool:', 'sunglasses.png'),
    (':sunglasses', 'sunglasses.png'),

    ('-_-', 'neutral.png'),
    ('-__-', 'neutral.png'),
    ('-___-', 'neutral.png'),
    (':|', 'neutral.png'),
    (':-|', 'neutral.png'),
    ('T_T', 'neutral.png'),
    (':neutral:', 'neutral.png'),

    (':?', 'confused.png'),
    (':-?', 'confused.png'),
    (':???', 'confused.png'),
    ('>:\\', 'confused.png'),
    ('>:/', 'confused.png'),
    (':-/', 'confused.png'),
    (':/', 'confused.png'),
    (':-\\', 'confused.png'),
    (':\\', 'confused.png'),
    ('=/', 'confused.png'),
    ('=\\', 'confused.png'),
    (':L', 'confused.png'),
    (':-L', 'confused.png'),
    ('=L', 'confused.png'),
    (':confused:', 'confused.png'),

    (':P', 'razz.png'),
    (':-P', 'razz.png'),
    ('=P', 'razz.png'),
    (':-p', 'razz.png'),
    (':p', 'razz.png'),
    ('=p', 'razz.png'),
    (':-Þ', 'razz.png'),
    (':Þ', 'razz.png'),
    (':þ', 'razz.png'),
    (':-þ', 'razz.png'),
    (':-b', 'razz.png'),
    (':b', 'razz.png'),
    ('d:', 'razz.png'),
    (':razz:', 'razz.png'),

    (':-O', 'shock.png'),
    (':O', 'shock.png'),
    (':-o', 'shock.png'),
    (':o', 'shock.png'),
    ('O_O', 'shock.png'),
    ('o_o', 'shock.png'),
    ('>:O', 'shock.png'),
    ('8o', 'shock.png'),
    ('8-o', 'shock.png'),
    ('8O', 'shock.png'),
    ('8-O', 'shock.png'),
    (':eek:', 'shock.png'),
    (':shock', 'shock.png'),

    (':-X', 'mad.png'),
    (':X', 'mad.png'),
    (':-#', 'mad.png'),
    (':#', 'mad.png'),
    ('=X', 'mad.png'),
    ('=x', 'mad.png'),
    (':x', 'mad.png'),
    (':-x', 'mad.png'),
    ('=#', 'mad.png'),
    (':mad:', 'mad.png'),

    (']:)', 'evil.png'),
    (']:-)', 'evil.png'),
    (']:D', 'evil.png'),
    (']:-D', 'evil.png'),
    (']=D', 'evil.png'),
    (':evil:', 'evil.png'),

    (':lol:', 'lol.png'),
    (':oops:', 'oops.png'),
    (':twisted:', 'twisted.png'),
    (':geek:', 'geek.png'),
    (':spy:', 'spy.png'),
    (':random:', 'random.png'),
    (':bomb:', 'bomb.png'),
    (':tamia:', 'tamia.png'),
    (':!:', 'warning.png'),
    (':?:', 'question.png'),
    (':idea:', 'idea.png'),
    (':mrgreen:', 'alien.png'),
    (':nuclear:', 'nuclear.png'),
    (':sleep:', 'sleep.png'),
    (':stop:', 'stop.png'),
    (':death:', 'death.png'),
)

# Document attribute name for storing the emoticons map
EMOTICONS_MAP_ATTR_NAME = 'EMOTICONS_MAP'

# Document attribute name for storing the emoticons detection regex
EMOTICONS_REGEX_ATTR_NAME = 'EMOTICONS_REGEX'

# Document attribute name for storing the emoticons base URL
EMOTICONS_BASE_URL_ATTR_NAME = 'EMOTICONS_BASE_URL'

# Document attribute name for storing the emoticons HTML class
EMOTICONS_HTML_CLASS_ATTR_NAME = 'EMOTICONS_HTML_CLASS'


def setup_smileys_replacement(document_tree, base_url, emoticons_map=DEFAULT_EMOTICONS_MAP, html_class='emoticons'):
    """
    Setup the document for emoticons replacement.
    :param document_tree: The document tree instance to be setup.
    :param emoticons_map: A tuple of tuple with two values ``(emoticon_text, emoticon_filename)``.
    :param base_url: The base URL for all emoticon images. Can also be a callable for dynamic paths.
    :param html_class: The HTML class to be assigned to each emoticons img tag (optional).
    """
    assert document_tree, "Document tree is mandatory."
    assert document_tree.is_root, "Document tree must be a root tree node instance."
    assert base_url, "Base URL is mandatory."

    # Craft the emoticons regex
    emoticons_regex = r'(^|\s+)(?P<emoticon>%s)(\s+|$)' % '|'.join([re.escape(escape_html(e)) for e, _ in emoticons_map])
    emoticons_regex = re.compile(emoticons_regex)

    # Turn emoticons map into a dictionary
    # Note: use escape_html(k) as key because at rendering, when the ``do_smileys_replacement`` routine is called
    # emoticons are already HTML-encoded. As we need to inject HTML code for img, we can't do the replacement when
    # the emoticons are in plain text.
    emoticons_map = {escape_html(k): v for k, v in emoticons_map}

    # Turn base_url into a callable
    if isinstance(base_url, str):
        base_path = base_url if base_url.endswith('/') else base_url + '/'
        base_url = lambda x: base_path + x

    # Store all emoticons related options
    document_tree.attrs[EMOTICONS_MAP_ATTR_NAME] = emoticons_map
    document_tree.attrs[EMOTICONS_REGEX_ATTR_NAME] = emoticons_regex
    document_tree.attrs[EMOTICONS_BASE_URL_ATTR_NAME] = base_url
    document_tree.attrs[EMOTICONS_HTML_CLASS_ATTR_NAME] = html_class


def do_smileys_replacement(root_tree_node, input_text):
    """
    Do all smileys replacement.
    :param root_tree_node: The root tree node.
    :param input_text: The input text to be processed.
    :return: The string with all cosmetics replacement done.
    """

    # Shortcut if not text
    if not input_text:
        return ''

    # Get all emoticons related options
    emoticons_map = root_tree_node.attrs.get(EMOTICONS_MAP_ATTR_NAME, {})
    emoticons_regex = root_tree_node.attrs.get(EMOTICONS_REGEX_ATTR_NAME, None)
    base_url = root_tree_node.attrs.get(EMOTICONS_BASE_URL_ATTR_NAME, None)
    html_class = root_tree_node.attrs.get(EMOTICONS_HTML_CLASS_ATTR_NAME, None)

    # Only do replacement if configured for
    if not emoticons_map or not emoticons_regex or not base_url:
        return input_text

    # Process all emoticons
    def _handle_match(matchobj):
        emoticon = matchobj.group('emoticon')
        if emoticon in emoticons_map:
            extra_class = ' class="{}"'.format(html_class) if html_class else ''
            img = '<img src="{url}" alt="{alt}"{extra}>'.format(url=base_url(emoticons_map[emoticon]),
                                                                alt=emoticon, extra=extra_class)
            return matchobj.group(1) + img + matchobj.group(3)
        else:
            return matchobj.group(0)

    # Return the result
    return emoticons_regex.sub(_handle_match, input_text)
