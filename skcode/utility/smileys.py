"""
SkCode smileys replacement utility code.
"""

import re
from html import escape as escape_html

from .walketree import walk_tree_for_cls


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
    ('X)', 'dizzy.png'),
    ('X-)', 'dizzy.png'),
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


def setup_smileys_replacement(document_tree, base_url, emoticons_map=DEFAULT_EMOTICONS_MAP, html_class='emoticons'):
    """
    Setup the document for cosmetics replacement.
    :param document_tree: The document tree instance.
    :param emoticons_map: A list of tuple with two values (emoticon_text, emoticon_filename).
    :param base_url: The base url for all emoticon images. Can also be a callable for dynamic paths.
    :param html_class: The HTML class to be assigned to each emoticons img tag (optional).
    """

    # Craft the emoticons regex
    emoticons_regex = '(^|\s+)(?P<emoticon>%s)(\s+|$)' % '|'.join([re.escape(escape_html(e)) for e, _ in emoticons_map])
    emoticons_regex = re.compile(emoticons_regex)

    # Turn emoticons map into a dictionary
    emoticons_map = {escape_html(k): v for k, v in emoticons_map}

    # Turn base_url into a callable
    if isinstance(base_url, str):
        base_path = base_url if base_url.endswith('/') else base_url + '/'
        base_url = lambda x: base_path + x

    # Inject options in all tree node requiring them
    for tree_node in walk_tree_for_cls(document_tree, object):
        if getattr(tree_node.opts, 'inject_smileys_options', False):
            setattr(tree_node.opts, 'emoticons_map', emoticons_map)
            setattr(tree_node.opts, 'emoticons_regex', emoticons_regex)
            setattr(tree_node.opts, 'emoticons_base_url', base_url)
            setattr(tree_node.opts, 'emoticons_html_class', html_class)


def do_smileys_replacement(input_text, options):
    """
    Do all smileys replacement.
    :param input_text: The input text to be processed.
    :param options: The current tag options class (used as storage class by the ``setup_cosmetics_replacement`` function).
    :return: The string with all cosmetics replacement done.
    """

    # Get the cosmetics map from the options container
    emoticons_map = getattr(options, 'emoticons_map', {})
    emoticons_regex = getattr(options, 'emoticons_regex', None)
    base_url = getattr(options, 'emoticons_base_url', None)
    html_class = getattr(options, 'emoticons_html_class', None)

    # Test parameters
    if not emoticons_map or not emoticons_regex or not base_url:
        return input_text

    # Process all cosmetics
    def _handle_match(matchobj):
        emoticon = matchobj.group('emoticon')
        if emoticon in emoticons_map:
            extra_class = ' class="%s"' % html_class if html_class else ''
            img = '<img src="%s" alt="%s"%s>' % (base_url(emoticons_map[emoticon]), emoticon, extra_class)
            return matchobj.group(1) + img + matchobj.group(3)
        else:
            return matchobj.group(0)

    # Return the result
    return emoticons_regex.sub(_handle_match, input_text)
