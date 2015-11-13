"""
SkCode text formating tag definitions code.
"""

from .base import InlineWrappingTagOptions


class BoldTextTagOptions(InlineWrappingTagOptions):
    """ Bold text tag options container class. """

    def __init__(self, **kwargs):
        super(BoldTextTagOptions, self).__init__('<strong>%s</strong>', **kwargs)


class ItalicTextTagOptions(InlineWrappingTagOptions):
    """ Italic text tag options container class. """

    def __init__(self, **kwargs):
        super(ItalicTextTagOptions, self).__init__('<em>%s</em>', **kwargs)


class StrikeTextTagOptions(InlineWrappingTagOptions):
    """ Strike text tag options container class. """

    def __init__(self, **kwargs):
        super(StrikeTextTagOptions, self).__init__('<del>%s</del>', **kwargs)


class UnderlineTextTagOptions(InlineWrappingTagOptions):
    """ Underline text tag options container class. """

    def __init__(self, **kwargs):
        super(UnderlineTextTagOptions, self).__init__('<ins>%s</ins>', **kwargs)


class SubscriptTextTagOptions(InlineWrappingTagOptions):
    """ Subscript text tag options container class. """

    def __init__(self, **kwargs):
        super(SubscriptTextTagOptions, self).__init__('<sub>%s</sub>', **kwargs)


class SupscriptTextTagOptions(InlineWrappingTagOptions):
    """ Supscript text tag options container class. """

    def __init__(self, **kwargs):
        super(SupscriptTextTagOptions, self).__init__('<sup>%s</sup>', **kwargs)


class PreTextTagOptions(InlineWrappingTagOptions):
    """ Pre text tag options container class. """

    def __init__(self, **kwargs):
        super(PreTextTagOptions, self).__init__('<pre>%s</pre>', **kwargs)


class InlineCodeTextTagOptions(InlineWrappingTagOptions):
    """ Inline code text tag options container class. """

    def __init__(self, **kwargs):
        super(InlineCodeTextTagOptions, self).__init__('<code>%s</code>', **kwargs)


class InlineSpoilerTextTagOptions(InlineWrappingTagOptions):
    """ Inline spoiler text tag options container class. """

    def __init__(self, **kwargs):
        super(InlineSpoilerTextTagOptions, self).__init__('<span class="ispoiler">%s</span>', **kwargs)


class KeyboardTextTagOptions(InlineWrappingTagOptions):
    """ Keyboard text tag options container class. """

    def __init__(self, **kwargs):
        super(KeyboardTextTagOptions, self).__init__('<kbd>%s</kbd>', **kwargs)


class HighlightTextTagOptions(InlineWrappingTagOptions):
    """ Highlight text tag options container class. """

    def __init__(self, **kwargs):
        super(HighlightTextTagOptions, self).__init__('<mark>%s</mark>', **kwargs)


class SmallTextTagOptions(InlineWrappingTagOptions):
    """ Small text tag options container class. """

    def __init__(self, **kwargs):
        super(SmallTextTagOptions, self).__init__('<small>%s</small>', **kwargs)
